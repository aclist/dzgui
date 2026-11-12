import pytest

from typing import Literal, TYPE_CHECKING

from dzgui.const.constants import (
    FLATPAK_APPID,
    FLATPAK_ROOT_PATH,
)
from dzgui.init import proc

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch

pytestmark = pytest.mark.flatpak


def mock_has_cmd(cmd: str) -> Literal[True]:
    return True


def mock_has_not_cmd(cmd: str) -> Literal[False]:
    return False


def mock_get_flatpak_output() -> list[str]:
    lines = ["Application", "com.freedesktop.Platform", f"{FLATPAK_APPID}"]
    return lines


@pytest.mark.parametrize(
    "output, expected",
    [
        (
            [
                [f"/home/user/{FLATPAK_ROOT_PATH}/.local/share/Steam"],
                ["/home/user/.local/share/Steam/ubuntu12_64/steamwebhelper"],
            ],
            True,
        ),
        (
            [
                [f"/home/user/{FLATPAK_ROOT_PATH}/.local/share/Steam"],
                ["steam-runtime-launcher-service"],
            ],
            False,
        ),
        ([[f"/home/user/{FLATPAK_ROOT_PATH}/.local/share/Steam"]], False),
        ([["/home/user/.local/share/Steam/ubuntu12_64/steamwebhelper"]], True),
        (
            [
                ["/home/user/.local/share/Steam/ubuntu12_64/steamwebhelper"],
                ["steam-runtime-launcher-service"],
            ],
            True,
        ),
    ],
)
def test_native_steam_running(
    monkeypatch: "MonkeyPatch", output: list[list[str]], expected: bool
) -> None:
    def mock_get_steam_procs() -> list[list[str]]:
        return output

    monkeypatch.setattr("dzgui.init.proc.has_cmd", mock_has_cmd)
    monkeypatch.setattr("dzgui.init.proc.get_steam_procs", mock_get_steam_procs)
    assert proc.is_native_steam_running() == expected


def test_flatpak_running(monkeypatch: "MonkeyPatch") -> None:
    monkeypatch.setattr("dzgui.init.proc.has_cmd", mock_has_cmd)
    monkeypatch.setattr("dzgui.init.proc.get_flatpak_output", mock_get_flatpak_output)
    assert proc.is_flatpak_steam_running()


def test_flatpak_sandboxed(monkeypatch: "MonkeyPatch") -> None:
    monkeypatch.setattr("dzgui.init.proc.has_cmd", mock_has_not_cmd)
    monkeypatch.setenv("FLATPAK_ID", FLATPAK_APPID)
    assert proc.is_flatpak_steam_running()


def test_flatpak_not_installed(monkeypatch: "MonkeyPatch") -> None:
    monkeypatch.setattr("dzgui.init.proc.has_cmd", mock_has_not_cmd)
    assert not proc.is_flatpak_steam_running()


def test_steam_not_installed(monkeypatch: "MonkeyPatch") -> None:
    monkeypatch.setattr("dzgui.init.proc.has_cmd", mock_has_not_cmd)
    assert not proc.is_native_steam_running()


def test_invalid_client() -> None:
    with pytest.raises(TypeError):
        proc.is_steam_running("invalid-client")
