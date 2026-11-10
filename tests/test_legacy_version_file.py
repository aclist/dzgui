from typing import TYPE_CHECKING

from dzgui.init.migrate import clean_legacy_versions_file

if TYPE_CHECKING:
    from pathlib import Path


def test_null_signature_stripping(tmp_path: "Path") -> None:
    tmp = tmp_path.joinpath("dzg.versions")
    lines = [
        "1111,2222",
        "3333,4444",
        "5555,null",
        "foo",
        ",4555",
        "1111",
        " ",
        ",,,",
        "-1",
    ]
    expect = ["1111,2222", "3333,4444"]
    tmp.write_text("\n".join(lines))
    clean_legacy_versions_file(tmp)
    assert expect == tmp.read_text().splitlines()
