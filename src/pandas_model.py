from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
import pandas as pd

class PandasModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame = None, parent=None):
        super().__init__(parent)
        self._df = df.copy() if df is not None else pd.DataFrame()

    def rowCount(self, parent=QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QModelIndex()):
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role in (Qt.DisplayRole, Qt.EditRole):
            val = self._df.iat[index.row(), index.column()]
            return str(val)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return str(self._df.columns[section])
        else:
            return str(self._df.index[section])

    def sort(self, column, order):
        colname = self._df.columns[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(drop=True, inplace=True)
        self.layoutChanged.emit()

    def setDataFrame(self, df):
        self.beginResetModel()
        self._df = df.copy()
        self.endResetModel()
