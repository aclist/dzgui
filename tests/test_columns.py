import pytest

from typing import TYPE_CHECKING

from dzgui.init.migrate import convert_cols_file
from tests.fixtures import fixture_path

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def columns_with_perspective() -> "Path":
    return fixture_path("columns_1")


@pytest.fixture
def columns_without_perspective() -> "Path":
    return fixture_path("columns_2")


@pytest.fixture
def columns_with_view() -> "Path":
    return fixture_path("columns_3")


@pytest.mark.config
def test_columns_with_perspective(columns_with_perspective: "Path") -> None:
    j = convert_cols_file(columns_with_perspective)
    if j is None:
        return
    assert "View" in j["cols"]
    assert "Max" in j["cols"]


@pytest.mark.config
def test_columns_without_perspective(columns_without_perspective: "Path") -> None:
    j = convert_cols_file(columns_without_perspective)
    if j is None:
        return
    assert "View" not in j["cols"]
    assert "Max" not in j["cols"]


@pytest.mark.config
def test_columns_with_view(columns_with_view: "Path") -> None:
    j = convert_cols_file(columns_with_view)
    assert j is None
