from __future__ import annotations

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex
)


class ModTableModel(QAbstractTableModel):

    HEADERS = [
        "Mod",
        "Loader",
        "Tipo",
        "Confianza",
        "Dependencias"
    ]

    def __init__(self):

        super().__init__()

        self._mods = []

    def rowCount(self, parent=QModelIndex()):

        return len(self._mods)

    def columnCount(self, parent=QModelIndex()):

        return len(self.HEADERS)

    def headerData(self, section, orientation, role):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

        return section + 1

    def data(self, index, role):

        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        mod = self._mods[index.row()]

        column = index.column()

        if column == 0:
            return mod["name"]

        elif column == 1:
            return mod["loader"]

        elif column == 2:
            return mod["side"]

        elif column == 3:
            return f'{mod["confidence"]}%'

        elif column == 4:
            return ", ".join(mod["depends"])

        return None

    def clear(self):

        self.beginResetModel()

        self._mods.clear()

        self.endResetModel()

    def add_mod(self, mod):

        self.beginInsertRows(
            QModelIndex(),
            len(self._mods),
            len(self._mods)
        )

        self._mods.append(mod)

        self.endInsertRows()

    def mods(self):

        return self._mods
