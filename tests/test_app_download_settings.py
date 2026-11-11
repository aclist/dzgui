import pytest

from _pytest.monkeypatch import MonkeyPatch
from collections.abc import Iterator
from pathlib import Path

from dzgui.api.steam import get_app_allows_downloads, get_last_updated
from tests.fixtures import fixture_path

pytestmark = pytest.mark.apitest


def mock_path(p: Path, appid: int) -> Path:
    return Path(fixture_path("api"))


def mock_config_allows(p: Path) -> Path:
    return Path(fixture_path("api/client_allows_downloads.vdf"))


def mock_config_disallows(p: Path) -> Path:
    return Path(fixture_path("api/client_disallows_downloads.vdf"))


def mock_config_missing(p: Path) -> Path:
    return Path(fixture_path(""))


@pytest.fixture
def client_allows() -> Path:
    return Path(fixture_path("api/client_allows_downloads.vdf"))


@pytest.fixture
def steam_path() -> Path:
    return Path(fixture_path("api"))


@pytest.fixture(scope="module", autouse=True)
def patch_api() -> Iterator[None]:
    mp = MonkeyPatch()
    mp.setattr("dzgui.api.steam.get_app_path", mock_path)
    yield
    mp.undo()


def test_no_last_update(steam_path: Path) -> None:
    assert get_last_updated(steam_path, 555) is None


def test_last_update(steam_path: Path) -> None:
    assert get_last_updated(steam_path, 444) == "2026-10-22 00:09:33"


def test_app_allows_downloads(steam_path: Path) -> None:
    assert get_app_allows_downloads(steam_path, 111) is True


def test_app_disallows_downloads(steam_path: Path) -> None:
    assert get_app_allows_downloads(steam_path, 222) is False


def test_app_delegates_downloads(
    monkeypatch: MonkeyPatch, steam_path: Path, client_allows: Path
) -> None:
    monkeypatch.setattr("dzgui.api.steam.get_config", mock_config_disallows)
    assert get_app_allows_downloads(steam_path, 333) is False
    monkeypatch.setattr("dzgui.api.steam.get_config", mock_config_allows)
    assert get_app_allows_downloads(steam_path, 333) is True
    monkeypatch.setattr("dzgui.api.steam.get_config", mock_config_missing)
    assert get_app_allows_downloads(steam_path, 333) is True
