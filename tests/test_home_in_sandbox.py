import pytest
import tempfile

from pathlib import Path
from typing import TYPE_CHECKING

from dzgui.config.xdg import get_xdg_paths

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch


@pytest.mark.parametrize("env", ["SNAP_REAL_HOME", "HOME"])
def test_sandbox_home_resolution(monkeypatch: "MonkeyPatch", env: str) -> None:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        monkeypatch.setenv(env, f.name)
        paths = get_xdg_paths()
        assert paths["XDG_CONFIG_HOME"] == Path(f.name).joinpath(".config/dzgui")


def test_home_fallback() -> None:
    paths = get_xdg_paths()
    assert paths["XDG_CONFIG_HOME"] == Path.home().joinpath(".config/dzgui")
