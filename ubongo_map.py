__author__ = 'umayloveme'
from shape3d import Shape, Point, ConcreteShape


class UbongoMap:

    def __init__(self, points, height):
        self.map_locations = list(points)
        self.height = height
        self.in_use_list = []
        self.shape_map = {}
        for h in range(1, height):
            self.map_locations += map(lambda point: Point(point.x, point.y, h), points)
        self.avail_list = self.map_locations

    def size(self):
        return len(self.map_locations)

    def get_avails(self):
        return self.avail_list
        # return [x for x in self.map_locations if x not in self.in_use_list]

    def is_inside(self, point):
        return point in self.map_locations

    def is_available(self, point):
        return point not in self.in_use_list and self.is_inside(point)

    def _refresh_avails(self):
        self.avail_list = [x for x in self.map_locations if x not in self.in_use_list]

    def check(self, point):
        if point in self.map_locations and point not in self.in_use_list:
            self._append(point)
            self._refresh_avails()

    def _append(self, point):
        self.in_use_list.append(point)

    def fill(self, shape):
        if self.fits(shape):
            points = shape.get_points()
            self.shape_map[shape.get_origin()] = points
            map(self._append, points)
            self._refresh_avails()

    def remove(self, shape):
        origin = shape.get_origin()
        if origin in self.shape_map:
            del self.shape_map[origin]
            self.in_use_list = sum(self.shape_map.values(), [])
            self._refresh_avails()

    def fits(self, shape):
        for point in shape.get_points():
            if not self.is_available(point):
                return False
        return True

    def is_full(self):
        return len(self.map_locations) == len(self.in_use_list)
        # def sorter(p1, p2):
        #     if p1.x == p2.x:
        #         if p1.y == p2.y:
        #             return p1.z - p2.z
        #         else:
        #             return p1.y - p2.y
        #     else:
        #         return p1.x - p2.x
        #
        # self.map_locations.sort(sorter)
        # self.in_use_list.sort(sorter)
        # return self.map_locations == self.in_use_list


    def __repr__(self):
        return "Ubongo Map:\n%s\n" % (str(self.shape_map))
