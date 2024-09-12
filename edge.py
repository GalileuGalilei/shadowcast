from math import sqrt


class Edge:
    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        self.start = start
        self.end = end

    def midpoint(self) -> tuple[int, int]:
        """Calcula o ponto médio da aresta."""
        return ((self.start[0] + self.end[0]) / 2, (self.start[1] + self.end[1]) / 2)

    def distance(self, point: tuple[int, int]) -> float:
        """Calcula a distância entre o ponto fornecido a aresta."""

        sx = self.start[0]
        ex = self.end[0]

        if sx > ex:
            sx, ex = ex, sx

        sy = self.start[1]
        ey = self.end[1]

        if sy > ey:
            sy, ey = ey, sy

        if sx <= point[0] <= ex and sy <= point[1] <= ey:
            return 0
        
        if point[0] > sx and point[0] < ex:
            return min(abs(point[1] - sy), abs(point[1] - ey))
        
        if point[1] > sy and point[1] < ey:
            return min(abs(point[0] - sx), abs(point[0] - ex))
        
        dist1 = sqrt((sx - point[0]) ** 2 + (sy - point[1]) ** 2)
        dist2 = sqrt((ex - point[0]) ** 2 + (ey - point[1]) ** 2)
        return min(dist1, dist2)

    def orientation(self, p: tuple[int, int]) -> int:
        """Calcula a orientação entre a parede e o ponto fornecido."""
        # Utilizamos uma variação do determinante para calcular a orientação
        val = (self.end[1] - self.start[1]) * (p[0] - self.end[0]) - (self.end[0] - self.start[0]) * (p[1] - self.end[1])
        if val == 0:
            return 0  # Colinear
        return 1 if val > 0 else -1  # 1 para sentido horário, -1 para anti-horário

    def intersects(self, other: 'Edge') -> bool:
        """Verifica se essa aresta cruza outra aresta."""
        # Aqui, usamos a orientação para determinar se as paredes se cruzam
        o1 = self.orientation(other.start)
        o2 = self.orientation(other.end)
        o3 = other.orientation(self.start)
        o4 = other.orientation(self.end)

        return o1 != o2 and o3 != o4
    
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.start == other.start and self.end == other.end or self.start == other.end and self.end == other.start
    
    def __hash__(self):
        return hash((self.start, self.end))
    
    