__author__ = 'umayloveme'

import unittest
import shape3d
from ubongo_map import UbongoMap
from ubongo_player import Spinner
from map_manipulate import MapManipulator
from shape3d import Shape, Point, ConcreteShape


class ObjectMaker:

    def __init__(self):
        self.map_height = 1
        self.map_data = []
        self.blocks = []
        self.spinner_size = 1

    def set_map_info(self, height, *data):
        self.map_data = data
        self.map_height = height

    def set_blocks(self, blocks):
        self.blocks = blocks

    def set_spinner_size(self, size):
        self.spinner_size = size

    def set_spin_order(self, order):
        self.order = order

    def ready(self):
        self.map = UbongoMap([Point.instance(*d) for d in self.map_data], self.map_height)
        self.manipulator = MapManipulator(self.map)
        self.spinner = Spinner(self.get_manipulator(), self.blocks, self.spinner_size)
        self.spinner.set_order(self.order)

    def get_map(self):
        return self.map

    def get_manipulator(self):
        return self.manipulator

    def get_spinner(self):
        return self.spinner


class TestUbongoPlayer(unittest.TestCase):

    def __order(self, sequence):
        if sequence < 4:
            return (1, 'x')
        if sequence == 4:
            return (1, 'y')
        if sequence == 5:
            return (2, 'y')
        return None

    def setUp(self):
        self.factory = ObjectMaker()
        self.stick_block = shape3d.get_aligned(0, 1)
        self.l_stick     = shape3d.get_aligned(0, 6, 1, 1)
        self.twisted_stick = shape3d.get_aligned(0, 6, 2, 1, 1)
        self.twisted_stick.name = 'twisted'

    def test_spin_ready(self):
        self.factory.set_map_info(1,(0,0), (0,1))
        self.factory.set_blocks([self.stick_block])
        self.factory.set_spinner_size(1)
        self.factory.set_spin_order(self.__order)
        self.factory.ready()

        manipulator = self.factory.get_manipulator()
        spinner = self.factory.get_spinner()

        spinner.ready()
        self.assertTrue(manipulator.is_complete())

    def test_spin_container(self):
        self.factory.set_map_info(1,(0,0), (1,0))
        self.factory.set_blocks([self.stick_block])
        self.factory.set_spinner_size(1)
        self.factory.set_spin_order(self.__order)
        self.factory.ready()

        simple_manipulator = self.factory.get_manipulator()
        spinner = self.factory.get_spinner()
        containers = spinner.get_containers()
        self.assertEqual(1, len(containers))

        spinner.ready()
        self.assertEqual(self.stick_block, containers[0].get_current_shape())
        spinner.spin()
        self.assertEqual(self.stick_block.get_rotated(1,'z'), containers[0].get_current_shape())
        self.assertTrue(simple_manipulator.is_complete())

    def test_spin_container2(self):
        self.factory.set_map_info(2,(0,0))
        self.factory.set_blocks([self.stick_block])
        self.factory.set_spinner_size(1)
        self.factory.set_spin_order(self.__order)
        self.factory.ready()

        spinner = self.factory.get_spinner()
        manipulator = self.factory.get_manipulator()
        containers = spinner.get_containers()
        self.assertEqual(1, len(containers))

        spinner.ready()
        self.assertEqual(self.stick_block, containers[0].get_current_shape())
        spinner.spin();self.assertEqual(shape3d.get_shape(0,2), containers[0].get_current_shape())
        spinner.spin();self.assertEqual(shape3d.get_shape(0,3), containers[0].get_current_shape())
        spinner.spin();self.assertEqual(shape3d.get_shape(0,4), containers[0].get_current_shape())
        spinner.spin();self.assertEqual(shape3d.get_shape(0,6), containers[0].get_current_shape())
        self.assertTrue(manipulator.is_complete())

    def __twobythree_setup(self):
        self.factory.set_map_info(2,(0,0), (1,0), (2,0))
        self.factory.set_blocks([self.stick_block, self.l_stick])
        self.factory.set_spinner_size(2)
        self.factory.set_spin_order(self.__order)
        self.factory.ready()

    def test_containers(self):
        self.__twobythree_setup()

        spinner = self.factory.get_spinner()
        containers = spinner.get_containers()

        self.assertEqual(2, len(containers))
        self.assertEqual(containers[0], containers[1].get_prev())
        self.assertEqual(containers[1], containers[0].get_next())

    def test_spin_with_two_pieces(self):
        self.__twobythree_setup()

        spinner = self.factory.get_spinner()
        manipulator = self.factory.get_manipulator()
        containers = spinner.get_containers()
        umap = self.factory.get_map()

        spinner.ready()
        self.assertEqual(self.l_stick, containers[0].get_current_shape())
        self.assertEqual(None, containers[1].get_current_shape())
        self.assertEqual(0, len(umap.in_use_list))

        spinner.spin()
        self.assertEqual(4, len(umap.in_use_list))
        self.assertEqual(self.stick_block, containers[1].get_current_shape())

        spinner.spin()
        self.assertTrue(manipulator.is_complete())
        # self.assertEqual(self.stick_block, containers[1].get_current_shape())

    def test_spin_with_two_pieces_fail(self):
        self.__twobythree_setup()
        self.factory.set_blocks([self.l_stick, self.twisted_stick])
        self.factory.ready()

        spinner = self.factory.get_spinner()
        manipulator = self.factory.get_manipulator()
        containers = spinner.get_containers()
        umap = self.factory.get_map()

        spinner.ready()
        self.assertEqual(0, len(umap.in_use_list))

        for x in range(24):
            spinner.spin()
            self.assertFalse(manipulator.is_complete())
            self.assertEqual(None, containers[1].get_current_shape())

        self.assertEqual(self.l_stick, containers[0].get_current_shape())
        self.assertEqual(1, len(spinner.shapes))
        spinner.spin()
        self.assertEqual(self.twisted_stick, containers[1].get_current_shape())

    def test_soving_straight_forward(self):
        self.__twobythree_setup()
        self.factory.set_map_info(2,(0,2), (1,1), (1,2), (2,1), (2,2), (3,0), (3,1))
        self.factory.set_blocks([shape3d.get_aligned(0,5,1,2,3), self.twisted_stick, shape3d.get_aligned(0,1,2,5)])
        self.factory.set_spinner_size(3)
        self.factory.ready()

        spinner = self.factory.get_spinner()
        manipulator = self.factory.get_manipulator()
        containers = spinner.get_containers()
        umap = self.factory.get_map()

        spinner.ready()

        self.assertEqual(Point.instance(0,2,0), manipulator.get_next_spot())
        while len(umap.in_use_list) == 0:
            spinner.spin()

        self.assertEqual(Point.instance(0,2,1), manipulator.get_next_spot())
        while len(umap.in_use_list) == 4:
            spinner.spin()

        self.assertEqual(Point.instance(2,1,1), manipulator.get_next_spot())
        while len(umap.in_use_list) == 9:
            spinner.spin()

        self.assertTrue(manipulator.is_complete())

    def test_soving_with_one_wrong_block(self):
        self.__twobythree_setup()
        self.factory.set_map_info(2,(0,2), (1,1), (1,2), (2,1), (2,2), (3,0), (3,1))
        self.factory.set_blocks([shape3d.get_aligned(0,5,1,2,3),
                                 shape3d.get_aligned(0,1,2,2,3),
                                 self.twisted_stick,
                                 shape3d.get_aligned(0,1,2,5)])
        self.factory.set_spinner_size(3)
        self.factory.ready()

        spinner = self.factory.get_spinner()
        manipulator = self.factory.get_manipulator()
        umap = self.factory.get_map()

        spinner.ready()

        self.assertEqual(Point.instance(0,2,0), manipulator.get_next_spot())
        while len(umap.in_use_list) == 0:
            spinner.spin()

        self.assertEqual(Point.instance(0,2,1), manipulator.get_next_spot())
        while len(umap.in_use_list) == 4:
            spinner.spin()

        self.assertEqual(Point.instance(2,1,1), manipulator.get_next_spot())
        while len(umap.in_use_list) == 9:
            spinner.spin()

        self.assertTrue(manipulator.is_complete())

    def test_soving_with_one_wrong_block(self):
        self.__twobythree_setup()
        self.factory.set_map_info(2,(0,2), (1,1), (1,2), (2,1), (2,2), (3,0), (3,1))

        mushroom = shape3d.get_aligned(0,5,1,2,3)
        mushroom.name = 'mushroom'
        twistedmini = shape3d.get_aligned(0,1,2,5)
        twistedmini.name = 'twistedmini'
        gate = shape3d.get_aligned(0,1,2,2,3)
        gate.name = 'gate'

        self.factory.set_blocks([mushroom, twistedmini, gate, self.twisted_stick])
        self.factory.set_spinner_size(3)
        self.factory.ready()
        spinner = self.factory.get_spinner()
        manipulator = self.factory.get_manipulator()
        umap = self.factory.get_map()

        spinner.ready()

        while len(umap.in_use_list) == 0:
            spinner.spin()

        while len(umap.in_use_list) == 5:
            spinner.spin()

        while not manipulator.is_complete():
            spinner.spin()
        self.assertTrue(True)

    def test_soving_complete(self):
        self.__twobythree_setup()
        self.factory.set_map_info(2,(0,2), (1,1), (1,2), (2,1), (2,2), (3,0), (3,1))

        mushroom = shape3d.shape('mushroom', 0,5,1,2,3)
        twistedmini = shape3d.shape('twistedmini', 0,1,2,5)
        oozi = shape3d.shape('oozi', 0,2,5,1,1)
        gun = shape3d.shape('gun', 0,5,1,1)
        earthworm = shape3d.shape('earthworm', 0,1,6,1,4)


        self.factory.set_blocks([earthworm, oozi, gun, mushroom, twistedmini])
        self.factory.set_spinner_size(3)
        self.factory.ready()
        spinner = self.factory.get_spinner()
        manipulator = self.factory.get_manipulator()
        umap = self.factory.get_map()

        spinner.ready()

        while not spinner.finished():
            spinner.spin()
            # if manipulator.is_complete():
            #     print umap
        self.assertTrue(True)

    def test_real(self):

        shape_data = {
            '1': [(1,0,0), (1,1,0), (0,1,0), (1,2,0), (1,2,1)],
            '2': [(1,0,1), (1,0,0), (1,1,0), (1,2,0), (0,2,0)],
            '3': [(0,0,0), (0,1,0), (1,1,0), (1,1,1)],
            '4': [(0,0,0), (1,0,0), (1,1,0), (1,2,0), (0,2,0)],
            '5': [(0,0,1), (0,0,0), (1,0,0), (1,1,0), (1,2,0)],
            '6': [(1,0,0), (1,1,0), (0,1,0), (0,2,0), (0,2,1)],
            '7': [(0,0,0), (1,0,0), (1,1,0), (0,1,0), (2,3,0)],
            '8': [(0,0,0), (1,0,0), (1,1,0)],
            '9': [(0,0,0), (1,0,0), (1,1,0), (0,1,0), (1,1,1)],
            '10': [(1,0,0), (1,1,0), (0,1,0), (0,1,1)],
            '11': [(0,0,0), (1,0,0), (1,1,0), (1,2,0), (1,2,1)],
            '12': [(1,0,0), (1,1,0), (0,1,0), (0,2,0)],
            '13': [(0,0,0), (0,1,0), (1,1,0), (1,2,0), (1,2,1)],
            '14': [(1,0,0), (1,1,0), (1,2,0), (0,2,0), (0,2,1)],
            '15': [(1,0,0), (1,1,0), (0,1,0), (1,2,0)],
            '16': [(0,0,0), (1,0,0), (1,1,0), (1,2,0)]
        }

        self.__twobythree_setup()
        self.factory.set_spinner_size(4)
        # self.factory.set_map_info(3,(0,2), (1,1), (1,2), (2,1), (2,2), (3,0), (3,1))
        # self.factory.set_map_info(3,(0,0), (1,0), (2,0), (2,2), (0,1), (0,2), (1,1), (1,2), (2,1))
        shapes = [Shape(map(lambda d:Point.instance(*d),y),x) for x,y in shape_data.items()]

        self.factory.set_blocks(shapes)
        self.factory.set_map_info(2,(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2))
        self.factory.ready()
        umap = self.factory.get_map()
        locations = umap.map_locations
        del umap.map_locations[locations.index(Point(1,0,1))]
        del umap.map_locations[locations.index(Point(1,2,1))]
        # del umap.map_locations[locations.index(Point(2,1,1))]
        print len(umap.map_locations)
        umap._refresh_avails()
        spinner = self.factory.get_spinner()
        manipulator = self.factory.get_manipulator()

        spinner.ready()

        solutions = []
        while not spinner.finished():
            spinner.spin()
            if manipulator.is_complete():
                data = spinner.get_in_use_list()
                data.sort(lambda x,y: cmp(int(x.name), int(y.name)))
                solution = str(data)
                if solution not in solutions:
                    solutions.append(solution)
                    print spinner
                    print umap
                    # if '[8, 16, 9]' == solution:
                    #     print spinner
                    #     print umap
                    # if '[16, 8, 9]' == solution:
                    #     print spinner
                    #     print umap
        solutions.sort()
        print '\n'.join(solutions)
        print 'total:', len(solutions)
