import re

from dataclasses import dataclass, fields
from operator import attrgetter
from typing import TYPE_CHECKING, Union

from dzgui.const.enum import FilterMode
from dzgui.model.model_factory import ModelFactory
from dzgui.util import strings
from dzgui.strings import filters as str_filters

if TYPE_CHECKING:
    from dzgui.managers.filter import FilterManager
    from dzgui.model.model_factory import FastInsertListStore
    from dzgui.api.servers import Record
    from dzgui.model.servers import NewPlayerCount

DAY_REG = r"([0][6-9]|[1][0-7])"
NIGHT_REG = r"([0][0-5]|[1][8-9]|[2][0-3])"


@dataclass(slots=True, frozen=True)
class ServerRow:
    name: str
    mapname: str
    view: str
    time: str
    players: int
    max_players: int
    queue: int
    ip: str
    qport: int
    ping: str
    provider: str
    modded: bool

    # NOTE: construct getter once for fast lookup in lieu of field introspection
    _to_tuple = attrgetter(
        "name",
        "mapname",
        "view",
        "time",
        "players",
        "max_players",
        "queue",
        "ip",
        "qport",
        "ping",
        "provider",
        "modded",
    )

    # TODO: tests for marshalled row insertion
    @classmethod
    def marshal_rows(
        cls, rows: list["ServerRow"]
    ) -> list[tuple[str, str, str, str, int, int, int, str, int, str, str, bool]]:
        """Marshals data before passing into FastInsertListStore's extend() method"""
        getter = cls._to_tuple
        return [getter(row) for row in rows]


class FiltrationManager:
    def __init__(self) -> None:

        self.filter_map = {
            strings.filter_3pp: self.filter_3pp,
            strings.filter_1pp: self.filter_1pp,
            strings.filter_official: self.filter_official,
            strings.filter_unofficial: self.filter_unofficial,
            strings.filter_empty: self.filter_empty,
            strings.filter_full: self.filter_full,
            strings.filter_duplicate: self.filter_duplicate,
            strings.filter_day: self.filter_day,
            strings.filter_night: self.filter_night,
            strings.filter_nonascii: self.filter_nonascii,
            strings.filter_lowpop: self.filter_lowpop,
            strings.filter_modded: self.filter_modded,
            strings.filter_unmodded: self.filter_unmodded,
        }

    def filter_3pp(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if row.view != strings.filter_3pp]

    def filter_1pp(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if row.view != strings.filter_1pp]

    def filter_official(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if row.provider != strings.filter_official]

    def filter_unofficial(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if row.provider != strings.filter_unofficial]

    def filter_empty(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if row.players != 0]

    def filter_full(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if row.players != row.max_players]

    def filter_duplicate(self, rows: list[ServerRow]) -> list[ServerRow]:
        seen = set()
        final = []
        for row in rows:
            if row.name not in seen:
                seen.add(row.name)
                final.append(row)
        rows = final
        return rows

    def filter_day(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if not re.match(DAY_REG, row.time)]

    def filter_night(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if not re.match(NIGHT_REG, row.time)]

    def filter_nonascii(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if row.name.isascii()]

    def filter_lowpop(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if (row.players / row.max_players * 100) > 30]

    def filter_modded(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if not row.modded]

    def filter_unmodded(self, rows: list[ServerRow]) -> list[ServerRow]:
        return [row for row in rows if row.modded]

    def filter(self, filter_type: str, rows: list[ServerRow]) -> list[ServerRow]:
        func = self.filter_map[filter_type]
        return func(rows)


