"""
ons
===
Python module to read ONS datafiles.

"""


from pandas import DataFrame
import pandas as pd


def read_csv(filepath, *args, index_col=0, return_meta=False, stride=5, **kwargs):
    """Read ONS CSV data to a `Pandas` `DataFrame`. Optionally return metadata.

    Parameters
    ----------
    filepath : path to CSV file
    index_col : integer
        Passed to `read_csv()` to identify the index column
    return_meta : boolean
        If `False`, just return the data. If `True`, return the data and the
        metadata as a tuple of `DataFrame` objects
    stride : integer


    Returns
    -------
    If `return_meta` is `False`:
        data : DataFrame
            CSV data

    If `return_meta` is `True`: (data, meta), where `data` is as above and
    `meta` is a DataFrame containing the metadata to accompany the dataset

    """
    # Empty class to store raw metadata content
    class Meta(object):
        pass
    raw_meta = Meta()

    # Reader class to pass to `pandas` `read_csv()`
    class Reader(object):
        def __init__(self, filepath):
            self.buffer = self.iter(filepath)
        # Line-by-line file generator
        def iter(self, filepath):
            with open(filepath, 'rt', newline='') as f:
                for line in f:
                    if len(line.strip()) > 0:
                        yield line
                    else:       # If line is empty, read raw metadata
                        f.readline()
                        f.readline()
                        raw_meta.text = f.read()
                        raise StopIteration
        # Read method for `pandas` `read_csv()`
        def read(self, n=0):
            try:
                return next(self.buffer)
            except StopIteration:
                return ''

    # Read CSV data
    data = pd.read_csv(Reader(filepath), *args, index_col=index_col, **kwargs)
    if not return_meta:
        return data
    # Optionally read metadata and return alongside `data`
    meta = read_meta(raw_meta.text, stride)
    return data, meta

def read_meta(raw_text, stride=5):
    lines = raw_text.splitlines()
    meta_dict = {}
    for pos in range(0, len(lines), stride):
        heading = lines[pos]
        code, desc = heading.split(',', maxsplit=1)
        entry = {'description': desc[1:-1]}
        for item in lines[pos + 1:pos + stride]:
            key, value = item[1:].split('=', maxsplit=1)
            entry[key] = value[1:-1]
        meta_dict[code] = entry
    return DataFrame(meta_dict)
