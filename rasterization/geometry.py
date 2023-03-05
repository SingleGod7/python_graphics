from math import cos, sin, sqrt, radians

class Vec2:
    def __init__(self, *args) -> None:
        temp = list(args)
        if(len(temp) == 1 and isinstance(temp[0], (tuple, list))):
            self.x, self.y = temp[0]
        if(len(temp) == 2):
            self.x = temp[0]
            self.y = temp[1]

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        else:
            return Vec2(self.x * other.x, self.y * other.y)
    def __rmul__(self, other):
        return self * other
    
    def __str__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    def rotate(self, angle):
        #默认为顺时针旋转
        angle = radians(angle)
        return Vec2(cos(angle) * self.x - sin(angle) * self.y, sin(angle) * self.x + cos(angle) * self.y)
    
    def to_tuple(self):
        return (self.x, self.y)
    
    def norm(self):
        length = sqrt(self.x * self.x + self.y * self.y)
        self.x /= length
        self.y /= length
        return Vec2(self.x, self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def det(self, other):
        return self.x * other.y - self.y * other.x
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x
    

class Vec3:
    def __init__(self, *args) -> None:
        temp = list(args)
        if(len(temp) == 1 and isinstance(temp[0], (tuple, list))):
            self.x, self.y, self.z = temp[0]
        if(len(temp) == 3):
            self.x = temp[0]
            self.y = temp[1]
            self.z = temp[2]

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
    def __rmul__(self, other):
        return self * other
    
    def __str__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"
    
    def rotate(self, angle):
        #默认为顺时针旋转
        pass
    
    def to_tuple(self):
        return (self.x, self.y, self.z)
    
    def norm(self):
        length = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        self.x /= length
        self.y /= length
        self.z /= length
        return Vec3(self.x, self.y, self.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def det(self, other):
        return self.x * other.y - self.y * other.x + self.z * other.x - self.x * other.z + self.y * other.z - self.z * other.y

    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)