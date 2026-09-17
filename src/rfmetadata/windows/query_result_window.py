from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem

from rfmetadata.signal_manager.data_signal_manager import table_type_manager

result_window:QMainWindow


class TableResultsWindow(QMainWindow):
    window_type:bool = False
    def __init__(self, query:str) -> None:
        super().__init__()
        self.setWindowTitle("Query Results")
        # Create table view
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(len(query))
        self.table.setHorizontalHeaderLabels(["ID", "frequency", "power", "datetime"])


        for row, row_data in enumerate(query):
            for col, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)



        # Configure table
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeColumnsToContents()

        self.setCentralWidget(self.table)
        self.resize(800, 600)

        table_type_manager.data_signal.connect(self.set_type)

    def set_type(self, type:bool) -> None:
        TableResultsWindow.window_type = type

# Usage:
def show_query_results(query:str) -> None:

    global result_window
    result_window = TableResultsWindow(query)
    if result_window.window_type:
        result_window.show()
    else:
        pass
