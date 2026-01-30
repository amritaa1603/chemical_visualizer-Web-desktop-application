import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QFileDialog, QLabel, QTableWidget, 
                             QTableWidgetItem, QHBoxLayout, QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemVis Desktop - Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1100, 700)
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Controls
        controls = QHBoxLayout()
        self.btn_upload = QPushButton("Upload CSV to API")
        self.btn_upload.clicked.connect(self.upload_file)
        self.btn_upload.setStyleSheet("padding: 10px; font-weight: bold;")
        controls.addWidget(self.btn_upload)
        layout.addLayout(controls)

        # Stats Area
        self.stats_label = QLabel("Waiting for data...")
        self.stats_label.setStyleSheet("font-size: 14px; color: #2563eb; margin: 10px;")
        layout.addWidget(self.stats_label)

        # Table and Chart Layout
        display_layout = QHBoxLayout()
        self.table = QTableWidget()
        display_layout.addWidget(self.table)

        self.canvas = PlotCanvas(self)
        display_layout.addWidget(self.canvas)
        
        layout.addLayout(display_layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                # Talking to your Django Backend
                with open(file_path, 'rb') as f:
                    response = requests.post("http://127.0.0.1:8000/api/upload/", files={'file': f})
                
                if response.status_code == 200:
                    result = response.json()
                    self.update_display(result)
                else:
                    QMessageBox.warning(self, "Error", "Backend error during processing.")
            except Exception as e:
                QMessageBox.critical(self, "Connection Error", "Is your Django server running?")

    def update_display(self, result):
        summary = result['summary']
        # Update text labels
        stats = (f"Items: {summary['total_count']} | "
                 f"Pressure: {summary['avg_pressure']:.2f} PSI | "
                 f"Temp: {summary['avg_temperature']:.2f} °C | "
                 f"Flowrate: {summary['avg_flowrate']:.2f} m³/h")
        self.stats_label.setText(stats)

        # Update Table
        data = result['data']
        if data:
            columns = data[0].keys()
            self.table.setColumnCount(len(columns))
            self.table.setRowCount(len(data))
            self.table.setHorizontalHeaderLabels(columns)
            for r, row in enumerate(data):
                for c, (key, value) in enumerate(row.items()):
                    self.table.setItem(r, c, QTableWidgetItem(str(value)))

        # Update Matplotlib Chart
        dist = summary['type_distribution']
        self.canvas.plot(list(dist.keys()), list(dist.values()))

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

    def plot(self, labels, values):
        self.axes.clear()
        self.axes.bar(labels, values, color='#2563eb')
        self.axes.set_title('Equipment Distribution')
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())