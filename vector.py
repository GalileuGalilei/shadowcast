from __future__ import annotations
from math import atan2, cos, sin

class Vector3:
    """
    Class to represent a point in 3D space. Each point has an x, y, and z coordinate.
    """

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other: Vector3) -> float:
        """Calculate Euclidean distance between current point and another point"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5
    
    def distance_squared(self, other: Vector3) -> float:
        """Calculate squared Euclidean distance between current point and another point"""
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
    
    def cross_product(self, other: Vector3) -> Vector3:
        """Calculate the cross product of the current point and another point"""
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)
    
    def dot_product(self, other: Vector3) -> float:
        """Calculate the dot product of the current point and another point"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cossine(self, other: Vector3) -> float:
        """Calculate the cossine of the angle between the current point and another point"""
        
        l1 = self.length()
        l2 = other.length()

        if l1 == 0 or l2 == 0:
            return 0

        return self.dot_product(other) / (l1 * l2)
    
    def normalize(self) -> Vector3:
        """Normalize the current point"""
        magnitude = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return Vector3(self.x / magnitude, self.y / magnitude, self.z / magnitude)
    
    def is_equal_with_tolerance(self, other: Vector3, tolerance: float) -> bool:
        """Check if the current point is equal to another point with a given tolerance"""
        return (abs(self.x - other.x) < tolerance and
                abs(self.y - other.y) < tolerance and
                abs(self.z - other.z) < tolerance)
    
    def truncate(self) -> Vector3:
        """Truncate the current point"""
        return Vector3(int(self.x), int(self.y), int(self.z))
    
    def is_clockwise(self, other: Vector3, normal: Vector3) -> bool:
        """Check if the current point is clockwise to another point with respect to a given normal vector"""
        return self.cross_product(other).dot_product(normal) > 0
    
    def length(self) -> float:
        """Calculate the length of the current point"""
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    def rotate(self, angle: float, axis: Vector3) -> Vector3:
        """Rotate the current point around an axis by a given angle"""

        x = self.x
        y = self.y
        z = self.z
        u = axis.x
        v = axis.y
        w = axis.z

        #apply the rotation matrix
        x_new = (u * (u * x + v * y + w * z) * (1 - cos(angle)) +
                 x * cos(angle) +
                 (-w * y + v * z) * sin(angle))
        y_new = (v * (u * x + v * y + w * z) * (1 - cos(angle)) +
                 y * cos(angle) +
                 (w * x - u * z) * sin(angle))
        z_new = (w * (u * x + v * y + w * z) * (1 - cos(angle)) +
                 z * cos(angle) +
                 (-v * x + u * y) * sin(angle))

        return Vector3(x_new, y_new, z_new)
    
    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> Vector3:
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar: float) -> Vector3:
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __eq__(self, other: Vector3) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self) -> str:
        return f'Point3D({self.x}, {self.y}, {self.z})'
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
class Vector2:
    """
    Class to represent a point in 2D space. Each point has an x and y coordinate.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance(self, other: Vector2) -> float:
        """Calculate Euclidean distance between current point and another point"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def distance_squared(self, other: Vector2) -> float:
        """Calculate squared Euclidean distance between current point and another point"""
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2
    
    def cross_product(self, other: Vector2) -> float:
        """Calculate the cross product of the current point and another point"""
        return self.x * other.y - self.y * other.x
    
    def dot_product(self, other: Vector2) -> float:
        """Calculate the dot product of the current point and another point"""
        return self.x * other.x + self.y * other.y
    
    def angle(self) -> float:
        """Calculate the angle of the current point"""
        return atan2(self.y, self.x)
    
    def cossine(self, other: Vector2) -> float:
        """Calculate the cossine of the angle between the current point and another point"""
        
        l1 = self.length()
        l2 = other.length()

        if l1 == 0 or l2 == 0:
            return 0

        return self.dot_product(other) / (l1 * l2)
    
    def normalize(self) -> Vector2:
        """Normalize the current point"""
        magnitude = (self.x ** 2 + self.y ** 2) ** 0.5
        return Vector2(self.x / magnitude, self.y / magnitude)
    
    def is_equal_with_tolerance(self, other: Vector2, tolerance: float) -> bool:
        """Check if the current point is equal to another point with a given tolerance"""
        return (abs(self.x - other.x) < tolerance and
                abs(self.y - other.y) < tolerance)
    
    def truncate(self) -> Vector2:
        """Truncate the current point"""
        return Vector2(int(self.x), int(self.y))
    
    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> Vector2:
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __eq__(self, other: Vector2) -> bool:
        return self.x == other.x and self.y == other.y
    