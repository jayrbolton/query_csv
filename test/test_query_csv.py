import pytest
import query_csv

_PATH = 'test/data/test.csv'
_GZPATH = 'test/data/test.csv.gz'
_EMPTY_PATH = 'test/data/empty.csv'
_BAD_EXT = 'test/data/test.txt'


def test_iter_csv_rows_ok():
    """Test happy path for iter_csv_rows"""
    rows = query_csv.iter_csv_rows(_PATH, delim=' ')
    assert list(rows) == [
        {'s': 'a', 'i': 1, 'f': 1.0},
        {'s': 'b', 'i': 2, 'f': 2.0},
        {'s': 'c', 'i': 3, 'f': 3.0},
    ]


def test_iter_csv_rows_gzipped_ok():
    """Test happy path for iter_csv_rows (with gzipped file)"""
    rows = query_csv.iter_csv_rows(_GZPATH, delim=' ')
    assert list(rows) == [
        {'s': 'a', 'i': 1, 'f': 1.0},
        {'s': 'b', 'i': 2, 'f': 2.0},
        {'s': 'c', 'i': 3, 'f': 3.0},
    ]


def test_filter_rows_ok():
    """Test happy path for filter_rows"""
    rows = query_csv.iter_csv_rows(_PATH, delim=' ')
    filtered = query_csv.filter_rows(rows, {'i': 2, 'f': 2.0})
    assert list(filtered) == [
        {'s': 'b', 'i': 2, 'f': 2.0}
    ]


def test_filter_rows_overfit():
    """Test overfit condition for filter_rows"""
    rows = query_csv.iter_csv_rows(_PATH, delim=' ')
    where = {'i': 2, 'f': 2.0, 's': 'b', 'x': 'hi'}
    filtered = query_csv.filter_rows(rows, where)
    assert list(filtered) == []


def test_filter_rows_empty_dict():
    """Test empty dict provided for filter_rows"""
    rows = query_csv.iter_csv_rows(_PATH, delim=' ')
    filtered = query_csv.filter_rows(rows, {})
    assert list(filtered) == [
        {'s': 'a', 'i': 1, 'f': 1.0},
        {'s': 'b', 'i': 2, 'f': 2.0},
        {'s': 'c', 'i': 3, 'f': 3.0},
    ]


def test_filter_rows_list_input():
    """Test plain list provided for rows"""
    ls = [
        {'s': 'a', 'i': 1, 'f': 1.0},
        {'s': 'b', 'i': 2, 'f': 2.0},
        {'s': 'c', 'i': 3, 'f': 3.0},
    ]
    filtered = query_csv.filter_rows(ls, {'s': 'a'})
    assert list(filtered) == [
        {'s': 'a', 'i': 1, 'f': 1.0},
    ]


def test_sum_columns():
    """Test happy path for sum_columns"""
    rows = query_csv.iter_csv_rows(_PATH, delim=' ')
    _sum = query_csv.sum_columns(rows, ['i', 'f'])
    assert _sum == 12.0


def test_sum_columns_empty():
    """Test sum on empty columns"""
    rows = query_csv.iter_csv_rows(_PATH, delim=' ')
    _sum = query_csv.sum_columns(rows, [])
    assert _sum == 0.0


def test_invalid_csv_extension():
    """Test the case where we provide a file with a bad extension"""
    with pytest.raises(query_csv.exceptions.InvalidFileError) as ctx:
        list(query_csv.iter_csv_rows(_BAD_EXT))
    expected = "File extension must be '.csv' or '.csv.gz'; it is '.txt'"
    assert str(ctx.value) == expected


def test_nonexistent_file():
    """Test the case where we provide a nonexistent file path"""
    with pytest.raises(query_csv.exceptions.InvalidFileError) as ctx:
        list(query_csv.iter_csv_rows('nonexistent.csv'))
    expected = "File does not exist: nonexistent.csv"
    assert str(ctx.value) == expected


def test_empty_file():
    """Test the case where we provide an empty file"""
    with pytest.raises(query_csv.exceptions.InvalidFileError) as ctx:
        list(query_csv.iter_csv_rows(_EMPTY_PATH))
    expected = "CSV is empty"
    assert str(ctx.value) == expected


def test_sum_non_numeric():
    """Test the case where we try to sum non-numeric columns"""
    rows = query_csv.iter_csv_rows(_PATH, delim=' ')
    with pytest.raises(TypeError):
        query_csv.sum_columns(rows, ['i', 's'])
