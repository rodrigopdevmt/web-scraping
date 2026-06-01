from src.staircase import create_staircase


def test_valid_staircase() -> None:
    result = create_staircase([1, 2, 3, 4, 5, 6])
    assert result == [[1], [2, 3], [4, 5, 6]]


def test_valid_staircase_ten() -> None:
    result = create_staircase([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert result == [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10]]


def test_invalid_staircase() -> None:
    result = create_staircase([1, 2, 3, 4, 5])
    assert result is None


def test_empty_list() -> None:
    result = create_staircase([])
    assert result == []


def test_single_element() -> None:
    result = create_staircase([42])
    assert result == [[42]]


def test_does_not_mutate_input() -> None:
    original = [1, 2, 3, 4, 5, 6]
    copy = list(original)
    create_staircase(original)
    assert original == copy
