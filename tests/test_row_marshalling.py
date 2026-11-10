from dzgui.model.model_factory import ModelFactory
from dzgui.model.proxy_model import ServerRow


def test_row_conversion() -> None:
    """Converted FastInsertListStore is expected to have identical elements"""
    data = [
        "Test Server",
        "chernarusplus",
        "1PP",
        "05:00",
        10,
        10,
        0,
        "127.0.0.0:27016",
        27017,
        99,
        "Unofficial",
        False,
    ]
    rows = [ServerRow(*data)]
    marshalled = ServerRow.marshal_rows(rows)
    store = ModelFactory().make_server_store()
    store.extend(marshalled)
    converted = [[el for el in row] for row in store]
    assert data == converted[0]
