#from PySide6.QtWidgets import QMainWindow
#
#from rfmetadata.windows.query_result_window import TableResultsWindow
#
#
#def test_window_initialization(qtbot):
#
#    data =  [
#                (90, 103.7, 20.54, '06-06-2025 12:16:18'),
#                (91, 104.3, 20.18, '06-06-2025 12:16:18')
#            ]
#
#    table = TableResultsWindow(data)
#
#    qtbot.addWidget(table)
#
#    assert isinstance(table, QMainWindow)
#
#    table.set_type(True)
#    assert table.window_type
#