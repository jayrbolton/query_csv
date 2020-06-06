> **Note: this is only a code example and not a real library**

# query_csv

![](https://github.com/jayrbolton/query_csv/workflows/Run%20tests/badge.svg)
[![codecov](https://codecov.io/gh/jayrbolton/query_csv/branch/master/graph/badge.svg)](https://codecov.io/gh/jayrbolton/query_csv)

Functions to search, filter, and aggregate a CSV document.

## Installation

Use pip

```
pip install query_csv==0.1.0
```

> **Note: this is only a code example and is not published**

## Usage

### query_csv.iter_csv_rows(csv_path, delim=', ')

Yield rows of a CSV document as dictionaries where each key is a header
name and each value is a column value.

Automatically parses numeric values into integers or floats.

* csv_path: file path to a CSV file (can be gzipped)
* delim: column deliminiter to use for parsing (defaults to comma)

Yields: dictionary where the keys are header names and values are column values
Raises: `query_csv.exceptions.InvalidFileError` if path nonexistent or file has incorrect extension

```py
rows = iter_csv_rows('/filepath.csv.gz')
# Iterate over the rows:
for row in rows:
    print(row)

# Load all rows into a list in memory
rows = list(iter_csv_rows('/filepath.csv.gz'))
```

### query_csv.filter_rows(rows, columns)

Generate rows for a given CSV document where column values all match the
values given in `columns`.

Args:

* rows: Iterable collection of row dictionaries (for example, the output
    of iter_csv_rows)
* columns: keys are column names (based on the headers), and values are
    column values to filter based on exact match. The match is based on
    an AND conjuction, so all columns in the row must match *all*
    values in `columns`.

Yields: dicts where the keys are header names and values are column values

Examples:

```py
rows = iter_csv_rows(mypath, delim='\t')
filtered = filter_rows(rows, {'colx': 'x', 'coly': 'y'})
```

### query_csv.sum_columns(rows, columns)

Sum numeric columns over a set of rows.

Args:

* csv_path: file path to a CSV file (can be gzipped)

Returns: A float value representing the sum of all given
    columns in all rows in the CSV

Raises:
 * `TypeError` if any column value is not an int or float

Examples:
```py
sum_columns(iter_csv_rows(csv_path), ['colx', 'coly']) -> 123.456
```

## Development

### Setup and tests

With Python `^3.6`, install poetry with `pip install poetry`.

Install dependencies and virtualenv with `poetry install`

### Build & Publish

Run the following:

```
poetry build
poetry publish
```
