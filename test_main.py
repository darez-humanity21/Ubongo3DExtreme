__author__ = 'umayloveme'
import unittest


def suite():
    modules_to_test = ('test_shape', 'test_map', 'test_manipulate', 'test_player')
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')

