import pytest
import vdf  # type: ignore[import-untyped]

from pathlib import Path

from dzgui.api.mods import get_local_mod_ids
from dzgui.util.dirs import make_parents
from tests.fixtures import fixture_path


@pytest.fixture
def libraryfolders() -> Path:
    return fixture_path("api/steamapps/libraryfolders.vdf")


def test_missing_mod_dir(tmp_path: Path, libraryfolders: Path) -> None:
    """
    Updates fixture file key with tmp path value serializes to file,
    then tests for missing mod directory returning an empty list
    """
    folders = tmp_path.joinpath("steamapps/libraryfolders.vdf")
    workshop = tmp_path.joinpath("steamapps/workshop/content")
    make_parents(folders)
    make_parents(workshop, descend=True)

    with open(libraryfolders, "r") as f:
        data = vdf.load(f)
    data["libraryfolders"]["0"]["path"] = tmp_path
    with open(folders, "w") as f:
        vdf.dump(data, f, pretty=True)
    ids = get_local_mod_ids(tmp_path)
    assert len(ids) == 0
