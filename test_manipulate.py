__author__ = 'umayloveme'

import unittest
import shape3d
from ubongo_map import UbongoMap
from map_manipulate import MapManipulator
from shape3d import Shape, Point, ConcreteShape


class TestProblemSolving(unittest.TestCase):

    def setUp(self):
        map_data    = [(0,2),  (1,1), (1,2), (2,1), (2,2), (3,0), (3,1)]

        self.umap   = UbongoMap(map(lambda d: Point.instance(*d), map_data), 2)
        self.manipulator = MapManipulator(self.umap)

        self.yellow_block   = shape3d.get_aligned(0,2,3,5)
        self.blue_block     = shape3d.get_aligned(0,2,2,6,3)
        self.red_block      = shape3d.get_aligned(0,2,6,3,5)
        self.wrong_block    = shape3d.get_aligned(0,1,1,1)

    def test(self):
        self.assertEqual(14, self.umap.size())
        self.assertTrue(self.umap.is_inside(Point.instance(1,1,0)))

    def test_fill_yellow(self):
        self.umap.fill(self.yellow_block.get_placed(Point(0,1,0)))
        self.assertFalse(self.umap.is_available(Point.instance(0,2,0)))
        self.assertFalse(self.umap.is_available(Point.instance(1,1,0)))
        self.assertFalse(self.umap.is_available(Point.instance(1,2,0)))

        self.umap.fill(self.blue_block.get_placed(Point(0,1,0)))
        self.umap.fill(self.red_block.get_placed(Point(2,0,0)))

        self.umap.is_full()
        self.assertTrue(self.umap.is_full())

    def test_find_next_spot(self):
        next = self.manipulator.get_next_spot()
        self.assertEqual(Point.instance(0,2,0), next)

        self.umap.check(next)
        next = self.manipulator.get_next_spot()
        self.assertEqual(Point.instance(0,2,1), next)

        self.umap.check(next)
        next = self.manipulator.get_next_spot()
        self.assertEqual(Point.instance(1,1,0), next)

    def test_find_starting_point(self):
        self.assertEqual(Point.instance(0,1,0), self.manipulator.get_starting_point(self.yellow_block))
        points = Point.instance(0, 0, 0), Point.instance(0, -1, 0), Point.instance(0, -1, 1), Point.instance(1, -1, 1), Point.instance(2, -1, 1)
        self.assertEqual(Point.instance(0,-1,0), self.manipulator.get_starting_point(Shape(points)))

    def test_includes(self):
        self.assertTrue(self.manipulator.has_room(self.yellow_block))

    def test_put_shape(self):
        self.manipulator.put(self.yellow_block)
        self.assertFalse(self.umap.is_available(Point.instance(0,2,0)))
        self.assertFalse(self.umap.is_available(Point.instance(1,1,0)))
        self.assertFalse(self.umap.is_available(Point.instance(1,1,1)))
        self.assertFalse(self.umap.is_available(Point.instance(1,2,0)))
        self.assertEqual(4, len(self.umap.in_use_list))
        self.assertEqual(Point.instance(0,2,1), self.manipulator.get_next_spot())

        self.manipulator.put(self.blue_block)
        self.assertEqual(9, len(self.umap.in_use_list))

        self.manipulator.put(self.red_block)
        self.assertEqual(14, len(self.umap.in_use_list))
        self.assertTrue(self.umap.is_full())

    def test_wrong_put(self):
        self.assertFalse(self.manipulator.has_room(self.wrong_block))
        self.manipulator.put(self.wrong_block)
        self.assertEqual(0, len(self.umap.in_use_list))
