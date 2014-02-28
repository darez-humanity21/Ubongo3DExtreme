__author__ = 'umayloveme'

import math
from point import Point

angle = math.pi/2
cos = int(math.cos(angle))
sin = int(math.sin(angle))

rotation_map = {
    'x': lambda x, y, z: [x, y*cos + z*sin,z*cos - y*sin],
    'y': lambda x, y, z: [x*cos-z*sin, y, x*sin + z*cos],
    'z': lambda x, y, z: [x*cos+y*sin, y*cos-x*sin, z]
}

# For performance purposes
rotation_map = {
    'x': lambda x, y, z: [x, z, -y],
    'y': lambda x, y, z: [-z, y, x],
    'z': lambda x, y, z: [y, -x, z]
}


def _repeat(f, data, times):
    if times <= 0:
        return data
    else:
        return _repeat(f, f(data), times-1)


def get_rotated(origin_points, times, direction):
    rotate = rotation_map[direction]
    f = lambda points: [Point(*rotate(*point.to_array())) for point in points]
    return _repeat(f, origin_points, times)
