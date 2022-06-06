import datetime
import platform
import re
import sys
from threading import Thread

import pandas as pd
from PIL.ImageQt import rgb
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QAbstractTableModel, QSize, Qt
from PySide2.QtWidgets import QApplication, QMainWindow

# GUI FILE
from app_modules import *
from settings.env import envHelpers


class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():

            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])

            column_count = self.columnCount()

            for column in range(0, column_count):

                if (index.column() == column and role == Qt.TextAlignmentRole):
                    return Qt.AlignHCenter | Qt.AlignVCenter

        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        if role != Qt.EditRole:
            return False

        row = index.row()

        if row < 0 or row >= len(self._data.values):
            return False

        column = index.column()

        if column < 0 or column >= self._data.columns.size:
            return False

        self._data.iloc[row][column] = value
        self.dataChanged.emit(index, index)

        return True

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        flags |= Qt.ItemIsDragEnabled
        flags |= Qt.ItemIsDropEnabled

        return flags


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## PRINT ==> SYSTEM
        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        ########################################################################
        ## START - WINDOW ATTRIBUTES
        ########################################################################

        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        # init env variables
        app_env = envHelpers()

        ## SET ==> WINDOW TITLE
        self.setWindowTitle('StellarMap [Prototype] - v0.1.1')
        UIFunctions.labelTitle(self, 'StellarMap [Prototype] - v0.1.1')

        # set default message when user opens the app
        UIFunctions.labelDescription(self, 'Network (default): TESTNET')

        # user sets the network when selected from dropdown
        self.ui.networkComboBox.activated[str].connect(lambda: UIFunctions.set_stellar_network(self))

        # user clicks on the search button and calls search_creator_by_accounts()
        self.ui.btn_search.clicked.connect(lambda: UIFunctions.search_creator_by_accounts(self))

        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        ## ==> CREATE MENUS
        ########################################################################

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "HOME", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        # UIFunctions.addNewMenu(self, "Add User", "btn_new_user", "url(:/16x16/icons/16x16/cil-user-follow.png)", True)
        UIFunctions.addNewMenu(self, "Settings", "btn_widgets", "url(:/16x16/icons/16x16/cil-equalizer.png)", False)
        ## ==> END ##

        t=Thread(target=self.load_df)
        t.daemon = True
        t.start()


        # for i in range(df.rowCount()):
        #     for j in range(df.columnCount()):
        #         x = '{:.3f}'.format(self.df.iloc[i, j])
        #         self.tableWidget.setItem(i, j, QTableWidgetItem(x))

        # START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_home")
        ## ==> END ##

        ## ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        ## ==> END ##

        ## USER ICON ==> SHOW HIDE
        UIFunctions.userIcon(self, "RO", "", False)
        ## ==> END ##


        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returnStatus(self) == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ## ==> END ##

        ## ==> LOAD DEFINITIONS
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> END ##

        ########################################################################
        ## END - WINDOW ATTRIBUTES
        ############################## ---/--/--- ##############################




        ########################################################################
        #                                                                      #
        ## START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- ##
        #                                                                      #
        ## ==> USER CODES BELLOW                                              ##
        ########################################################################



        ## ==> QTableWidget RARAMETERS
        ########################################################################
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        ## ==> END ##



        ########################################################################
        #                                                                      #
        ## END --------------- WIDGETS FUNCTIONS/PARAMETERS ----------------- ##
        #                                                                      #
        ############################## ---/--/--- ##############################
        # import qtvscodestyle as qtvsc
        # stylesheet = qtvsc.load_stylesheet(
        #     'D:\python_projects\\revobrera\windows-terminal-aurelia-master\posh-theme\purple-man.json')
        # app.setStyleSheet(stylesheet)

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        # from qt_material import apply_stylesheet
        # apply_stylesheet(app, theme='dark_red.xml')
        #
        # File = QtCore.QFile('D:\python_projects\\revobrera\Simple_PySide_Base-master\MaterialDark.qss')
        # if not File.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
        #     return
        # print('here')
        # qss = QtCore.QTextStream(File)
        # # setup stylesheet
        # self.setStyleSheet(qss.readAll())
        # import qtvscodestyle as qtvsc
        # stylesheet = qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS)
        # app.setStyleSheet(stylesheet)

        # theme_file = r"D:\python_projects\\revobrera\windows-terminal-aurelia-master\profile\profiles.json"
        # stylesheet = qtvsc.load_stylesheet(theme_file)
        # app.setStyleSheet(stylesheet)
        # stylesheet = load_stylesheet

        self.show()
        ## ==> END ##

    def nested_dict_pairs_iterator(self,dict_obj):
        ''' This function accepts a nested dictionary as argument
            and iterate over all values of nested dictionaries
        '''
        # Iterate over all key-value pairs of dict argument
        for key, value in dict_obj.items():
            # Check if value is of dict type
            if isinstance(value, dict):
                # If value is dict then iterate over all its values
                for pair in self.nested_dict_pairs_iterator(value):
                    yield (key, *pair)
            else:
                # If value is not dict type then yield the value
                yield (key, value)

    def is_valid_url(self,url):
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url is not None and regex.search(url)

    def is_valid_path(self,path):
        check_file = re.compile("^(\/+\w{0,}){0,}\.\w{1,}$")
        check_directory = re.compile("^(\/+\w{0,}){0,}$")
        if check_file.match(path) or check_directory.match(path):
            return True
        else:
            return False

    def is_valid_stellar_address(self, stellar_address):
        check_stellar_address = re.compile("[A-Z,0-9]{56}")
        if check_stellar_address.match(stellar_address):
            return True
        else:
            return False

    def customize_text(self,item):
        # get current date time
        datetime_object = datetime.datetime.now()
        self.ui.textEdit.insertPlainText('\n[' + str(datetime_object) + '] ')

        if self.is_valid_url(item):
            color = rgb(78, 201, 176)
        elif self.is_valid_path(item):
            color = rgb(234, 84, 159)
        else:
            color = rgb(255, 255, 255)


        color = QtGui.QColor(color)

        color_format = self.ui.textEdit.currentCharFormat()
        color_format.setForeground(color)
        self.ui.textEdit.setCurrentCharFormat(color_format)
        self.ui.textEdit.insertPlainText(item)

    def print_Response(self,data):
        for pair in self.nested_dict_pairs_iterator(data):
            self.ui.textEdit.insertPlainText('\n')
            for item in pair:
                self.customize_text(str(item))

    def load_df(self):
        link = 'https://horizon-testnet.stellar.org/'

        self.customize_text('Initiated data loading from ')
        self.customize_text(link)


        df = pd.read_json(link)
        del df['_links']
        model = PandasModel(df)
        self.ui.tableView.setModel(model)

        thread1=Thread(target=self.print_Response,args=(df.to_dict(),))
        thread1.start()

    ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE NEW USER
        if btnWidget.objectName() == "btn_new_user":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_user)
            UIFunctions.resetStyle(self, "btn_new_user")
            UIFunctions.labelPage(self, "New User")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Settings")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    ## ==> END ##

    ########################################################################
    ## START ==> APP EVENTS
    ########################################################################

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##

    ## EVENT ==> KEY PRESSED
    ########################################################################
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
    ## ==> END ##

    ########################################################################
    ## END ==> APP EVENTS
    ############################## ---/--/--- ##############################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('/StellarMap/fonts/Cascadia.ttf')
    window = MainWindow()
    sys.exit(app.exec_())
