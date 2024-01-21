import os
import sys
from pathlib import Path
from typing import List, Iterable, Set

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget

from model import ModItem, ModItemModel, ModViewProxyModel
from pz import PZModInfo
from ui.MainWindow_ui import Ui_MainWindow
from ui.ModDetails_ui import Ui_ModDetails
from ui.ModSelector_ui import Ui_ModSelector

if os.name == 'nt':
    # noinspection PyUnresolvedReferences
    from win import *
elif os.name == 'posix':
    # noinspection PyUnresolvedReferences
    from linux import *
else:
    raise Exception("Unsupported operating system")


def discover_available_mods() -> List[ModItem]:
    local_mods: List[ModItem]
    workshop_mods: List[ModItem]
    local_mod_dir = PZ_HOME_DIR / "mods"
    workshop_dir = get_steam_path() / "steamapps" / "workshop" / "content" / "108600"

    # discover mods from workshop items (good to know: one workshop item can contain many mods)
    workshop_mods = [ModItem(PZModInfo.from_info_file(mod_info_file), item_dir.name)
                     for item_dir in workshop_dir.glob("*/")
                     for mod_info_file in item_dir.glob("mods/*/mod.info")]

    # discover locally installed mods
    local_mods = [ModItem(PZModInfo.from_info_file(mod_info_file), None)
                  for mod_info_file in local_mod_dir.glob("*/mod.info") if mod_info_file.parent.name != "examplemod"]

    return sorted(workshop_mods + local_mods, key=lambda mod: mod.modInfo.id)


def read_enabled_mods(server_config: Path, mod_items: List[ModItem]):
    # load enabled mods and items from ini file
    enabled_mods: List[str] = []
    enabled_workshop_items: List[str] = []  # TODO not sure how relevant this list really is for *reading*...
    with server_config.open() as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("Mods=") and len(line) > len("Mods="):
                enabled_mods = line[len("Mods="):].split(';')
            elif line.startswith("WorkshopItems=") and len(line) > len("WorkshopItems="):
                enabled_workshop_items = line[len("WorkshopItems="):].split(';')

    # assign load order from enabled mods list to all items where applicable
    mods_by_id = {mod.modInfo.id: mod for mod in mod_items}
    for i, mod_id in enumerate(enabled_mods):
        mods_by_id[mod_id].load_order = i


class ModManager(QObject):

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
        self.ui_details = Ui_ModDetails()
        self.ui_details.setupUi(self.ui.widget_modDetails)

        # set up slots
        self.ui.button_enable.clicked.connect(self.enable_mods)
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
        self._toggle_selected_mods(True)

    @Slot()
    def disable_mods(self):
        self._toggle_selected_mods(False)

    def _toggle_selected_mods(self, to_state: bool):
        if to_state is True:
            # from disabled to enabled
            selection = [self.disabled_filter_model.mapToSource(filtered_index)
                         for filtered_index in self.ui.list_disabledMods.selectedIndexes()]
        else:
            # from enabled to disabled
            selection = [self.enabled_filter_model.mapToSource(filtered_index)
                         for filtered_index in self.ui.list_enabledMods.selectedIndexes()]

        print(f"Toggle to {to_state} {len(selection)} mods in " + self.config_name, self.tabber.currentWidget())
        if len(selection) > 0:
            for selected_item_index in selection:
                self.model.set_mod_state(selected_item_index, to_state)
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