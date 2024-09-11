class Edge:
    def __init__(self, start : tuple[int, int], end : tuple[int, int]):
        self.start = start
        self.end = end

    def lenght(self) -> float:
        return ((self.start[0] - self.end[0]) ** 2 + (self.start[1] - self.end[1]) ** 2) ** 0.5
    
    def distance(self, point : tuple[int, int]) -> float:
        """
        Calculate the distance between the edge and a point
        """
        x, y = point
        x1, y1 = self.start
        x2, y2 = self.end
        return abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / self.lenght()