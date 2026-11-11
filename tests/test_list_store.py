import pytest

from typing import Any

from dzgui.model.model_factory import FastInsertListStore


@pytest.fixture
def heterogeneous_list() -> list[list[Any]]:
    return [["a", 0, True], ["b", 1, False]]


@pytest.fixture
def mismatched_length_list() -> list[list[Any]]:
    return [["a", 0, True], ["b", 1, False, 0]]


@pytest.fixture
def extended_list(heterogeneous_list: list[list[Any]]) -> FastInsertListStore:
    fs = FastInsertListStore(str, int, bool)
    fs.extend(heterogeneous_list)
    return fs


@pytest.fixture
def appended_list(heterogeneous_list: list[list[Any]]) -> FastInsertListStore:
    fs = FastInsertListStore(str, int, bool)
    for row in heterogeneous_list:
        fs.append(row)
    return fs


@pytest.mark.parametrize("target", ["extended_list", "appended_list"])
def test_list_parity(
    heterogeneous_list: list[list[Any]], request: pytest.FixtureRequest, target: str
) -> None:
    target = request.getfixturevalue(target)
    extracted = [[el for el in row] for row in target]
    assert heterogeneous_list == extracted


def test_type_disparity(heterogeneous_list: list[list[Any]]) -> None:
    with pytest.raises(TypeError):
        fs = FastInsertListStore(str, bool, bool)
        fs.extend(heterogeneous_list)


def test_length_disparity(mismatched_length_list: list[list[Any]]) -> None:
    with pytest.raises(ValueError):
        fs = FastInsertListStore(str, int, bool)
        fs.extend(mismatched_length_list)
