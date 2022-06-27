#Importing libraries for 

import datetime  # Managing date and time
import json  # Handling json format files
import platform  # Getting system information
import re  # Regular expressions (For putting checks on emails, names etc)
import sys  # To perform system level operations
from threading import Thread  # To handle multiple threads (processes) at once

import pandas as pd  # For managing and handling text data
from PIL.ImageQt import rgb  # For managing and handling image data
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

#-----------------------------PyQt5 libraries and extensions----------------------------------


#----------------------------------------------------------------------------------------------


#----------------------------------Importing UI files------------------------------------------

try:
    from .helpers.created_accounts import CreatedByAccounts
    from .static.icons.icons_rc import *
    from .settings.env import EnvHelpers
    from .gui.events import *  # IMPORT FUNCTIONS
    from .gui.mainwindow import Ui_MainWindow  # GUI FILE
    from .gui.styles import Style  # IMPORT QSS CUSTOM

except:
    from helpers.created_accounts import CreatedByAccounts
    from static.icons.icons_rc import *
    from settings.env import EnvHelpers
    from gui.events import *
    from gui.mainwindow import Ui_MainWindow
    from gui.styles import Style

#----------------------------------------------------------------------------------------------

  

class MainWindow(QMainWindow, CreatedByAccounts):


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
        self.setWindowTitle('StellarMap [Prototype] - v0.2.0')
        UIFunctions.labelTitle(self, 'StellarMap [Prototype] - v0.2.0')
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


    def nested_dict_pairs_iterator(self,dict_obj):
        """
        This function accepts a nested dictionary as argument
        and goes over all values of nested dictionaries
        """

        # Iterate over each value pairs of dict argument
        for key, value in dict_obj.items():
            
            # Check if type of value is dictionary
            if isinstance(value, dict):

                # If value is dictioinary type then iterate over all its sub-values
                for pair in self.nested_dict_pairs_iterator(value):
                    yield (key, *pair)
            

            else:
                # If value is not dict type then yield the value
                yield (key, value)


    def is_valid_url(self,url):
        """
        This function takes a url as input and checks if it is valid or not
        """

        #Use regular expression to valide if url is in right format
        regex = re.compile(
            
            r'^https?://'                                                       #   http:// or https:// at staer
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'     #   Domain name
            r'localhost|'                                                       #   localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'                              #   ip
            r'(?::\d+)?'                                                        #   optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        

        #At the end return the url
        return url is not None and regex.search(url)


    def is_valid_path(self,path):
        """
        This functions checks if given path is valid or not
        """

        check_file = re.compile("^(\/+\w{0,}){0,}\.\w{1,}$")        #Check if file in path is valid
        check_directory = re.compile("^(\/+\w{0,}){0,}$")           #Check if directory is valid
        if check_file.match(path) or check_directory.match(path):   #If both are valid return true
            return True
        else:
            return False                                            #Otherwise return false


    def is_valid_stellar_address(self, stellar_address):
        """
        This function checks if steller address is valid
        """

        check_stellar_address = re.compile("[A-Z,0-9]{56}")         #Make an address containing A to Z and 0 to 9
        
        if check_stellar_address.match(stellar_address):            #Match that address with input
            return True                                             #If matched return true
        else:
            return False                                            #Otherwise return false

    
    def customize_text(self, item):
        """
        This function sets style properties of search bar
        """

        # get current date time
        datetime_object = datetime.datetime.now()
        self.ui.textEdit.insertPlainText('\n[' + str(datetime_object) + '] ')
        
        #Check if url that got typed in search bar is valid
        if self.is_valid_url(item):
            color = rgb(78, 201, 176)

        #If it is not a url check if it is a path
        elif self.is_valid_path(item):
            color = rgb(234, 84, 159)
        
        #If it is neither make the color of text red
        else:
            color = rgb(255, 255, 255)

        
        #--------------Set styling properties of search bar depending on what was entered-----------------
        color = QtGui.QColor(color)
        color_format = self.ui.textEdit.currentCharFormat()
        color_format.setForeground(color)
        self.ui.textEdit.setCurrentCharFormat(color_format)
        self.ui.textEdit.append(item)
        #-------------------------------------------------------------------------------------------------
        pass


    def print_Response(self,data):
        """
        This function shows the response after validating what was entered
        """

        for pair in self.nested_dict_pairs_iterator(data):
            self.ui.textEdit.insertPlainText('\n')
            for item in pair:
                self.customize_text(str(item))


    def loading_dataset_to_ui_old(self, stellar_account_url_link):
        """
        This function take stellar account url and get data from it
        """

        #---------------------------------Verify if link is valid-------------------------------------------
        self.customize_text('Initiated data loading from ')
        self.customize_text(stellar_account_url_link)
        #---------------------------------------------------------------------------------------------------


        #-------------------------------Get data of given stellar account-----------------------------------
        df = pd.read_json(stellar_account_url_link)
        #---------------------------------------------------------------------------------------------------


        # Put fethed data in a model
        model = PandasModel(df)
        self.ui.tableView.setModel(model)


        # dataframe output
        thread1=Thread(target=self.print_Response,args=(df.to_dict(),))
        thread1.start()


        # json output
        self.loading_json_old(stellar_account_url_link, df.to_json())

    def loading_dataset_to_ui(self, stellar_account_url_link):
        """
        This function take stellar account url and get data from it
        """
        # self.cba = CreatedByAccounts(stellar_account_url_link)
        
        thread1=Thread(target=self.initCall,args=(stellar_account_url_link,))
        thread1.start()

    def Button(self):
        """
        This function links all buttons with their respective functions
        """


        #--------------------Check if button gets clicked and perform function--------------------------
        btnWidget = self.sender()


        # Home button
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))


        # New user button
        if btnWidget.objectName() == "btn_new_user":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_user)
            UIFunctions.resetStyle(self, "btn_new_user")
            UIFunctions.labelPage(self, "New User")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # Widgets buttons
        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Settings")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))


    #----------------------------------------Events---------------------------------------------------

    def eventFilter(self, watched, event):
        """
        This function runs when double click of mouse left click is pressed
        """
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    
    def mousePressEvent(self, event):
        """
        This function runs whenever mouse click occurs
        """

        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
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
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        """
        This function displays new height and width whenever window is resized
        """

        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))

    #--------------------------------------------------------------------------------------------------


def runall():
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('/StellarMap/static/fonts/Cascadia.ttf')
    window = MainWindow()

    # default testnet network
    e = EnvHelpers()
    e.set_testnet_network()

    sys.exit(app.exec_())
