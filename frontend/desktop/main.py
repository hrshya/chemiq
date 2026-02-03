import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QListWidget,
    QLineEdit,
    QMessageBox,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

from api_client import APIClient


class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

    def plot_bar(self, labels, values, title=''):
        self.axes.clear()
        self.axes.bar(labels, values)
        self.axes.set_title(title)
        self.draw()

    def plot_hist(self, series, title=''):
        self.axes.clear()
        self.axes.hist(series.dropna(), bins=20)
        self.axes.set_title(title)
        self.draw()


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api = APIClient()
        self.setWindowTitle('Chemical Equipment Parameter Visualizer (Desktop)')
        self.resize(1000, 700)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Login row
        login_row = QHBoxLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText('username')
        self.password = QLineEdit()
        self.password.setPlaceholderText('password')
        self.password.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.do_login)
        login_row.addWidget(self.username)
        login_row.addWidget(self.password)
        login_row.addWidget(self.login_btn)
        layout.addLayout(login_row)

        # Upload + history
        row = QHBoxLayout()
        upload_col = QVBoxLayout()
        self.upload_btn = QPushButton('Upload CSV')
        self.upload_btn.clicked.connect(self.select_and_upload)
        upload_col.addWidget(self.upload_btn)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_select)
        upload_col.addWidget(QLabel('Last uploads'))
        upload_col.addWidget(self.history_list)

        row.addLayout(upload_col, 1)

        # Chart area
        self.chart = ChartCanvas(self, width=6, height=5, dpi=100)
        row.addWidget(self.chart, 3)

        layout.addLayout(row)

        # Summary label
        self.summary_label = QLabel('Summary will appear here')
        layout.addWidget(self.summary_label)

        self.setLayout(layout)

    def do_login(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        if not u or not p:
            QMessageBox.warning(self, 'Login', 'Enter username and password')
            return
        resp = self.api.login(u, p)
        if resp.ok:
            QMessageBox.information(self, 'Login', 'Login successful')
            self.refresh_history()
        else:
            QMessageBox.critical(self, 'Login', f'Login failed: {resp.status_code}')

    def select_and_upload(self):
        fn, _ = QFileDialog.getOpenFileName(self, 'Select CSV file', os.path.expanduser('~'), 'CSV Files (*.csv)')
        if not fn:
            return
        resp = self.api.upload_csv(fn)
        if resp.ok:
            QMessageBox.information(self, 'Upload', 'Upload succeeded')
            self.refresh_history()
        else:
            QMessageBox.critical(self, 'Upload', f'Upload failed: {resp.status_code} {resp.text}')

    def refresh_history(self):
        resp = self.api.get_history()
        self.history_list.clear()
        if not resp.ok:
            QMessageBox.critical(self, 'History', 'Could not fetch history')
            return
        data = resp.json()
        # DRF pagination returns a dict with 'results'; otherwise expect a list
        if isinstance(data, dict):
            items = data.get('results') or data.get('data') or []
        elif isinstance(data, list):
            items = data
        else:
            items = []

        for item in items[:5]:
            # Expect item to have id and name/created
            display = f"{item.get('id')} - {item.get('name') or item.get('filename') or item.get('created_at')}"
            lw_item = QtWidgets.QListWidgetItem(display)
            lw_item.setData(QtCore.Qt.UserRole, item)
            self.history_list.addItem(lw_item)

    def on_history_select(self, item):
        itemdata = item.data(QtCore.Qt.UserRole)
        dataset_id = itemdata.get('id')
        resp = self.api.get_summary(dataset_id)
        if not resp.ok:
            QMessageBox.critical(self, 'Summary', 'Failed to fetch summary')
            return
        summary = resp.json()
        # Display textual summary
        text = f"Count: {summary.get('count')}\nAverages: {summary.get('averages')}\nTypes: {summary.get('type_distribution')}"
        self.summary_label.setText(text)
        # Render a simple chart: types distribution
        types = summary.get('type_distribution', {})
        if types:
            labels = list(types.keys())
            values = list(types.values())
            self.chart.plot_bar(labels, values, title='Equipment by Type')
        else:
            # if numeric fields exist, show histogram of flowrate
            df = self._fetch_dataset_dataframe(dataset_id)
            if df is not None and 'Flowrate' in df.columns:
                self.chart.plot_hist(df['Flowrate'], title='Flowrate distribution')

    def _fetch_dataset_dataframe(self, dataset_id):
        # fallback: try to fetch raw CSV from API if available
        url = f"{self.api.base_url}/api/datasets/{dataset_id}/download/"
        try:
            r = self.api.session.get(url)
            if r.ok:
                from io import StringIO

                return pd.read_csv(StringIO(r.text))
        except Exception:
            return None
        return None


def main():
    app = QApplication(sys.argv)
    w = DesktopApp()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
