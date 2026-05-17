"""
Nama: Mohammad Klisman Reynaldi
NIM : F1D022063
Kelas: PemVisD
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableView, QComboBox, QFileDialog, QLabel
)
from PySide6.QtCore import Qt

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

try:
    # when running as package (import src.main)
    from src.data_loader import load_data
    from src.pandas_model import PandasModel
except Exception:
    # when running directly (python src/main.py)
    from data_loader import load_data
    from pandas_model import PandasModel


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dashboard Visualisasi Data - PySide6')
        self.resize(1000, 700)

        self.df = load_data()

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Controls
        ctrl_layout = QHBoxLayout()
        self.combo = QComboBox()
        self.combo.addItem('All')
        if 'Product line' in self.df.columns:
            for v in sorted(self.df['Product line'].dropna().unique()):
                self.combo.addItem(str(v))
        ctrl_layout.addWidget(QLabel('Filter Product line:'))
        ctrl_layout.addWidget(self.combo)

        # Pie grouping selector (so pie chart can show other categorical distributions)
        self.pie_group_combo = QComboBox()
        ctrl_layout.addWidget(QLabel('Pie grouping:'))
        ctrl_layout.addWidget(self.pie_group_combo)
        # populate pie grouping choices with common categorical columns
        def populate_pie_choices():
            self.pie_group_combo.blockSignals(True)
            self.pie_group_combo.clear()
            # always include Product line as default
            choices = []
            for c in ['Product line', 'Payment', 'Gender', 'Branch', 'City', 'Customer type']:
                if c in self.df.columns:
                    choices.append(c)
            for ch in choices:
                self.pie_group_combo.addItem(ch)
            self.pie_group_combo.blockSignals(False)
        populate_pie_choices()

        self.refresh_btn = QPushButton('Refresh')
        self.export_chart_btn = QPushButton('Export Charts PNG')
        self.export_csv_btn = QPushButton('Export Table CSV')
        ctrl_layout.addWidget(self.refresh_btn)
        ctrl_layout.addWidget(self.export_chart_btn)
        ctrl_layout.addWidget(self.export_csv_btn)
        main_layout.addLayout(ctrl_layout)

        # Table
        self.table = QTableView()
        self.model = PandasModel(self.df)
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)
        main_layout.addWidget(self.table, stretch=3)

        # Charts
        charts_layout = QHBoxLayout()
        self.canvas_bar = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas_pie = MplCanvas(self, width=5, height=4, dpi=100)
        charts_layout.addWidget(self.canvas_bar, stretch=1)
        charts_layout.addWidget(self.canvas_pie, stretch=1)
        main_layout.addLayout(charts_layout, stretch=2)

        # Connections
        self.combo.currentTextChanged.connect(self.update_filters)
        self.pie_group_combo.currentTextChanged.connect(self.update_charts)
        self.refresh_btn.clicked.connect(self.on_refresh)
        self.export_chart_btn.clicked.connect(self.on_export_charts)
        self.export_csv_btn.clicked.connect(self.on_export_csv)

        self.update_charts()

    def filtered_df(self):
        sel = self.combo.currentText()
        if sel == 'All':
            return self.df
        return self.df[self.df['Product line'] == sel]

    def update_filters(self, _=None):
        df2 = self.filtered_df()
        self.model.setDataFrame(df2)
        self.update_charts()

    def on_refresh(self):
        self.df = load_data()
        # reset filter options
        self.combo.blockSignals(True)
        self.combo.clear()
        self.combo.addItem('All')
        if 'Product line' in self.df.columns:
            for v in sorted(self.df['Product line'].dropna().unique()):
                self.combo.addItem(str(v))
        self.combo.blockSignals(False)
        # repopulate pie grouping choices (they depend on columns present)
        try:
            # call the populate function if available
            populate = getattr(self, 'pie_group_combo', None)
            # we'll rebuild choices using same logic as initialization
            self.pie_group_combo.blockSignals(True)
            self.pie_group_combo.clear()
            for c in ['Product line', 'Payment', 'Gender', 'Branch', 'City', 'Customer type']:
                if c in self.df.columns:
                    self.pie_group_combo.addItem(c)
            self.pie_group_combo.blockSignals(False)
        except Exception:
            pass
        self.update_filters()

    def update_charts(self):
        df2 = self.filtered_df()
        # bar: aggregate by Branch or City and use Total or Sales as value
        self.canvas_bar.axes.clear()
        group_col = None
        for c in ['Branch', 'City']:
            if c in df2.columns:
                group_col = c
                break
        value_col = None
        for v in ['Total', 'Sales']:
            if v in df2.columns:
                value_col = v
                break
        if group_col and value_col:
            by_group = df2.groupby(group_col)[value_col].sum()
            by_group.plot(kind='bar', ax=self.canvas_bar.axes, color=['#2ca02c', '#1f77b4', '#ff7f0e'])
            # make x labels horizontal for readability
            self.canvas_bar.axes.tick_params(axis='x', rotation=0)
            # normalize display name to avoid 'Total Total' title
            display_name = 'Sales' if str(value_col).lower() in ('total', 'sales') else value_col
            self.canvas_bar.axes.set_title(f'Total {display_name} by {group_col}')
            self.canvas_bar.axes.set_ylabel(display_name)
        self.canvas_bar.draw()

        # pie: categorical distribution based on selected grouping
        self.canvas_pie.axes.clear()
        pg = None
        if hasattr(self, 'pie_group_combo') and self.pie_group_combo.currentText():
            pg = self.pie_group_combo.currentText()
        # default to Product line if nothing selected or not present
        if not pg:
            pg = 'Product line' if 'Product line' in df2.columns else None
        if pg and pg in df2.columns:
            counts = df2[pg].value_counts()
            counts.plot(kind='pie', ax=self.canvas_pie.axes, autopct='%1.1f%%')
            self.canvas_pie.axes.set_ylabel('')
            self.canvas_pie.axes.set_title(f'{pg} distribution')
        self.canvas_pie.draw()

    def on_export_charts(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select folder to save charts')
        if not folder:
            return
        bar_path = Path(folder) / 'chart_bar.png'
        pie_path = Path(folder) / 'chart_pie.png'
        try:
            self.canvas_bar.figure.savefig(bar_path)
            self.canvas_pie.figure.savefig(pie_path)
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Export error', f'Gagal menyimpan chart: {e}')

    def on_export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save CSV', filter='CSV Files (*.csv)')
        if not path:
            return
        try:
            self.filtered_df().to_csv(path, index=False)
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Export error', f'Gagal menyimpan CSV: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
