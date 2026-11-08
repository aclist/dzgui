from pathlib import Path

from dzgui.api.steam import get_local_signatures


def test_local_signatures_skip_malformed(tmp_path: Path) -> None:
    f = tmp_path / "dzg.versions"
    f.write_text("111,1000\n222,null\n333\n\n444,2000\n")
    assert get_local_signatures(f) == {"111": 1000, "444": 2000}
