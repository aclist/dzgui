from typing import TYPE_CHECKING

from dzgui.util import localize

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch


def test_de(monkeypatch: "MonkeyPatch") -> None:
    monkeypatch.setenv("LC_ALL", "de_DE.UTF-8")
    localize.set_locale()
    assert localize.number(9900) == "9.900"
    assert localize.number(99.88) == "99,88"


def test_en(monkeypatch: "MonkeyPatch") -> None:
    monkeypatch.setenv("LC_ALL", "en_US.UTF-8")
    localize.set_locale()
    assert localize.number(9900) == "9,900"
    assert localize.number(99.88) == "99.88"


def test_none(monkeypatch: "MonkeyPatch") -> None:
    localize.set_locale()
    assert localize.number(9900) == "9,900"
    assert localize.number(99.88) == "99.88"


def test_empty(monkeypatch: "MonkeyPatch") -> None:
    monkeypatch.setenv("LC_ALL", "")
    localize.set_locale()
    assert localize.number(9900) == "9,900"
    assert localize.number(99.88) == "99.88"
