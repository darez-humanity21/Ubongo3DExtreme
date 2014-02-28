__author__ = 'umayloveme'

import unittest
import shape3d
from shape3d import Shape, Point, ConcreteShape


class TestSequenceFunctions(unittest.TestCase):

    def test_start(self):
        shape = Shape()
        self.assertEqual(0, shape.length)

        points = [Point(0, 0, 0), Point(0, 0, 1)]
        shape2 = Shape(points)
        self.assertEqual(len(points), shape2.length)

    def test_creation(self):
        shape = shape3d.get_shape(0, 1, 1)
        self.assertEqual(3, shape.length)
        self.assertEqual(Point(0, 1, 0), shape.get_position(1))
        self.assertEqual(Point(0, 2, 0), shape.get_position(2))

    def test_rotation(self):
        shape = shape3d.get_shape(0, 2, 2)
        placed = shape.get_rotated(1, 'z')
        self.assertEqual(Point(0, -1, 0), placed.get_position(1))
        self.assertEqual(Point(0, -2, 0), placed.get_position(2))

        placed = shape.get_rotated(2, 'z')
        self.assertEqual(Point(-1, 0, 0), placed.get_position(1))
        self.assertEqual(Point(-2, 0, 0), placed.get_position(2))

        placed = shape.get_rotated(1, 'x')
        self.assertEqual(Point(1, 0, 0), placed.get_position(1))
        self.assertEqual(Point(2, 0, 0), placed.get_position(2))

        placed = shape.get_rotated(1, 'y')
        self.assertEqual(Point(0, 0, 1), placed.get_position(1))
        self.assertEqual(Point(0, 0, 2), placed.get_position(2))

    def test_rotation2(self):
        shape = shape3d.get_shape(0, 1, 2, 5)
        placed = shape.get_rotated(1, 'x')
        self.assertEqual(Point(0, 0, -1), placed.get_position(1))
        self.assertEqual(Point(1, 0, -1), placed.get_position(2))
        self.assertEqual(Point(1, 1, -1), placed.get_position(3))

        placed = shape.get_rotated(1, 'y')
        self.assertEqual(Point(0, 1, 0), placed.get_position(1))
        self.assertEqual(Point(0, 1, 1), placed.get_position(2))
        self.assertEqual(Point(-1, 1, 1), placed.get_position(3))

        placed = shape.get_rotated(1, 'z')
        self.assertEqual(Point(1, 0, 0), placed.get_position(1))
        self.assertEqual(Point(1, -1, 0), placed.get_position(2))
        self.assertEqual(Point(1, -1, 1), placed.get_position(3))

    def test_rotation_back(self):
        shape = shape3d.get_shape(0, 1, 2, 3, 4)
        points = shape.points
        self.assertEqual(5, len(points))
        for d in 'xyz':
            placed = shape.get_rotated(4, d)
            self.assertEqual(placed.points, points)

    def test_same_shape(self):
        self.assertEqual(shape3d.get_shape(0,1,1), shape3d.get_shape(0,1,1))

    def test_concrete_shape_move_and_rotate(self):
        shape = shape3d.get_shape(0,1,2,3)
        self.assertEqual(Point(0,1,0), shape.get_position(1))

        cshape = shape.get_placed(Point(2,2,2))
        self.assertEqual(cshape.origin, shape)
        self.assertEqual(Point(2,3,2), cshape.get_position(1))

        cshape = cshape.get_placed(Point(10, 10, 10))
        self.assertEqual(cshape.origin, shape)
        self.assertEqual(Point(10,11,10), cshape.get_position(1))
        rotated = cshape.get_rotated(1, 'x')
        self.assertEqual(Point(10,10,9), rotated.get_position(1))

# if __name__ == '__main__':
#     # unittest.main()
#     print 'test start'
#     suite1 = TestSequenceFunctions.TheTestSuite()
#     # suite2 = module2.TheTestSuite()
#     alltests = unittest.TestSuite([suite1, suite2])
#     # suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
#     # print dir(suite)
#     # unittest.TextTestRunner(verbosity=2).run(suite)
