__author__ = 'umayloveme'

from point import Point
import rotate


class Shape(object):
    def __init__(self, points=[], name=''):
        self.length = len(points)
        self.points = list(points)
        self.name = name

    def get_points(self):
        return self.points

    def get_position(self, index):
        return self.points[index]

    def get_placed(self, position):
        return ConcreteShape(self, self.points, position)

    def get_rotated(self, times, direction):
        points = rotate.get_rotated(self.points, times, direction)
        return ConcreteShape(self, points)

    def adjust(self):
        x, y, z = 0, 0, 0
        for point in self.points:
            if point.x < x:
                x = point.x
            if point.y < y:
                y = point.y
            if point.z < z:
                z = point.z
        for point in self.points:
            point.x -= x
            point.y -= y
            point.z -= z

    def get_origin(self):
        return self

    def __eq__(self, other):
        return other.points == self.points

    def __repr__(self):
        return self.name or str(self.points)


class ConcreteShape(Shape):

    def __init__(self, origin, points=[], position=None):
        Shape.__init__(self, points)
        self.origin = origin
        self.name = origin.name
        if position:
            self.points = [point+position for point in self.points]
        self.position = position or Point(0,0,0)

    def get_points(self):
        return self.points

    def get_origin(self):
        return self.origin

    def get_placed(self, position):
        return ConcreteShape(self.origin, self._get_initial_points(), position)

    def get_rotated(self, times, direction):
        points = rotate.get_rotated(self._get_initial_points(), times, direction)
        return ConcreteShape(self.origin, points, self.position)

    def _get_initial_points(self):
        return map(lambda p: p-self.position, self.points)


direction_map = {
    0: [0,0,0],
    1:[0,1,0],
    2:[1,0,0],
    3:[0,-1,0],
    4:[-1,0,0],
    5:[0,0,1],
    6:[0,0,-1],
}


def get_shape(*directions):
    start = Point(0,0,0)
    points = []
    for direction in directions:
        coordination = direction_map[direction]
        point_created = Point(start.x + coordination[0], start.y + coordination[1], start.z + coordination[2])
        points.append(point_created)
        start = point_created

    return Shape(points)


def get_aligned(*directions):
    shape = get_shape(*directions)
    shape.adjust()
    return shape


def shape(name, *directions):
    shape = get_aligned(*directions)
    shape.name = name
    return shape


def get_rotated(shape, times, direction):
    points = rotate.get_rotated(shape.points, times, direction)
    return ConcreteShape(shape, points)