class ProxyModelManager:
    """
    Manages access to cached FastInsertListStore resources and
    performs filtering on behalf of atomic TreeViews,
    which share the same column structure.

    A ProxyModelManager is attached to each ServerTreeView.

    Raw data is cached before being packed into a FastInsertListStore, see get_control()
    Filtration creates a proxy of the TreeView's model, see get_proxy_model()
    """

    def __init__(self, filter_man: "FilterManager") -> None:
        self.filter_cache: dict[
            tuple[str, ...],
            list[ServerRow],
        ] = {}

        self.proxy_model: "FastInsertListStore"
        self.filter_man = filter_man
        self.filtration_manager = FiltrationManager()

        self.control_model: list[ServerRow] | None = None
        self.filtered: list[ServerRow] = []
        self.success = True

    def has_control_model(self) -> bool:
        if self.control_model is None:
            return False
        return True

    def append_row_to_control(self, row: ServerRow) -> None:
        if self.control_model is None:
            raise AttributeError("Trying to add rows to a non-existent model")
        self.control_model.append(row)
        self.filter(FilterMode.INITIAL, skip_cache=True)

    def update_playercount(self, playercount: "NewPlayerCount") -> None:
        treeiter = playercount.treeiter
        field = [f.name for f in fields(ServerRow)]
        index_players = field.index("players")
        index_queue = field.index("queue")
        self.proxy_model[treeiter][index_players] = playercount.players
        self.proxy_model[treeiter][index_queue] = playercount.queue

    def append_row_to_history(
        self,
        history: ServerRow,
    ) -> None:
        addr = history.ip
        qport = history.qport

        if self.control_model is None:
            raise AttributeError("Trying to append row to empty model")
        found = False
        for i, row in enumerate(self.control_model):
            if addr == row.ip and qport == row.qport:
                item = self.control_model.pop(i)
                self.control_model.append(item)
                found = True
                break

        if found is False:
            self.control_model.append(history)

        # NOTE: truncate history to 10 records max
        if len(self.control_model) == 11:
            del self.control_model[0]

        self.filter(FilterMode.INITIAL, skip_cache=True)

    def remove_row_from_control(self, record: "Record") -> None:
        if self.control_model is None:
            return
        addr = f"{record.ip}:{record.gameport}"
        qport = record.qport
        for row in self.control_model:
            if addr == row.ip and qport == row.qport:
                self.control_model.remove(row)
                break
        self.wipe_cache()
        self.filter(FilterMode.INITIAL, skip_cache=True)

    def clear_proxy_model(self) -> None:
        self.proxy_model.clear()

    def get_proxy_model(self) -> Union["FastInsertListStore", None]:
        if hasattr(self, "proxy_model"):
            return self.proxy_model
        return None

    def filter(
        self, mode: FilterMode, skip_cache: bool = False
    ) -> Union["FastInsertListStore", None]:
        """
        Native Gtk.TreeView.refilter() method was not performant enough
        when running in the main loop with 40k+ records

        skip_cache: used when updating a record on Saved Servers/History and forcing a refilter

        NOTE: data must be marshalled from ServerRow format before constructing list stores
        The "clone" is the proxy model (list of tuples) actually fed into Gtk.TreeView
        """
        # TODO: filter cache: return a dataclass object with clearly enumerated map, keyword, and filter values
        # instead of just a serial list of strings
        filters = self.filter_man.get_all_filters()

        if skip_cache is False:
            if filters in self.filter_cache:
                cached_rows = self.filter_cache[filters]
                marshalled_rows = ServerRow.marshal_rows(cached_rows)
                clone = ModelFactory().make_server_store()
                clone.extend(marshalled_rows)
                self.set_proxy_model(clone)
                self.set_filtered(cached_rows)
                return None

        match mode:
            case FilterMode.INITIAL:
                rows = self.filter_initial(filters)
            case FilterMode.TOGGLE_ON:
                rows = self.filter_toggle_on(filters)
            case FilterMode.TOGGLE_OFF:
                for f in filters[2:]:
                    self.set_filtered(self.filter_toggle_off(filters, f))
                rows = self.filtered

        # NOTE: FastInsertListStore manipulation must remain local to the thread
        clone = ModelFactory().make_server_store()
        if len(rows) > 0:
            rows = self.sort_rows(rows)
            marshalled_rows = ServerRow.marshal_rows(rows)
            clone.extend(marshalled_rows)

        self.set_cache(filters, rows)
        self.set_proxy_model(clone)
        return clone

    def sort_rows(self, rows: list[ServerRow]) -> list[ServerRow]:
        rows.sort(key=lambda x: re.sub(r"[^A-Za-z0-9]+", "", x.name.lower()))
        return rows

    def filter_initial(self, filters: tuple[str, ...]) -> list[ServerRow]:
        """
        Simply culls the control model of any disabled filters
        """
        self.set_filtered(self.control_model)
        for f in filters[2:]:
            self.set_filtered(self.filter_toggle_off(filters, f))
        return self.filtered

    def filter_map(self, filters: tuple[str, ...]) -> list[ServerRow]:
        """
        Multi-filtration for any context starts by narrowing by map
        """
        rows = self.filtered
        sel_map = self.filter_man.get_active_map_name()

        if sel_map == str_filters.all_maps:
            return rows

        rows = [row for row in rows if row.mapname == sel_map]
        return rows

    def filter_keyword(self, filters: tuple[str, ...]) -> list[ServerRow]:
        keyword = self.filter_man.get_active_keyword()
        rows = self.filtered

        if keyword == "":
            return rows

        filtered = [
            row
            for row in rows
            if keyword in row.name.lower()
            or keyword in row.mapname.lower()
            or keyword in row.ip.lower()
        ]
        return filtered

    def filter_toggle_off(
        self, filters: tuple[str, ...], filter_type: str
    ) -> list[ServerRow]:
        """
        Sub-filtration of the current model
        """
        pairs = {
            strings.filter_3pp: strings.filter_1pp,
            strings.filter_day: strings.filter_night,
            strings.filter_official: strings.filter_unofficial,
        }
        for k, v in pairs.items():
            if k in filters and v in filters:
                self.set_filtered(None)
                return []

        # TODO: pack filter type enum in filter checkbox, rather than stringwise comparison
        rows = self.filtration_manager.filter(filter_type, self.filtered)
        return rows

    def filter_toggle_on(self, filters: tuple[str, ...]) -> list[ServerRow]:
        """Effectively applies all filters"""
        self.set_filtered(self.control_model)
        self.set_filtered(self.filter_map(filters))
        self.set_filtered(self.filter_keyword(filters))

        f: str
        for f in filters[2:]:
            self.set_filtered(self.filter_toggle_off(filters, f))
        return self.filtered

    def set_cache(
        self, filters: tuple[str, ...], filtered_rows: list[ServerRow]
    ) -> None:
        self.filter_cache[filters] = filtered_rows

    def set_filtered(self, rows: list[ServerRow] | None) -> None:
        if rows is None:
            self.filtered = []
        else:
            self.filtered = rows

    def get_filtered(self) -> list[ServerRow]:
        return self.filtered

    def set_proxy_model(self, model: "FastInsertListStore") -> None:
        """
        FastInsertListStore representation of the raw model after filtration

        This attribute is saved from within a thread so that it later be retrieved
        and safely packed into the TreeView in the main loop, cf. get_proxy_model()
        """
        self.proxy_model = model

    def set_control(self, rows: list[ServerRow]) -> None:
        """
        Raw data model prior to filtration
        """
        self.control_model = rows

    def get_control(self) -> list[ServerRow]:
        if self.control_model is None:
            raise AttributeError(
                "Expected a populated control model, but it is Nonetype"
            )
        return self.control_model

    def wipe_cache(self, full: bool = False) -> None:
        self.filtered = []
        self.filter_cache = {}

    def push(self, data: list[ServerRow]) -> None:
        self.wipe_cache()
        self.set_control(data)
        cur_keyword = self.filter_man.get_active_keyword()
        mode = FilterMode.TOGGLE_ON if len(cur_keyword) > 0 else FilterMode.INITIAL
        self.filter(mode)
