from typing import List, Optional

from PySide6.QtCore import QModelIndex, QAbstractListModel, QSortFilterProxyModel
from PySide6.QtGui import QColor, Qt

from pz import PZModInfo


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
            return QColor(200, 255, 200) if item.enabled else QColor(255, 200, 200)

    def removeRows(self, row, count, parent=...):
        super().beginRemoveRows(parent, row, row+count)
        for _ in range(count):
            del self.items[row]
            del self.indices[row]
        super().endRemoveRows()


class ModViewProxyModel(QSortFilterProxyModel):
    """Provides filtering to the view"""
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
