import configparser
import pytest

from pathlib import Path

from dzgui.const.constants import FLATPAK_APPID, GTK_APP_ID, TMP_PATH
from dzgui.config.xdg import get_xdg_paths
from dzgui.util.flatpak import apply_overrides

PATHS_KEY = "Context"
PATHS_SUBKEY = "filesystems"
BUS_KEY = "Session Bus Policy"

pytestmark = pytest.mark.flatpak


@pytest.fixture
def xdg_paths() -> dict[str, Path]:
    return get_xdg_paths()


@pytest.fixture
def override(xdg_paths: dict[str, Path]) -> None:
    apply_overrides(xdg_paths)


@pytest.fixture
def config(xdg_paths: dict[str, Path]) -> configparser.ConfigParser:
    conf_path = xdg_paths["XDG_DATA_HOME"].parent.joinpath(
        f"flatpak/overrides/{FLATPAK_APPID}"
    )
    config = configparser.ConfigParser()
    config.read(conf_path)
    return config


def test_session_bus(override: None, config: configparser.ConfigParser) -> None:
    bus = config[BUS_KEY][GTK_APP_ID]
    assert bus == "own"


def test_paths(
    override: None, xdg_paths: dict[str, Path], config: configparser.ConfigParser
) -> None:
    expect: list[Path] = []
    expect.append(Path(TMP_PATH))
    expect.extend([*xdg_paths.values()])
    paths = config[PATHS_KEY][PATHS_SUBKEY].split(";")
    assert all(str(path) in paths for path in expect)
