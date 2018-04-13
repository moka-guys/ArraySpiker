"""Contains tests for array_spiker.py and associate scripts"""

import unittest2 as unittest
from analysis_helpers import *
from moka_helpers import *


class ArraySpikerTest(unittest.TestCase):
    """Tests for array_spiker.py."""

    def test_label_maker(self):
        """Is file name string shortened correctly for use as a label in plot"""
        self.assertEquals(make_pretty_label("258503010103_S01_Guys121919_CGH_1100_Jul11_2_1_3.txt"),
                          "258503010103_2_1_3",
                          msg="ERROR: string returned by make_pretty_label() does not match expected output")

    def test_creation_of_output_directory(self):
        """Test that output directory name is processed correctly"""
        cwd = os.getcwd()
        test_regex = r"^" + re.escape(cwd) + "/array_spiker_output_"
        self.assertRegexpMatches(create_output_directory(cwd),
                                 test_regex,
                                 msg="ERROR: str returned by create_output_directory() does not match expected output")

    def test_create_sample_name(self):
        """Test that FE file name is created correctly"""
        message = "ERROR: string returned by create_sample_name() does not match expected output"
        self.assertEquals(create_sample_filename("258503010062", 1),
                          "258503010062_S01_Guys121919_CGH_1100_Jul11_2_1_1",
                          msg=message)
        self.assertEquals(create_sample_filename("258503010062", 2),
                          "258503010062_S01_Guys121919_CGH_1100_Jul11_2_1_2",
                          msg=message)
        self.assertEquals(create_sample_filename("258503010062", 8),
                          "258503010062_S01_Guys121919_CGH_1100_Jul11_2_2_4",
                          msg=message)

    def test_subarray_id_translator(self):
        """Test that translation between MOKA and FE filename subarray IDs is correct"""
        message = "ERROR: string returned by test_subarray_id_translator() does not match expected output"
        self.assertEquals(subarray_id_translator(3), "1_3", msg=message)
        self.assertEquals(subarray_id_translator(4), "1_4", msg=message)
        self.assertEquals(subarray_id_translator(5), "2_1", msg=message)
        self.assertEquals(subarray_id_translator(6), "2_2", msg=message)
        self.assertEquals(subarray_id_translator(7), "2_3", msg=message)
        self.assertEquals(subarray_id_translator(3), subarray_id_translator(3, 0), msg=message)
        # Check that translation works from FE File IDs ---> Moka IDs
        self.assertEquals(subarray_id_translator("2_3", 1), 7, msg=message)
        self.assertEquals(subarray_id_translator("1_2", 1), 2, msg=message)


if __name__ == '__main__':
    unittest.main()
