import pytest

from typing import Any, TYPE_CHECKING

from dzgui.const.constants import FLATPAK_RUN_CMD, STEAM_CMD
from dzgui.controllers.mc import Controller

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch


@pytest.mark.parametrize(
    "value, expected", [(FLATPAK_RUN_CMD, "Flatpak"), (STEAM_CMD, "Steam")]
)
def test_human_name(monkeypatch: "MonkeyPatch", value: str, expected: str) -> None:
    def mock_query_config(*args: Any) -> str:
        return value

    monkeypatch.setattr(
        "dzgui.controllers.mc.Controller.query_config", mock_query_config
    )
    controller = Controller()
    client = controller.get_client_name()
    assert client == expected
