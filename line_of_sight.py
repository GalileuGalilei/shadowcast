from __future__ import annotations
from math import atan2
from edge import Edge
from vector import Vector2
import numpy as np


class LineOfSight:
    def __init__(self) -> None:
        pass

    @staticmethod
    def angle(source: tuple[int, int], target: tuple[int, int]) -> float:
        """
        comparision function to sort points by angle from the source point.
        """

        # Calculate the angle between the source and target points
        angle = -np.arctan2(target[1] - source[1], target[0] - source[0])


        return angle
    
    @staticmethod
    def is_clockwise(p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]) -> bool:
        """
        Check if the points are in clockwise order.
        """
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) < 0
    
    @staticmethod
    def is_end_point(end: tuple[int,int], wall : Edge, source: tuple[int,int]):
        """
        Check if the point is an end point of the wall.
        """

        start = wall.start if wall.end == end else wall.end
        return LineOfSight.is_clockwise(source, start, end)
        
    @staticmethod
    def raycast(wall: Edge, ray_start, ray_dir) -> tuple[int, int] | None:
        """
        Raycast from the source point (ray_start) in the direction (ray_dir) to check for
        an intersection with the wall (Edge). Returns the intersection point if found, otherwise None.
        """
        # Unpack the wall's start and end points
        x1, y1 = wall.start
        x2, y2 = wall.end

        # Unpack the ray's starting point and direction
        x3, y3 = ray_start
        dx_ray, dy_ray = ray_dir

        #normalize the ray direction
        #norm = (dx_ray ** 2 + dy_ray ** 2) ** 0.5
        #dx_ray /= norm
        #dy_ray /= norm
        

        # Calculate wall direction (vector)
        dx_wall = x2 - x1
        dy_wall = y2 - y1

        # Denominator for determining intersection (based on 2D cross product)
        denominator = (-dx_ray * dy_wall + dx_wall * dy_ray)

        # If the denominator is zero, the lines are parallel and do not intersect
        if abs(denominator) < 1e-6:
            return (ray_start[0] + ray_dir[0], ray_start[1] + ray_dir[1])  # No intersection (or the lines are nearly parallel)

        # Numerators for solving the parametric intersection equations
        t_wall = (dx_ray * (y3 - y1) - dy_ray * (x3 - x1)) / denominator
        t_ray = (-dx_wall * (y3 - y1) + dy_wall * (x3 - x1)) / denominator

        # Check if the intersection occurs within the bounds of the wall and along the ray
        if 0 <= t_wall <= 1 and t_ray >= 0:
            # Calculate the intersection point
            intersection_x = x3 + t_ray * dx_ray
            intersection_y = y3 + t_ray * dy_ray
            return (int(intersection_x), int(intersection_y))

        return (ray_start[0] + ray_dir[0], ray_start[1] + ray_dir[1])  # No intersection (or the lines are nearly parallel)

    @staticmethod
    def build_visibility_triangles(walls: set[Edge], source: tuple[int, int], map_size: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Build the visibility polygon from the source point.
        """
        # Add the limits of the map as walls
        limits = [Edge((0, 0), (0, map_size[1])),
                Edge((0, map_size[1]), (map_size[0], map_size[1])),
                Edge((map_size[0], map_size[1]), (map_size[0], 0)),
                Edge((map_size[0], 0), (0, 0))]
        
        source = (source[0], map_size[1] - source[1])  # Invert the y-coordinate of the source point
        #invert the y-coordinate of the walls
        walls = [Edge((wall.start[0], map_size[1] - wall.start[1]), (wall.end[0], map_size[1] - wall.end[1])) for wall in walls]


        walls = walls + limits  # Combine walls with map limits

        # Create a dictionary with the vertices of the walls ordered by angle from the source
        wall_per_vertex = {}
        for wall in walls:
            if wall.start not in wall_per_vertex:
                wall_per_vertex[wall.start] = []
            if wall.end not in wall_per_vertex:
                wall_per_vertex[wall.end] = []

            wall_per_vertex[wall.start].append(wall)
            wall_per_vertex[wall.end].append(wall)
        
        #vertices = dict(sorted(vertices.items(), key=lambda x: LineOfSight.angle(source, x[0])))
        vertices = list(wall_per_vertex.keys())
        vertices.sort(key=lambda x: LineOfSight.angle(source, x))
        #create a list of type tuple[tuple[int,int], list[Edge]]
        wall_per_vertex = [(vertice, wall_per_vertex[vertice]) for vertice in vertices]

        # Initialize the open list of walls and the final polygon points
        open_walls = []
        polygon = []
        current_nearest_wall = None
        last_vertice = None

        # Iterate over vertices sorted by angle
        for vertice, walls in wall_per_vertex:
            # Add walls to the open list or remove if already in the list
            for wall in walls:
                if wall in open_walls and LineOfSight.is_end_point(vertice, wall, source):
                    open_walls.remove(wall)
                elif wall not in open_walls and not LineOfSight.is_end_point(vertice, wall, source):
                    open_walls.append(wall)

            # Find the nearest wall
            nearest_wall = None
            for wall in open_walls:
                if nearest_wall is None or wall.distance(source) < nearest_wall.distance(source):
                    nearest_wall = wall

            # If the nearest wall has changed, create a visibility triangle
            if nearest_wall != current_nearest_wall:
                if current_nearest_wall:
                    ray_dir = (vertice[0] - source[0], vertice[1] - source[1])
                    hit_point = LineOfSight.raycast(current_nearest_wall, source, ray_dir)
                    
                    if not hit_point:
                        print("This was not supossed to happen. Error in raycast")
                        break
                    polygon.append((source, last_vertice, hit_point))
                last_vertice = vertice
                current_nearest_wall = nearest_wall
            

        polygon.append((source, polygon[-1][-1], polygon[0][1]))

        #invert the y-coordinate of the polygon
        polygon = [[(point[0], map_size[1] - point[1]) for point in triangle] for triangle in polygon]

        return polygon


            

