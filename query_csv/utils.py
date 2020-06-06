import gzip
import shutil
import tempfile
import csv
import os
from typing import Union, List, Generator

# yielded by the CSV parsers below. Generator of lists of column values for
# every row in a CSV
Rows = Generator[List[str], None, None]


def convert_col_type(val: str) -> Union[str, float, int]:
    """
    Convert a CSV column into an integer, a float, or keep as a string based on
    its format.
    Args:
        val: column value
    Returns:
        Int if numeric without decimal, float if numeric with decimal, and
        string otherwise
    Examples:
        "hi" -> "hi"
        "10" -> 10 (int)
        "10.0" -> 10.0 (float)
    """
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val


def iter_csv_rows(path: str, delim: str) -> Rows:
    """
    Only loads one row at a time into memory and yields it.
    Args:
        path: path to a .csv file
        delim: string column delimiter
    Yields:
        List of string values for every column.
    """
    with open(path) as fd:
        reader = csv.reader(fd, delimiter=delim)
        for row in reader:
            yield row


def iter_gzip_csv_rows(path: str, delim: str) -> Rows:
    """
    Args:
        path: path to a .csv.gz file
        delim: string column delimiter
    Yields:
        List of string values for every column.
    """
    # Decompress the gzip contents into a tempfile without loading into memory
    with gzip.open(path, 'rb') as fdout:
        with tempfile.NamedTemporaryFile('w+b') as fdin:
            # Copies by chunks
            shutil.copyfileobj(fdout, fdin)
            # Flush buffer to disk
            fdin.flush()
            for row in iter_csv_rows(fdin.name, delim):
                yield row
    # Tempfile delete at end of context


def dict_is_subset(subset: dict, superset: dict) -> bool:
    """
    Check that all keys in `subset` are present in `superset` and have all the
    same values by `==`.
    Args:
        subset: All keys and values in the dict must match those in `superset`
        superset: Must contain all keys/vals from subset
    Returns:
        boolean result
    Examples:
        dict_is_subset({'x': 1}, {'x': 1, 'y': 2}) -> True
        dict_is_subset({'x': 1, 'z': 2}, {'x': 1, 'y': 2}) -> False
    """
    return all(
        key in superset and superset[key] == subset[key]
        for key in subset.keys()
    )


def get_extension(path):
    """
    Get the file extension of a given path. Returns double extensions, such as
    '.csv.gz'
    """
    (name, ext) = os.path.splitext(path)
    (_, subext) = os.path.splitext(name)
    # Get the double extension as '.csv.gz'
    # `subext` will be '' if not present
    ext = subext + ext
    return ext
