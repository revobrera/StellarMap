import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

def main():
    """
    Main function that displays a web page in a PyQt5 window.
    """
    # Create a QApplication instance
    app = QApplication()

    # Create a QWebEngineView instance
    view = QWebEngineView()

    # Get the path to the html file
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'collapsible_radial_tree', 'index.html')

    # Load the html file into the QWebEngineView
    view.load(QUrl.fromLocalFile(html_file))

    # Show the QWebEngineView
    view.show()

    # Run the QApplication event loop
    app.exec_()

if __name__ == '__main__':
    main()
