__author__ = 'umayloveme'

import shape3d
from ubongo_map import UbongoMap
from shape3d import Shape, Point, ConcreteShape

class MapManipulator:

    def __init__(self, umap):
        self.umap = umap

    def is_complete(self):
        return self.umap.is_full()

    def get_next_spot(self):
        return self._find_next(self.umap.get_avails())

    def get_starting_point(self, shape):
        return self._find_next(shape.get_points())

    def put(self, shape):
        self.umap.fill(self._get_adjusted(shape))

    def remove(self, shape):
        self.umap.remove(shape)

    def has_room(self, shape):
        placed = self._get_adjusted(shape)
        return placed and self.umap.fits(placed)

    def _get_adjusted(self, shape):
        next_spot = self.get_next_spot()
        if not next_spot:
            return None
        return shape.get_placed(next_spot - self.get_starting_point(shape))

    def _find_next(self, points):
        if not points:
            return None
        selected = points[0]
        for point in points:
            if point.x < selected.x:
                selected = point
            elif point.x == selected.x:
                if point.y < selected.y:
                    selected = point
                elif point.y == selected.y:
                    if point.z < selected.z:
                        selected = point
        return selected