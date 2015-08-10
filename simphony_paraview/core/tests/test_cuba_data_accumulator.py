import unittest

import numpy
from numpy.testing import assert_array_equal
from paraview.numpy_support import vtk_to_numpy
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer
from simphony.testing.utils import create_data_container, dummy_cuba_value

from simphony_paraview.core.api import CUBADataAccumulator, supported_cuba


class TestCUBADataAccumulator(unittest.TestCase):

    def test_accumulate(self):
        # given
        cuds_data = [create_data_container(constant=i) for i in range(10)]

        # when
        accumulator = CUBADataAccumulator()
        for data in cuds_data:
            accumulator.append(data)

        # then
        self.assertEqual(len(accumulator), 10)
        expected_cuba = set(CUBA) & supported_cuba()
        self.assertEqual(accumulator.keys, expected_cuba)
        for cuba in expected_cuba:
            default = dummy_cuba_value(cuba)
            if isinstance(default, numpy.ndarray):
                new_shape = (10,) + default.shape
                assert_array_equal(
                    vtk_to_numpy(accumulator[cuba]).reshape(new_shape),
                    [dummy_cuba_value(cuba, constant=i) for i in range(10)])
            else:
                assert_array_equal(
                    vtk_to_numpy(accumulator[cuba]),
                    [dummy_cuba_value(cuba, constant=i) for i in range(10)])

    def test_accumulate_on_keys(self):
        # given
        cuds_data = [create_data_container(constant=i) for i in range(10)]

        # when
        accumulator = CUBADataAccumulator(keys=[CUBA.NAME, CUBA.TEMPERATURE])

        # then
        self.assertEqual(len(accumulator), 0)
        self.assertEqual(accumulator.keys, set([CUBA.TEMPERATURE]))

        # when
        for data in cuds_data:
            accumulator.append(data)

        # then
        self.assertEqual(len(accumulator), 10)
        self.assertEqual(accumulator.keys, set([CUBA.TEMPERATURE]))
        assert_array_equal(
            vtk_to_numpy(accumulator[CUBA.TEMPERATURE]),
            [dummy_cuba_value(
                CUBA.TEMPERATURE, constant=i) for i in range(10)])

    def test_accumulate_with_missing_values(self):
        # given
        accumulator = CUBADataAccumulator()

        # when
        accumulator.append(DataContainer())

        # then
        self.assertEqual(len(accumulator), 1)

        # when
        accumulator.append(
            create_data_container(
                restrict=[CUBA.NAME, CUBA.TEMPERATURE], constant=7))

        # then
        self.assertEqual(len(accumulator), 2)
        self.assertEqual(accumulator.keys, set([CUBA.TEMPERATURE]))
        array = vtk_to_numpy(accumulator[CUBA.TEMPERATURE])
        assert_array_equal(
            array, [numpy.nan, dummy_cuba_value(CUBA.TEMPERATURE, constant=7)])

    def test_accumulate_and_expand(self):
        # given
        accumulator = CUBADataAccumulator()

        # when
        accumulator.append(create_data_container(restrict=[CUBA.MASS]))

        # then
        self.assertEqual(len(accumulator), 1)

        # when
        accumulator.append(
            create_data_container(restrict=[CUBA.NAME, CUBA.TEMPERATURE]))

        # then
        self.assertEqual(len(accumulator), 2)
        self.assertEqual(accumulator.keys, set([CUBA.MASS, CUBA.TEMPERATURE]))
        assert_array_equal(
            vtk_to_numpy(accumulator[CUBA.TEMPERATURE]),
            [numpy.nan, dummy_cuba_value(CUBA.TEMPERATURE)])
        assert_array_equal(
            vtk_to_numpy(accumulator[CUBA.MASS]),
            [dummy_cuba_value(CUBA.MASS), numpy.nan])
