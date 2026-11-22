import pytest
import tempfile

from pathlib import Path
from typing import TYPE_CHECKING

from dzgui.api.steam import get_steam_paths

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch


def test_custom_xdg_path(monkeypatch: "MonkeyPatch") -> None:
    tmp = tempfile.TemporaryDirectory(delete=False).name
    custom_path = Path(tmp).joinpath("xdg_data_home")
    monkeypatch.setenv("XDG_DATA_HOME", str(custom_path))

    vdf_path = custom_path.joinpath("Steam/steamapps")
    vdf_path.mkdir(parents=True, exist_ok=True)
    vdf_path.joinpath("libraryfolders.vdf").touch()

    resolved_paths = get_steam_paths()
    expect = custom_path.joinpath("Steam")
    assert any(expect in el for el in resolved_paths)


def test_default_xdg_path() -> None:
    resolved_paths = get_steam_paths()
    expect = Path.home().joinpath(".local/share/Steam")
    assert any(expect in el for el in resolved_paths)


def test_ubuntu_path() -> None:
    resolved_paths = get_steam_paths()
    expect = Path.home().joinpath(".steam/steam")
    assert any(expect in el for el in resolved_paths)


@pytest.mark.flatpak
def test_flatpak_path() -> None:
    resolved_paths = get_steam_paths()
    expect = Path.home().joinpath(".var/app/com.valvesoftware.Steam/data/steam")
    assert any(expect in el for el in resolved_paths)
