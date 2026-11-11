import pytest
from pathlib import Path
from typing import TYPE_CHECKING

from dzgui.api.steam import is_dayz_downloading

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch


@pytest.mark.parametrize(
    "file_list, expect",
    [
        (["state_221100_1111.patch"], True),
        (["state_730_1111.patch"], False),
        (["state_1024020_1111.patch"], True),
        (["221100"], False),
        (["221100", "state_221100_1111.patch"], True),
        (["state_221100_1111.patch", "state_1024020_1111.patch"], True),
        (["state_221100_1111"], False),
    ],
)
def test_dayz_patch_pending(
    monkeypatch: "MonkeyPatch", file_list: list[str], expect: bool
) -> None:
    def mock_get_pending_downloads(steam_path: Path, appid: int) -> list[Path]:
        files = [Path(file) for file in file_list]
        return files

    monkeypatch.setattr(
        "dzgui.api.steam.get_pending_downloads", mock_get_pending_downloads
    )
    assert is_dayz_downloading(Path("/tmp"), 221100) == expect
