from __future__ import annotations
from math import atan2
from edge import Edge
from vector import Vector2


class LineOfSight:
    def __init__(self) -> None:
        pass

    @staticmethod
    def angle(source: tuple[int, int], target: tuple[int, int]) -> float:
        """
        Calculate the angle between the source point and the target point
        """

        return atan2(target[1] - source[1], target[0] - source[0])

    @staticmethod
    def projection(wall: Edge, source: tuple[int, int], len: tuple[int, int]) -> tuple[int, int]:
        """
        Calculate the intersection of a vector (ray) from the source point passing through the len point 
        with the line segment representing the wall.

        :param wall: An Edge object representing the wall with start and end points (x, y).
        :param source: A tuple representing the source point (x, y).
        :param len: A tuple representing the direction point for the projection (x, y).
        :return: A tuple representing the coordinates of the intersection point (x, y), or None if no intersection exists.
        """

        # Função auxiliar para calcular o determinante 2x2 (serve para calcular a área)
        def determinant(a, b, c, d):
            return a * d - b * c

        # Coordenadas da parede (wall)
        x1, y1 = wall.start
        x2, y2 = wall.end

        # Coordenadas da linha (ray) que passa por source e len
        x3, y3 = source
        x4, y4 = len

        # Cálculo dos determinantes
        denom = determinant(x1 - x2, y1 - y2, x3 - x4, y3 - y4)

        # Se o determinante for zero, as linhas são paralelas ou coincidentes
        if denom == 0:
            return len

        # Calcula as interseções em termos de t e u (parâmetros de linha)
        t = determinant(x1 - x3, y1 - y3, x3 - x4, y3 - y4) / denom
        u = determinant(x1 - x3, y1 - y3, x1 - x2, y1 - y2) / denom

        # Verificar se o ponto de interseção está dentro do segmento da parede (t deve estar entre 0 e 1)
        if 0 <= t <= 1:
            # A linha (ray) não é limitada, então não precisamos verificar o valor de u
            # Cálculo do ponto de interseção
            intersection_x = x1 + t * (x2 - x1)
            intersection_y = y1 + t * (y2 - y1)
            return (int(intersection_x), int(intersection_y))

        # Se t estiver fora do intervalo [0, 1], não há interseção com o segmento da parede
        return len

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
        
        walls = walls + limits  # Combine walls with map limits

        # Create a dictionary with the vertices of the walls ordered by angle from the source
        vertices = {}
        for wall in walls:
            if wall.start not in vertices:
                vertices[wall.start] = []
            if wall.end not in vertices:
                vertices[wall.end] = []

            vertices[wall.start].append(wall)
            vertices[wall.end].append(wall)
        
        vertices = dict(sorted(vertices.items(), key=lambda x: LineOfSight.angle(source, x[0])))

        # Initialize the open list of walls and the final polygon points
        open_walls = []
        polygon = []
        current_nearest_wall = None
        last_vertice = None

        # Iterate over vertices sorted by angle
        for vertice in vertices.keys():
            # Add walls to the open list or remove if already in the list
            for wall in vertices[vertice]:
                if wall in open_walls:
                    open_walls.remove(wall)
                else:
                    open_walls.append(wall)

            # Find the nearest wall
            nearest_wall = None
            for wall in open_walls:
                if nearest_wall is None or wall.distance(source) < nearest_wall.distance(source):
                    nearest_wall = wall

            # If the nearest wall has changed or nearest_wall is None, create a visibility triangle
            if nearest_wall != current_nearest_wall:
                if nearest_wall and last_vertice:
                    polygon.append((source, LineOfSight.projection(nearest_wall, source, vertice), last_vertice))
                elif nearest_wall:
                    polygon.append((source, LineOfSight.projection(nearest_wall, source, vertice), vertice))
                else:
                    # No wall, just create a triangle to the vertex
                    polygon.append((source, vertice, polygon[-1][2]))

            current_nearest_wall = nearest_wall

        return polygon


            

