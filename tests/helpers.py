import unittest


def list_1d_almost_equal(tself: unittest.TestCase, list_a, list_b, places=5):
    tself.assertEqual(len(list_a), len(list_b))
    for a, b in zip(list_a, list_b):
        tself.assertAlmostEqual(a, b, places=places)
