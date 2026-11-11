import pytest

from typing import Any, TYPE_CHECKING

from dzgui.api import probe
from dzgui.config.query import get_config
from dzgui.config.xdg import get_xdg_paths, parse_filepaths

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.webtest


@pytest.fixture
def config() -> Any:
    paths = get_xdg_paths()
    xdg = parse_filepaths(paths)
    return get_config(xdg.config)


def test_ipdb() -> None:
    assert probe.test_ipdb()


def test_steam(config: Any) -> None:
    key = config["steam_api"]
    assert probe.test_steam_api(key)
