"""
Functions to search, filter, and aggregate a CSV document.

See README.md for details

Uses Google Style Python docstrings:
    https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
"""
import os
from typing import Generator, List

import query_csv.utils as utils
from query_csv.exceptions import InvalidFileError

# Generator of CSV rows created by iter_csv_rows
Rows = Generator[dict, None, None]


def iter_csv_rows(csv_path: str, delim: str = ',') -> Rows:
    """
    Yield rows of a CSV document as dictionaries where each key is a header
    name and each value is a column value.
    Automatically parses numeric values into integers or floats.
    Args:
        csv_path: file path to a CSV file (can be gzipped)
        delimiter
    Yields:
        dictionary where the keys are header names and values are column values
    Raises:
        InvalidFileError if path nonexistent or file has incorrect extension
    Examples:
        rows = iter_csv_rows('/filepath.csv.gz')
        for row in rows:
            ...
    """
    if not os.path.isfile(csv_path):
        raise InvalidFileError(f"File does not exist: {csv_path}")
    ext = utils.get_extension(csv_path)
    if ext != '.csv' and ext != '.csv.gz':
        msg = f"File extension must be '.csv' or '.csv.gz'; it is '{ext}'"
        raise InvalidFileError(msg)
    if ext == '.csv.gz':
        # Extract a gzipped file; `rows` is a generator
        rows = utils.iter_gzip_csv_rows(csv_path, delim)
    else:
        # Open the csv; `rows` is a generator
        rows = utils.iter_csv_rows(csv_path, delim)
    try:
        headers = next(rows)  # Gets first row
    except StopIteration:
        raise InvalidFileError("CSV is empty")
    for each_row in rows:
        ret = {}
        for (idx, header_name) in enumerate(headers):
            # Converts numeric columns into ints or floats
            val = utils.convert_col_type(each_row[idx])
            ret[header_name] = val
        yield ret


def filter_rows(rows: Rows, columns: dict) -> Rows:
    """
    Generate rows for a given CSV document where column values all match the
    values given in `columns`.
    Args:
        rows: Iterable collection of row dictionaries (for example, the output
            of iter_csv_rows)
        columns: keys are column names (based on the headers), and values are
            column values to filter based on exact match. The match is based on
            an AND conjuction, so all columns in the row must match *all*
            values in `columns`.
    Yields:
        dicts where the keys are header names and values are column values
    Examples:
        rows = iter_csv_rows(mypath, delim='\t')
        filtered = filter_rows(rows, {'colx': 'x', 'coly': 'y'})
    """
    for row in rows:
        # Check if all keys/vals exist in and match those in row
        if utils.dict_is_subset(columns, row):
            yield row


def sum_columns(rows: Rows, columns: List[str]) -> float:
    """
    Sum numeric columns over a set of rows.
    Args:
        csv_path: file path to a CSV file (can be gzipped)
    Returns:
        A float value representing the sum of all given
        columns in all rows in the CSV
    Raises:
        TypeError if any column value is not an int or float
    Examples:
        sum_columns(iter_csv_rows(csv_path), ['colx', 'coly']) -> 123.456
    """
    _sum = 0.0  # `sum` is a builtin
    for row in rows:
        for col_name in columns:
            val = row[col_name]
            if not isinstance(val, int) and not isinstance(val, float):
                msg = (
                    f"Trying to sum column '{col_name}', "
                    "which must be an int or float; "
                    f"it is a {type(val)} with value {val}"
                )
                raise TypeError(msg)
            _sum += val
    return _sum
