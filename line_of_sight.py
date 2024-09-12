from __future__ import annotations
from math import atan2, sqrt
from edge import Edge
from functools import cmp_to_key


class LineOfSight:
    def __init__(self) -> None:
        pass

    @staticmethod
    def distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
        """
        Calculate the distance between two points.
        """

        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    @staticmethod
    def angle(source: tuple[int, int], target: tuple[int, int]) -> float:
        """
        comparision function to sort points by angle from the source point.
        """

        # Calculate the angle between the source and target points
        angle = -atan2(target[1] - source[1], target[0] - source[0])
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
    def line_intersection(p1_start: tuple[int, int], p1_end: tuple[int, int], 
                p2_start: tuple[int, int], p2_end: tuple[int, int]) -> tuple[float, float]:
        """
        Calculate the intersection point between two lines (p1_start -> p1_end and p2_start -> p2_end).
        The lines are represented by two points each.
        
        Returns:
            The intersection point as a tuple (x, y) if the lines intersect, otherwise None.
        """
        x1, y1 = p1_start
        x2, y2 = p1_end
        x3, y3 = p2_start
        x4, y4 = p2_end

        # Determinant
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # If the determinant is zero, the lines are parallel
        if denom == 0:
            return None

        # Calculate the intersection point
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

        return (px, py) 
    
    @staticmethod
    def build_triangle(source : tuple[int, int], old_vertex : tuple[int, int], current_vertex : tuple[int, int], closest_old_wall : Edge) -> (tuple[int, int, int]):
        """
        Build a visibility triangle from the source point to the current vertex.
        """
        dist1 = LineOfSight.distance(source, old_vertex)
        dist2 = LineOfSight.distance(source, current_vertex)

        closest_vertex = old_vertex if dist1 < dist2 else current_vertex
        far_vertex = current_vertex if dist1 < dist2 else old_vertex
        close_hit_point = LineOfSight.line_intersection(source, closest_vertex, closest_old_wall.start, closest_old_wall.end)
        far_hit_point = LineOfSight.line_intersection(source, far_vertex, closest_old_wall.start, closest_old_wall.end)

        if not close_hit_point:
            close_hit_point = closest_vertex

        if not far_hit_point:
            far_hit_point = far_vertex

        return (source, far_hit_point, close_hit_point)

    @staticmethod
    def build_visibility_triangles(walls: set[Edge], source: tuple[int, int], map_size: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Build the visibility polygon from the source point.
        """
        ##### pygame stuff #######
        # Invert the y-coordinate of the source point
        source = (source[0], map_size[1] - source[1]) 
        # invert the y-coordinate of the walls
        walls = [Edge((wall.start[0], map_size[1] - wall.start[1]), (wall.end[0], map_size[1] - wall.end[1])) for wall in walls]
        ##### pygame stuff #######

        # Add the limits of the map as walls
        limits = [Edge((0, 0), (0, map_size[1])),
                Edge((0, map_size[1]), (map_size[0], map_size[1])),
                Edge((map_size[0], map_size[1]), (map_size[0], 0)),
                Edge((map_size[0], 0), (0, 0))]
        
        # Combine walls with map limits
        walls = walls + limits 

        # Create a dictionary with the vertices of the walls
        walls_per_vertex = {}
        for wall in walls:
            if wall.start not in walls_per_vertex:
                walls_per_vertex[wall.start] = []
            if wall.end not in walls_per_vertex:
                walls_per_vertex[wall.end] = []

            walls_per_vertex[wall.start].append(wall)
            walls_per_vertex[wall.end].append(wall)
        
        # Sort the vertices by angle from the source
        walls_per_vertex = dict(sorted(walls_per_vertex.items(), key=lambda x: LineOfSight.angle(source, x[0])))

        # Initialize the open list of walls and the final polygon points
        open_walls = []
        polygon = []
        old_vertex = None

        #the first pass is only to find the first wall and the last wall
        for passes in range(2):
            # Iterate over vertices sorted by angle
            for vertex in walls_per_vertex.keys():
                # get the old closest wall
                old_nearest_wall = open_walls[0] if open_walls else None

                # Add walls that start at the current vertex and remove wall that end at this vertex
                for wall in walls_per_vertex[vertex]:
                    if wall not in open_walls and not LineOfSight.is_end_point(vertex, wall, source):
                        open_walls.append(wall)
                    if wall in open_walls and LineOfSight.is_end_point(vertex, wall, source):
                        open_walls.remove(wall)

                # Find the new closest wall
                open_walls.sort(key=lambda x: x.distance(source))
                new_nearest_wall = open_walls[0] if open_walls else None
                
                # If the nearest wall has changed, create a visibility triangle
                if new_nearest_wall != old_nearest_wall:
                    if old_nearest_wall and passes == 1:
                        triangle = LineOfSight.build_triangle(source, old_vertex, vertex, old_nearest_wall)
                        polygon.append(triangle)
                    old_vertex = vertex

        ###### pygame stuff ######
        #invert the y-coordinate of the polygon
        polygon = [[(point[0], map_size[1] - point[1]) for point in triangle] for triangle in polygon]
        ###### pygame stuff ######

        return polygon


            

