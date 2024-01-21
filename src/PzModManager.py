import os
import sys
from pathlib import Path
from typing import List, Iterable, Optional

from PySide6.QtCore import QObject, Slot, Signal, QItemSelectionModel
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QListView

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
    editorDirty = Signal(bool)

    def __init__(self, server_config: Path, tabber: QTabWidget):
        # init stuff
        super().__init__(tabber)
        self.tabber = tabber
        self.tab_index: int = -1
        self.config_name = server_config.name[:-4]
        self.config_path = server_config

        # create stuff
        self.widget = QWidget()
        self.ui = Ui_ModSelector()
        self.ui.setupUi(self.widget)
        self.ui_details = Ui_ModDetails()
        self.ui_details.setupUi(self.ui.widget_modDetails)
        self.active_list: Optional[QListView] = None

        # set up slots
        self.ui.button_enable.clicked.connect(self.enable_mods)
        self.ui.button_disable.clicked.connect(self.disable_mods)
        self.ui.list_disabledMods.clicked.connect(self.set_disabled_list_active)
        self.ui.list_enabledMods.clicked.connect(self.set_enabled_list_active)
        self.ui.button_moveUp.clicked.connect(self.move_enabled_up)
        self.ui.button_moveDown.clicked.connect(self.move_enabled_down)
        self.modStateChanged.connect(self.mod_state_changed)
        self.editorDirty.connect(self.editor_dirty)

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

    @property
    def is_active(self) -> bool:
        return self.tabber.currentWidget() == self.widget

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
            self.ui.list_disabledMods.clearSelection()
        else:
            # from enabled to disabled
            selection = [self.enabled_filter_model.mapToSource(filtered_index)
                         for filtered_index in self.ui.list_enabledMods.selectedIndexes()]
            self.ui.list_enabledMods.clearSelection()

        print(f"Toggle to {to_state} {len(selection)} mods in " + self.config_name, self.tabber.currentWidget())
        if len(selection) > 0:
            for selected_item_index in selection:
                self.model.set_mod_state(selected_item_index, to_state)
            self.modStateChanged.emit(*self.model.counts())
            self.editorDirty.emit(True)

    @Slot()
    def set_disabled_list_active(self):
        self.active_list = self.ui.list_disabledMods

    @Slot()
    def set_enabled_list_active(self):
        self.active_list = self.ui.list_enabledMods

    def move_enabled_up(self):
        self._move_enabled_mods(-1)

    @Slot()
    def move_enabled_down(self):
        self._move_enabled_mods(1)

    def _move_enabled_mods(self, direction: int):
        list_view = self.ui.list_enabledMods
        selection = sorted(list_view.selectedIndexes(), key=lambda x: x.row())
        if len(selection) == 0 \
                or direction < 0 and selection[0].row() == 0 \
                or direction > 0 and selection[-1].row() == self.model.counts()[1] - 1:
            # do nothing if there is no selection or top-most selected item is at the very top already
            return

        # algorithm:
        #   to move items up, go through the list top-to-bottom
        #   and swap the load_order of each selected item with the one of the item directly before it
        filtered_rows_to_select = []
        for filtered_item_index in selection:
            actual_selected_item_index = self.enabled_filter_model.mapToSource(filtered_item_index)
            filtered_item_index_before = self.enabled_filter_model.index(filtered_item_index.row() + direction, 0)
            actual_item_index_before = self.enabled_filter_model.mapToSource(filtered_item_index_before)

            selected_item = self.model.get_item_of(actual_selected_item_index)
            item_before = self.model.get_item_of(actual_item_index_before)
            selected_item.load_order += direction
            item_before.load_order -= direction

            filtered_rows_to_select.append(filtered_item_index_before.row())
            self.model.update()

        self.editorDirty.emit(True)

        # update current selection accordingly, so it gets moved with the item(s)
        list_view.clearSelection()
        sm = list_view.selectionModel()
        for row in filtered_rows_to_select:
            sm.select(self.enabled_filter_model.index(row, 0), QItemSelectionModel.SelectionFlag.Select)

    @Slot()
    def mod_state_changed(self, total_count: int, enabled_count: int):
        print("Mods state changed", total_count, enabled_count)
        self.ui.label_disabledCount.setText(f"({total_count-enabled_count})")
        self.ui.label_enabledCount.setText(f"({enabled_count})")
        self.model.update()
        self.enabled_filter_model.invalidate()
        self.disabled_filter_model.invalidate()

    @Slot()
    def editor_dirty(self, is_dirty: bool):
        tab: QTabWidget = self.parent()
        current_text = tab.tabText(self.tab_index)
        if is_dirty and not current_text.endswith('*'):
            tab.setTabText(self.tab_index, current_text + "*")
        elif not is_dirty and current_text.endswith('*'):
            tab.setTabText(self.tab_index, current_text[:-1])

    @Slot()
    def show_details(self, visible: bool):
        self.ui.widget_modDetails.setVisible(visible)

    @Slot()
    def save(self):
        if self.is_active:
            self._save()

    @Slot()
    def save_all(self):
        self._save()

    def _save(self):
        enabled_mods = self.model.get_enabled_mods()
        mod_ids = ";".join(mod.modInfo.id for mod in enabled_mods)
        workshop_ids = ";".join(set(mod.workshopId for mod in enabled_mods if mod.workshopId))

        with self.config_path.open("r", newline='\n') as f:
            current_contents = f.readlines()
        for i in range(len(current_contents)):
            if current_contents[i].startswith("Mods="):
                current_contents[i] = f"Mods={mod_ids}\n"
            elif current_contents[i].startswith("WorkshopItems="):
                current_contents[i] = f"WorkshopItems={workshop_ids}\n"
        with self.config_path.open("w", newline='\n') as f:
            f.writelines(current_contents)
        self.editorDirty.emit(False)

    @Slot()
    def select_all(self):
        if not self.is_active:
            return
        self.active_list.selectAll()


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
    ui.action_Quit.triggered.connect(app.quit)

    manager: ModManager
    for manager in load_server_configs(ui.tabWidget):
        manager.tab_index = ui.tabWidget.addTab(manager.widget, manager.config_name)
        ui.action_ShowDetails.toggled.connect(manager.show_details)
        ui.action_Save.triggered.connect(manager.save)
        ui.action_SaveAll.triggered.connect(manager.save_all)
        ui.action_SelectAll.triggered.connect(manager.select_all)

    main_window.show()

    sys.exit(app.exec())
