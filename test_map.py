__author__ = 'umayloveme'


import unittest
import shape3d
from ubongo_map import UbongoMap
from shape3d import Shape, Point, ConcreteShape


class TestMapFunctions(unittest.TestCase):

    def setUp(self):
        self.umap = UbongoMap([Point(0, 0), Point(1,0), Point(0,1), Point(1,1)], 2)
        self.floor0 = shape3d.get_shape(0, 1, 2, 3)
        self.floor1 = shape3d.get_shape(0, 1, 2, 3).get_placed(Point.instance(0,0,1))

    def test_start(self):
        self.assertEqual(1, UbongoMap([Point(0, 0)], 1).size())
        self.assertEqual(2, UbongoMap([Point(0, 0)], 2).size())

    def test_inside(self):
        self.assertEqual(8, self.umap.size())
        self.assertTrue(self.umap.is_inside(Point.instance(0,0,0)))
        self.assertTrue(self.umap.is_inside(Point.instance(0,0,1)))
        self.assertFalse(self.umap.is_inside(Point.instance(0,0,2)))

    def test_fill(self):
        self.assertTrue(self.umap.is_available(Point.instance(0,0,0)))
        self.umap.check(Point.instance(0,0,0))
        self.assertFalse(self.umap.is_available(Point.instance(0,0,0)))

    def test_fit_basic(self):
        self.assertTrue(self.umap.fits(shape3d.get_shape(0,1)))
        self.assertFalse(self.umap.fits(shape3d.get_shape(0,1,1)))

    def test_fill(self):
        self.umap.fill(self.floor0)
        self.assertFalse(self.umap.is_available(Point.instance(0,0,0)))
        self.assertFalse(self.umap.is_available(Point.instance(0,1,0)))
        self.assertFalse(self.umap.is_available(Point.instance(1,0,0)))
        self.assertFalse(self.umap.is_available(Point.instance(1,1,0)))

    def test_fill_fail(self):
        self.umap.check(Point.instance(0,0,0))
        self.assertFalse(self.umap.is_available(Point.instance(0,0,0)))
        self.umap.fill(self.floor0)
        self.assertFalse(self.umap.is_available(Point.instance(0,0,0)))
        self.assertTrue(self.umap.is_available(Point.instance(0,1,0)))
        self.assertTrue(self.umap.is_available(Point.instance(1,0,0)))
        self.assertTrue(self.umap.is_available(Point.instance(1,1,0)))

    def test_is_full(self):
        self.assertFalse(self.umap.is_full())
        self.umap.fill(self.floor0)

        #wrong block
        self.umap.check(Point.instance(0,0,0))
        self.umap.check(Point.instance(0,0,3))

        self.umap.fill(self.floor1)
        self.assertTrue(self.umap.is_full())

    def test_fit_with_checked(self):
        self.umap.check(Point.instance(0,0,0))
        self.assertFalse(self.umap.fits(Shape([Point.instance(0,0,0), Point.instance(1,0,0)])))
        self.assertTrue(self.umap.fits(Shape([Point.instance(0,1,0), Point.instance(1,1,0)])))

    def test_remove(self):
        self.umap.fill(self.floor0)
        self.umap.fill(self.floor1)

        self.assertFalse(self.umap.is_available(Point.instance(0,0,0)))
        self.assertFalse(self.umap.is_available(Point.instance(0,0,1)))

        self.umap.remove(self.floor0)
        self.assertTrue(self.umap.is_available(Point.instance(0,0,0)))
        self.assertFalse(self.floor0 in self.umap.shape_map)
        self.assertEqual(4, len(self.umap.in_use_list))

        self.umap.remove(self.floor1)
        self.assertTrue(self.umap.is_available(Point.instance(0,0,1)))
        self.assertFalse(self.floor1 in self.umap.shape_map)
        self.assertEqual(0, len(self.umap.in_use_list))




