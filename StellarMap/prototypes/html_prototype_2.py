import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
view = QWebEngineView()

html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'collapsible_radial_tree', 'index.html')
view.load(QUrl.fromLocalFile(html_file))

view.show()
sys.exit(app.exec_())
