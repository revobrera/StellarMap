#Importing libraries for 

import datetime  # Managing date and time
import json  # Handling json format files
import platform  # Getting system information
import re  # Regular expressions (For putting checks on emails, names etc)
import sys  # To perform system level operations
import threading # To handle multiple threads (processes) at once

import pandas as pd  # For managing and handling text data
from PIL.ImageQt import rgb  # For managing and handling image data
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

#-----------------------------PyQt5 libraries and extensions----------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------Importing UI files------------------------------------------

try:
    from .gui.events import *  # IMPORT FUNCTIONS
    from .gui.mainwindow import Ui_MainWindow  # GUI FILE
    from .gui.styles import Style  # IMPORT QSS CUSTOM
    from .helpers.created_accounts import CreatedByAccounts
    from .settings.env import EnvHelpers
    from .static.icons.icons_rc import *

except:
    from gui.events import *
    from gui.mainwindow import Ui_MainWindow
    from gui.styles import Style
    from helpers.created_accounts import CreatedByAccounts
    from settings.env import EnvHelpers
    from static.icons.icons_rc import *

#----------------------------------------------------------------------------------------------


class ApplicationWindow(QMainWindow, CreatedByAccounts):


    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """ Display system info"""

        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        #----------------Remove top bar (The one with close, minimize and maximize buttons)----------------
        UIFunctions.removeTitleBar(True)
        #--------------------------------------------------------------------------------------------------

        #--------------------------------Set names of window-----------------------------------------------
        self.setWindowTitle('StellarMap [Prototype] - v0.4.0')
        UIFunctions.labelTitle(self, 'StellarMap [Prototype] - v0.4.0')
        #--------------------------------------------------------------------------------------------------


        #--------------------------------Show this message when user opens app-----------------------------
        UIFunctions.labelDescription(self, 'Network (default): TESTNET')
        #--------------------------------------------------------------------------------------------------


        #------------------------------Let user select which network to use--------------------------------
        self.ui.networkComboBox.activated[str].connect(lambda: UIFunctions.set_stellar_network(self))
        #--------------------------------------------------------------------------------------------------


        #---------------------------------Run when user clicks search bar---------------------------------
        self.ui.btn_search.clicked.connect(lambda: UIFunctions.search_creator_by_accounts(self))
        #--------------------------------------------------------------------------------------------------


        

        #-----------------------------------------Set default window size----------------------------------
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        #--------------------------------------------------------------------------------------------------

        
        #--------------------------------------Pull side menu----------------------------------------------
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        #--------------------------------------------------------------------------------------------------

        #---------------------------------------Add more menus---------------------------------------------
        self.ui.stackedWidget.setMinimumWidth(20)
        
        #Adding home menu
        UIFunctions.addNewMenu(self, "HOME", "btn_home", "url(:/16x16/16x16/cil-home.png)", True)
        
        #Adding settings menu
        UIFunctions.addNewMenu(self, "Settings", "btn_widgets", "url(:/16x16/16x16/cil-equalizer.png)", False)
        #--------------------------------------------------------------------------------------------------


        #-------------------------------------Start menu gets selected-------------------------------------
        UIFunctions.selectStandardMenu(self, "btn_home")
        #--------------------------------------------------------------------------------------------------

        #-------------------------------------Start menu gets selected-------------------------------------
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        #--------------------------------------------------------------------------------------------------

        #-------------------------------------Show/Hide user icon------------------------------------------
        UIFunctions.userIcon(self, "RO", "", False)
        #--------------------------------------------------------------------------------------------------


        #------------Whenever mouse click detected at top border, move window to latest position-----------
        def moveWindow(event):

            # If windows is in full screen, change back to normal
            if UIFunctions.returnStatus(self) == 1:
                UIFunctions.maximize_restore(self)

            #Detect click on top frame and move window where mouse moves
            if event.buttons() == Qt.LeftButton:

                #Take new position and move window
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        #Select top frame that will make window move
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        #--------------------------------------------------------------------------------------------------

        #-------------------------------------Load basic window structure----------------------------------
        UIFunctions.uiDefinitions(self)
        #--------------------------------------------------------------------------------------------------


        #-------------------------------Set table parameters like size-------------------------------------
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        #--------------------------------------------------------------------------------------------------

        self.show()


    def nested_dict_pairs_iterator(self, dict_obj: dict) -> tuple:
        """
        Iterate over all key-value pairs in a nested dictionary.

        Parameters:
        - dict_obj (dict): The nested dictionary to iterate over.

        Yields:
        - tuple: A tuple of the form (key, value), where key is a string and value is any type.
        """
        for key, value in dict_obj.items():
            if isinstance(value, dict):
                for pair in self.nested_dict_pairs_iterator(value):
                    yield (key, *pair)
            else:
                yield (key, value)


    def is_valid_url(self, url: str) -> bool:
        """
        Check if a given string is a valid URL.

        Parameters:
        - url (str): The string to check.

        Returns:
        - bool: True if the string is a valid URL, False otherwise.
        """
        regex = re.compile(
            r'^https?://'                                                       #   http:// or https:// at start
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'     #   Domain name
            r'localhost|'                                                       #   localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'                              #   ip
            r'(?::\d+)?'                                                        #   optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return url is not None and regex.search(url) is not None

    def is_valid_path(self, path: str) -> bool:
        """
        Check if a given string is a valid file or directory path.

        Parameters:
        - path (str): The string to check.

        Returns:
        - bool: True if the string is a valid file or directory path, False otherwise.
        """
        check_file = re.compile(r'^(\/+\w{0,}){0,}\.\w{1,}$')
        check_directory = re.compile(r'^(\/+\w{0,}){0,}$')
        return check_file.match(path) is not None or check_directory.match(path) is not None

    def is_valid_stellar_address(self, stellar_address: str) -> bool:
        """
        Check if a given string is a valid Stellar address.

        Parameters:
        - stellar_address (str): The string to check.

        Returns:
        - bool: True if the string is a valid Stellar address, False otherwise.
        """
        check_stellar_address = re.compile(r'[A-Z,0-9]{56}')
        return check_stellar_address.match(stellar_address) is not None
    
    def customize_text(self, item: str):
        """
        Set the style properties of the search bar based on the input.

        Parameters:
        - item (str): The string to check and customize.
        """
        datetime_object = datetime.datetime.now()
        self.ui.textEdit.insertPlainText('\n[' + str(datetime_object) + '] ')

        if self.is_valid_url(item):
            color = (78, 201, 176)
        elif self.is_valid_path(item):
            color = (234, 84, 159)
        else:
            color = (255, 255, 255)

        color = QtGui.QColor(*color)
        color_format = self.ui.textEdit.currentCharFormat()
        color_format.setForeground(color)
        self.ui.textEdit.setCurrentCharFormat(color_format)
        self.ui.textEdit.append(item)


    def print_response(self, data: dict):
        """
        Print the response after validating the input.

        Parameters:
        - data (dict): The data to print.
        """
        for pair in self.nested_dict_pairs_iterator(data):
            self.ui.textEdit.insertPlainText('\n')
            for item in pair:
                self.customize_text(str(item))


    def loading_dataset_to_ui_old(self, stellar_account_url_link: str):
        """
        Load data from a Stellar account URL and display it in the UI.

        Parameters:
        - stellar_account_url_link (str): The URL of the Stellar account to load data from.
        """
        self.customize_text('Initiated data loading from ')
        self.customize_text(stellar_account_url_link)

        df = pd.read_json(stellar_account_url_link)
        model = PandasModel(df)
        self.ui.tableView.setModel(model)

        thread1 = threading.Thread(target=self.print_response, args=(df.to_dict(),))
        thread1.start()
        self.loading_json_old(stellar_account_url_link, df.to_json())
        
    def loading_dataset_to_ui(self, stellar_account_url_link: str):
        """
        Load data from a Stellar account URL and display it in the UI.

        Parameters:
        - stellar_account_url_link (str): The URL of the Stellar account to load data from.
        """
        thread1 = threading.Thread(target=self.init_variables, args=(stellar_account_url_link,))
        thread1.start()

    def Button(self):
        """
        This function links all buttons with their respective functions
        """
        # Get the button widget that was clicked
        btn_widget = self.sender()
        button_name = btn_widget.objectName()
        
        # Home button
        if button_name == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btn_widget.setStyleSheet(UIFunctions.selectMenu(btn_widget.styleSheet()))

        # New user button
        elif button_name == "btn_new_user":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_user)
            UIFunctions.resetStyle(self, "btn_new_user")
            UIFunctions.labelPage(self, "New User")
            btn_widget.setStyleSheet(UIFunctions.selectMenu(btn_widget.styleSheet()))

        # Widgets buttons
        elif button_name == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Settings")
            btn_widget.setStyleSheet(UIFunctions.selectMenu(btn_widget.styleSheet()))
    

    #----------------------------------------Events---------------------------------------------------

    def eventFilter(self, watched, event):
        """
        This function runs when double click of mouse left click is pressed.
        """
        # Check if the double click event was on the watched object (self.le)
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    
    def mousePressEvent(self, event):
        """
        This function runs whenever a mouse click event occurs. It determines
        which button was clicked (left, right, or middle) and prints a message
        indicating which button was clicked.

        Parameters:
        event (QMouseEvent): The mouse event that triggered this function.

        Returns:
        None
        """
        self.dragPos = event.globalPos()
        button = event.button()

        if button == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        elif button == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        elif button == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')

    def keyPressEvent(self, event):
        """
        This function runs whenever any key is pressed
        """

        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
        
    def resizeEvent(self, event):
        """
        This function runs when we try to resize the window
        """

        self.resizeFunction()
        return super(ApplicationWindow, self).resizeEvent(event)

    def resizeFunction(self):
        """
        This function displays new height and width whenever window is resized
        """

        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))

    #--------------------------------------------------------------------------------------------------


def runall():
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('/StellarMap/static/fonts/Cascadia.ttf')
    window = ApplicationWindow()

    # default testnet network
    e = EnvHelpers()

    sys.exit(app.exec_())
