# -*- coding: utf-8 -*-


import os
import gzip

import numpy as np
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
import pandas as pd

from nose.tools import with_setup, raises

from FSICdata.eurostat import tsv as reader


def setup():
    global test_input_data
    test_input_data = '''\
indic_na,s_adj,geo\\time\t2014Q2\t2014Q1\t2013Q4\t2013Q3\t2013Q2\t2013Q1
B1GM,SA,EU28\t1\t2\t:\t: \t5\t6
B1GM,SA,EU27\t7\t8\t9\t10\t11\t12
B1G,SA,EU28\t13 p\t: p\t:\t: \t:\t:
B1G,SA,EU27\t19\t20\t21\t22\t23\t24
'''
    column_order = [
        'indic_na', 's_adj', 'geo\\time',
        '2014Q2', '2014Q1',
        '2013Q4', '2013Q3', '2013Q2', '2013Q1']

    global expected_raw
    expected_raw = DataFrame(
        {'indic_na': ['B1GM', 'B1GM', 'B1G', 'B1G'],
         's_adj': ['SA', 'SA', 'SA', 'SA'],
         'geo\\time': ['EU28', 'EU27', 'EU28', 'EU27'],
         '2014Q2': ['1', '7', '13 p', '19'],
         '2014Q1': ['2', '8', ': p', '20'],
         '2013Q4': [np.NaN, 9, np.NaN, 21],
         '2013Q3': [np.NaN, 10, np.NaN, 22],
         '2013Q2': [5, 11, np.NaN, 23],
         '2013Q1': [6, 12, np.NaN, 24], })
    expected_raw = expected_raw[column_order]

    global expected_clean
    expected_clean = DataFrame(
        {'indic_na': ['B1GM', 'B1GM', 'B1G', 'B1G'],
         's_adj': ['SA', 'SA', 'SA', 'SA'],
         'geo\\time': ['EU28', 'EU27', 'EU28', 'EU27'],
         '2014Q2': [1.0, 7.0, 13.0, 19.0],
         '2014Q1': [2.0, 8.0, np.NaN, 20.0],
         '2013Q4': [np.NaN, 9.0, np.NaN, 21.0],
         '2013Q3': [np.NaN, 10.0, np.NaN, 22.0],
         '2013Q2': [5.0, 11.0, np.NaN, 23.0],
         '2013Q1': [6.0, 12.0, np.NaN, 24.0], })
    expected_clean = expected_clean[column_order]

    global expected_structured
    expected_structured = DataFrame(
        {'indic_na': ['B1GM', 'B1GM', 'B1G', 'B1G', 'B1GM',
                      'B1GM', 'B1G', 'B1G', 'B1GM', 'B1GM',
                      'B1G', 'B1G', 'B1GM', 'B1GM', 'B1G',
                      'B1G', 'B1GM', 'B1GM', 'B1G', 'B1G',
                      'B1GM', 'B1GM', 'B1G', 'B1G'],
         's_adj': [ 'SA', 'SA', 'SA', 'SA', 'SA',
                    'SA', 'SA', 'SA', 'SA', 'SA',
                    'SA', 'SA', 'SA', 'SA', 'SA',
                    'SA', 'SA', 'SA', 'SA', 'SA',
                    'SA', 'SA', 'SA', 'SA'],
         'geo': ['EU28', 'EU27', 'EU28', 'EU27', 'EU28',
                 'EU27', 'EU28', 'EU27', 'EU28', 'EU27',
                 'EU28', 'EU27', 'EU28', 'EU27', 'EU28',
                 'EU27', 'EU28', 'EU27', 'EU28', 'EU27',
                 'EU28', 'EU27', 'EU28', 'EU27'],
         'time': ['2014Q2', '2014Q2', '2014Q2', '2014Q2', '2014Q1',
                  '2014Q1', '2014Q1', '2014Q1', '2013Q4', '2013Q4',
                  '2013Q4', '2013Q4', '2013Q3', '2013Q3', '2013Q3',
                  '2013Q3', '2013Q2', '2013Q2', '2013Q2', '2013Q2',
                  '2013Q1', '2013Q1', '2013Q1', '2013Q1'],
         'value': [1.0, 7.0, 13.0, 19.0, 2.0,
                   8.0, np.NaN, 20.0, np.NaN, 9.0,
                   np.NaN, 21.0, np.NaN, 10.0, np.NaN,
                   22.0, 5.0, 11.0, np.NaN, 23.0,
                   6.0, 12.0, np.NaN, 24.0]})
    expected_structured = expected_structured[[
        'indic_na', 's_adj', 'geo', 'time', 'value']]


@with_setup(setup)
def test_read():
    input_file = 'test.tsv'
    with open(input_file, 'wt') as f:
        f.write(test_input_data)
    data = reader.read(input_file)
    os.remove(input_file)
    assert_frame_equal(data, expected_structured)


@with_setup(setup)
def test_read_no_structure():
    input_file = 'test.tsv'
    with open(input_file, 'w') as f:
        f.write(test_input_data)
    data = reader.read(input_file, form='raw')
    os.remove(input_file)
    assert_frame_equal(data, expected_clean)


@with_setup(setup)
@raises(ValueError)
def test_read_bad_structure():
    input_file = 'test.tsv'
    with open(input_file, 'wt') as f:
        f.write(test_input_data)
    data = reader.read(input_file, form='')
    os.remove(input_file)
    assert_frame_equal(data, expected_clean)


@with_setup(setup)
def test_read_raw():
    input_file = 'test.tsv'
    with open(input_file, 'wt') as f:
        f.write(test_input_data)
    raw = reader.read_raw(input_file)
    os.remove(input_file)
    assert_frame_equal(raw, expected_raw)


@with_setup(setup)
def test_read_raw_compressed():
    input_file = 'test.tsv.gz'
    with gzip.open(input_file, 'wt') as g:
        g.write(test_input_data)
    raw = reader.read_raw(input_file)
    os.remove(input_file)
    assert_frame_equal(raw, expected_raw)


@with_setup(setup)
def test_clean_data():
    result = reader.clean_data(expected_raw)
    assert_frame_equal(
        result,
        expected_clean)


def test_clean_field():
    fields = ['123', '456.7', '890 p', ':', ': ', ': p']
    expected = [123.0, 456.7, 890.0, np.NaN, np.NaN, np.NaN]
    result = [reader.clean_field(f) for f in fields]
    for r, e in zip(result, expected):
        if np.isnan(r):
            assert np.isnan(r) and np.isnan(e)
        else:
            assert np.isclose(r, e)


@with_setup(setup)
def test_structure():
    print(expected_clean)
    result = reader.structure(expected_clean)
    assert_frame_equal(
        result,
        expected_structured)


@with_setup(setup)
@raises(ValueError)
def test_structure_bad_column():
    expected_clean_bad_column = expected_clean.copy()
    column_names = list(expected_clean_bad_column.columns)
    column_names[0] = column_names[0] + '\\dummy'
    expected_clean_bad_column.columns = column_names
    result = reader.structure(expected_clean_bad_column)
    assert_frame_equal(
        result,
        expected_structured)


if __name__ == '__main__':
    import nose
    nose.runmodule()
