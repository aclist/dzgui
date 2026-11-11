import pytest
import tempfile


from _pytest.monkeypatch import MonkeyPatch
from collections.abc import Iterator
from pathlib import Path
from typing import Any, cast, TYPE_CHECKING

from dzgui.api.shortcuts import Shortcuts
from tests.fixtures import fixture_path

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch

pytestmark = pytest.mark.apitest


def mock_find_shortcuts(self: Shortcuts, steam_path: Path) -> Path:
    return Path(fixture_path("api/no_shortcuts.vdf"))


@pytest.fixture(scope="module", autouse=True)
def patch_api() -> Iterator[None]:
    mp = MonkeyPatch()
    mp.setattr("dzgui.api.shortcuts.Shortcuts.find_shortcuts_path", mock_find_shortcuts)
    yield
    mp.undo()


def test_no_shortcuts(monkeypatch: "MonkeyPatch") -> None:
    s = Shortcuts(Path(""))
    assert len(s.shortcuts["shortcuts"]) == 0


@pytest.fixture
def dummy_app() -> dict[str, Any]:
    d = {
        "AppName": "TEST APP",
        "StartDir": Path("TEST_DIR"),
        "Exe": Path("TEST_DIR/TEST_EXE.EXE"),
        "icon": Path("IMAGES_DIR/TEST_IMAGE.PNG"),
    }
    return d


@pytest.fixture
def shortcuts(dummy_app: dict[str, Any]) -> Shortcuts:
    s = Shortcuts(Path(""))
    args = cast(tuple[str, Path, Path, Path], dummy_app.values())
    s.add_shortcut(*args)
    return s


def test_wrap_exe(shortcuts: Shortcuts) -> None:
    assert shortcuts.shortcuts["shortcuts"]["0"]["Exe"][0] == '"'
    assert shortcuts.shortcuts["shortcuts"]["0"]["Exe"][-1] == '"'


def test_add_shortcut(shortcuts: Shortcuts, dummy_app: dict[str, Any]) -> None:
    new = shortcuts.shortcuts["shortcuts"]
    ind = str(len(new) - 1)
    for k, v in dummy_app.items():
        if k == "Exe":
            v = f'"{v}"'
        assert new[ind][k] == str(v)


def test_save_shortcut(shortcuts: Shortcuts) -> None:
    with tempfile.NamedTemporaryFile() as f:
        tmp = Path(f.name)
        shortcuts.shortcuts_path = tmp
        shortcuts.save_shortcuts()
        shortcuts._load_shortcuts(tmp)
        assert len(shortcuts.shortcuts["shortcuts"]) == 1


def test_shortcut_crc(shortcuts: Shortcuts) -> None:
    for key in shortcuts.shortcuts["shortcuts"].keys():
        entry = shortcuts.shortcuts["shortcuts"][key]
        name = entry["AppName"]
        exe = entry["Exe"]
        uid = name + exe
        bpid = shortcuts.gen_bpid(uid)
        assert entry["appid"] & 0xFFFFFFFF == bpid


def test_reverse_crc(shortcuts: Shortcuts) -> None:
    for key in shortcuts.shortcuts["shortcuts"].keys():
        entry = shortcuts.shortcuts["shortcuts"][key]
        name = entry["AppName"]
        exe = entry["Exe"]
        uid = name + exe
        bpid = shortcuts.gen_bpid(uid)
        assert shortcuts.find_appname_by_unsigned_id(bpid) == name
