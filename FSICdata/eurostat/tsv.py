# -*- coding: utf-8 -*-
"""
tsv
===
Module to handle Eurostat bulk-download TSV files.

"""


import numpy as np
import pandas as pd


def read(path, clean=True, form='structured'):
    """Return the contents of `path` as a pandas DataFrame object.

    Parameters
    ==========
    path : string
        Path to input data file
    clean : boolean
        If `True`, apply further cleaning procedures to the raw data
    form : string
        Depending on the value, reshape the contents of the DataFrame before
        returning

    Returns
    =======
    data : pandas DataFrame
        Processed contents of `path`

    """
    # Read raw data
    data = read_raw(path)
    # Clean, if required
    if clean:
        data = clean_data(data)
    # Restructure, if required
    if form == 'structured':
        data = structure(data)
    elif form == 'raw':
        pass
    else:
        raise ValueError('Unrecognised `form` argument: %s' % form)
    # Return
    return data


def read_raw(path):
    """Return the contents of `path`.

    Parameters
    ==========
    path : string
        Input data file (may be compressed)

    Returns
    =======
    data : pandas DataFrame
        Contents of `path`

    """
    # Set compression type
    if path.endswith('.gz'):
        compression = 'gzip'
    else:
        compression = None
    # Read
    data = pd.read_csv(
        path,
        sep=r' *[,\t]',
        skipinitialspace=True,
        compression=compression,
        index_col=False,
        na_values=[':', ': '],
        engine='python')
    # Return
    return data


def clean_data(data):
    """Return a cleaned version of `data`.

    Parameters
    ==========
    data : pandas DataFrame
        Data to clean

    Returns
    =======
    data : pandas DataFrame
        Cleaned version of `data`

    """
    return data.apply(
        lambda x: x.apply(clean_field))


def clean_field(field):
    """Return a cleaned version of field.

    Parameters
    ==========
    field : numeric or string
        DataFrame cell to clean

    Returns
    =======
    field : numeric
        Cleaned DataFrame cell

    Notes
    =====

    In most cases, pandas will correctly read the contents of a Eurostat TSV
    data file. Columns that only contain standard numeric fields and ':'
    (missing values) are already converted by `read_raw()`.

    The exception to this is any column containing a field accompanied by
    metadata e.g. '890 p' or ': p'. The numeric/missing value always comes
    first, followed by a space, and then a series of characters indicating other
    attributes of that data point. In the example, 'p' indicates a provisional
    value.

    This function extracts the numeric value only.

    """
    try:
        field = field.split(' ')[0]
        if field.strip() == ':':
            field = np.NaN
        field = np.float64(field)
    except:
        pass
    return field


def structure(data):
    """Return a structured-form version of `data`.

    Parameters
    ==========
    data : pandas DataFrame
        Raw form of input data

    Return
    ======
    data : pandas DataFrame
        Melted (structured) version of `data`

    """
    # Extract column names and locate rightmost identifier column
    var_list = list(data.columns)
    last_id_loc = [i for i, e in enumerate(var_list) if '\\' in e]
    if len(last_id_loc) != 1:
        raise ValueError('Expected just one index when searching for final '
                         'identifer column')
    last_id_loc = last_id_loc[0]
    # Extract identifiers only and split final identifier in two
    id_vars = list(var_list[:last_id_loc + 1])
    id_vars[-1], var_name = id_vars[-1].split('\\')
    # Overwrite identifier column names in `data`
    var_list[last_id_loc] = id_vars[-1]
    data.columns = var_list
    # Melt and return
    data = pd.melt(
        data,
        id_vars=id_vars,
        var_name=var_name)
    return data
