import os
import sys
import string
from typing import List, Iterable, Optional, Set
import random

from PySide6.QtCore import QObject, Slot, QAbstractListModel, Qt, QSortFilterProxyModel, QModelIndex, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget

from pz import PZModInfo
from ui.MainWindow_ui import Ui_MainWindow
from ui.ModSelector_ui import Ui_ModSelector
from ui.ModDetails_ui import Ui_ModDetails
from pathlib import Path

if os.name == 'nt':
    # noinspection PyUnresolvedReferences
    from win import *
elif os.name == 'posix':
    # noinspection PyUnresolvedReferences
    from linux import *
else:
    raise Exception("Unsupported operating system")


class GeneratedElement(QObject):
    """Just a helper class for creating multiple instances of the same UI widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uid = "".join(random.choice(string.ascii_lowercase) for _ in range(8))

    def unique(self, what: str):
        return f"{what}_{self.uid}"

    def fix_object_name(self, what: QObject):
        what.setObjectName(f"{self.unique(what.objectName())}")


class ModItem:
    """Represents an item in the data-model of the MVC ListView"""
    def __init__(self, mod_info: PZModInfo, enabled: bool, workshop_id: Optional[str]):
        """
        :param mod_info: all info about the mod
        :param enabled: whether the mod is currently enabled
        :param workshop_id: Steam's workshop element ID if this is mod is from the Steam workshop
        """
        super().__init__()
        self.modInfo = mod_info
        self.enabled = enabled
        self.workshopId = workshop_id


class ModItemModel(QAbstractListModel):
    """Represents the data-model of the MVC ListView"""
    def __init__(self, mods: List[ModItem], parent=None):
        super().__init__(parent)
        self.items = mods
        self.indices = []
        for i, modInfo in enumerate(mods):
            self.indices.append(super().createIndex(i, 0, modInfo))

    def counts(self) -> (int, int):
        total = len(self.items)
        enabled = sum(1 for item in self.items if item.enabled)
        print("counts", total, enabled)
        return total, enabled

    def update(self):
        super().dataChanged.emit(self.indices[0], self.indices[-1], [])

    def read_item(self, index: QModelIndex):
        return self.items[index.row()]

    def set_mod_state(self, index: QModelIndex, enabled: bool):
        self.items[index.row()].enabled = enabled
        print("set", self.items[index.row()].modInfo.id, enabled)

    def index(self, row, column=0, parent=None):
        assert column == 0
        return self.indices[row]

    def parent(self):
        return super().parent()

    def rowCount(self, parent=None):
        return len(self.items)

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemNeverHasChildren

    def data(self, index, role=...):
        item = self.items[index.row()]
        mod = item.modInfo

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() > 0:
                return None
            display_string = mod.name
            if item.workshopId:
                display_string += f" [{item.workshopId}]"
            return display_string
        elif role == Qt.ItemDataRole.BackgroundRole:
            # so far, this is only for debugging purposes
            return QColor(200,255,200) if item.enabled else QColor(255,200,200)

    def removeRows(self, row, count, parent=...):
        super().beginRemoveRows(parent, row, row+count)
        for _ in range(count):
            del self.items[row]
            del self.indices[row]
        super().endRemoveRows()


def discover_available_mods() -> List[ModItem]:
    local_mods: List[ModItem]
    workshop_mods: List[ModItem]
    local_mod_dir = PZ_HOME_DIR / "mods"
    workshop_dir = get_steam_path() / "steamapps" / "workshop" / "content" / "108600"

    # discover mods from workshop items (good to know: one workshop item can contain many mods)
    workshop_mods = [ModItem(PZModInfo.from_info_file(mod_info_file), False, item_dir.name)
                     for item_dir in workshop_dir.glob("*/")
                     for mod_info_file in item_dir.glob("mods/*/mod.info")]

    # discover locally installed mods
    local_mods = [ModItem(PZModInfo.from_info_file(mod_info_file), False, None)
                  for mod_info_file in local_mod_dir.glob("*/mod.info") if mod_info_file.parent.name != "examplemod"]

    return sorted(workshop_mods + local_mods, key=lambda mod: mod.modInfo.id)


def read_enabled_mods(server_config: Path, mod_items: List[ModItem]):
    # load enabled mods and items from ini file
    enabled_mods: Set[str] = set()
    enabled_workshop_items: Set[str] = set()
    with server_config.open() as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("Mods="):
                enabled_mods.update(line[len("Mods="):].split(';'))
            elif line.startswith("WorkshopItems="):
                enabled_workshop_items.update(line[len("WorkshopItems="):].split(';'))

    # go through mod items and set 'enabled' flags accordingly
    for mod in mod_items:
        mod.enabled = mod.modInfo.id in enabled_mods or mod.workshopId in enabled_workshop_items


class ModViewProxyModel(QSortFilterProxyModel):
    def __init__(self, enabled_state_filter: bool, parent=None):
        super().__init__(parent)
        self.enabled_state_filter = enabled_state_filter

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        model: ModItemModel = super().sourceModel()
        item_index: QModelIndex = model.index(source_row, 0, source_parent)
        row_data: ModItem = model.read_item(item_index)
        if row_data.enabled != self.enabled_state_filter:
            return False
        return super().filterAcceptsRow(source_row, source_parent)


class ModManager(GeneratedElement):

    modStateChanged = Signal(int, int)  # total count, enabled count

    def __init__(self, server_config: Path, tabber: QTabWidget):
        # init stuff
        super().__init__(tabber)
        self.tabber = tabber
        self.config_name = server_config.name[:-4]
        self.config_path = server_config

        # create stuff
        self.widget = QWidget()
        self.ui = Ui_ModSelector()
        self.ui.setupUi(self.widget)
        self.fix_object_name(self.widget)
        self.ui_details = Ui_ModDetails()
        self.ui_details.setupUi(self.ui.widget_modDetails)

        # set up slots
        self.fix_object_name(self.ui.button_enable)
        self.ui.button_enable.clicked.connect(self.enable_mods)
        self.fix_object_name(self.ui.button_disable)
        self.ui.button_disable.clicked.connect(self.disable_mods)
        self.modStateChanged.connect(self.mod_state_changed)

        # create data model and set up list views
        self.all_mods = discover_available_mods()
        read_enabled_mods(server_config, self.all_mods)
        self.model = ModItemModel(self.all_mods, parent=self.widget)

        # ... model for "available" list
        self.disabled_filter_model = ModViewProxyModel(False, parent=self.widget)
        self.disabled_filter_model.setSourceModel(self.model)
        self.ui.list_disabledMods.setModel(self.disabled_filter_model)

        # ... model for "enabled" list
        self.enabled_filter_model = ModViewProxyModel(True, parent=self.widget)
        self.enabled_filter_model.setSourceModel(self.model)
        self.ui.list_enabledMods.setModel(self.enabled_filter_model)

        # hook up search bars
        self.ui.lineEdit_filterDisabled.textChanged.connect(self.disabled_filter_model.setFilterFixedString)
        self.ui.lineEdit_filterEnabled.textChanged.connect(self.enabled_filter_model.setFilterFixedString)

        # update certain things
        self.modStateChanged.emit(*self.model.counts())

    @Slot()
    def enable_mods(self):
        selection = self.ui.list_disabledMods.selectedIndexes()
        print(f"Enabling {len(selection)} mods in " + self.config_name, self.tabber.currentWidget())
        if len(selection) == 0:
            return
        for selected_item_index in selection:
            selected_item_index = self.disabled_filter_model.mapToSource(selected_item_index)
            self.model.set_mod_state(selected_item_index, True)
        self.modStateChanged.emit(*self.model.counts())

    @Slot()
    def disable_mods(self):
        selection = self.ui.list_enabledMods.selectedIndexes()
        print(f"Disabling {len(selection)} mods in " + self.config_name, self.tabber.currentWidget())
        if len(selection) == 0:
            return
        for selected_item_index in selection:
            selected_item_index = self.enabled_filter_model.mapToSource(selected_item_index)
            self.model.set_mod_state(selected_item_index, False)
        self.modStateChanged.emit(*self.model.counts())

    @Slot()
    def mod_state_changed(self, total_count: int, enabled_count: int):
        print("Mods state changed", total_count, enabled_count)
        self.ui.label_disabledCount.setText(f"({total_count-enabled_count})")
        self.ui.label_enabledCount.setText(f"({enabled_count})")
        self.model.update()
        self.enabled_filter_model.invalidate()
        self.disabled_filter_model.invalidate()

    @Slot()
    def show_details(self, visible: bool):
        self.ui.widget_modDetails.setVisible(visible)


def load_server_configs(tabber: QTabWidget) -> Iterable[ModManager]:
    server_config_dir = PZ_HOME_DIR / "Server"  # TODO this might not be the correct path on linux
    server_configs = server_config_dir.glob("*.ini")

    for config_file in sorted(server_configs):
        yield ModManager(config_file, tabber)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)

    ui.action_ShowDetails.setChecked(True)

    manager: ModManager
    for manager in load_server_configs(ui.tabWidget):
        ui.tabWidget.addTab(manager.widget, manager.config_name)
        ui.action_ShowDetails.toggled.connect(manager.show_details)

    main_window.show()

    sys.exit(app.exec())
