__author__ = 'umayloveme'


class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y and other.z == self.z

    def __repr__(self):
        return "(%d, %d, %d)" % (self.x, self.y, self.z)

    def to_array(self):
        return [self.x, self.y, self.z]

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y, self.z-other.z)

    @classmethod
    def instance(cls, x=0, y=0, z=0):
        return cls(x,y,z)
