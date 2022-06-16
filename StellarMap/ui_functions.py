#Importing libraries for


import json  # Performing operating system operations
import os
import time

import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import (  # PyQt5 libraries and sub-libaries
    QAbstractTableModel, QPropertyAnimation, QSize, Qt)
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import (QGraphicsDropShadowEffect, QMainWindow,
                             QPushButton, QSizeGrip, QSizePolicy, QDialog)
from ui_main import Ui_MainWindow

try:
    from .env import EnvHelpers  # Settings file
    from .generics import (GenericDataframeOutputWorkerThread,
                           GenericDescriptionOutputWorkerThread,
                           GenericJSONOutputWorkerThread,
                           GenericRequestsWorkerThread,
                           GenericTerminalOutputWorkerThread)
    from .icons_rc import *
    from .ui_styles import *

except:
    from env import EnvHelpers  # Settings file
    from generics import (GenericDataframeOutputWorkerThread,
                          GenericDescriptionOutputWorkerThread,
                          GenericJSONOutputWorkerThread,
                          GenericRequestsWorkerThread,
                          GenericTerminalOutputWorkerThread)
    from icons_rc import *
    from ui_styles import *

#-------------------------------------Global variables-------------------------------------------
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
#------------------------------------------------------------------------------------------------

## ==> COUT INITIAL MENU
count = 1

class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        """
        This function initializes table model.
        It is a constuctor so it gets called when object is created in line ..
        """

        QAbstractTableModel.__init__(self)
        self._data = data


    def rowCount(self, parent=None):
        """
        Simply returns the number of rows of table when called
        """

        return self._data.shape[0]


    def columnCount(self, parnet=None):
        """
        This piece of code returns number of columns when called
        """

        return self._data.shape[1]


    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        This function returns the alignment of any object that gets passed in it
        """

        #Checking if passed object is valid
        if index.isValid():
            
            
            #If object is set to display role it returns the location of data in it
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])


            #Otherwise it goes to desired column and returns its alignment
            column_count = self.columnCount()

            for column in range(0, column_count):

                if (index.column() == column and role == Qt.ItemDataRole.TextAlignmentRole):
                    return Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter



        #If object is invalid  or desired column does not exist it returns None
        return None


    def headerData(self, col, orientation, role):
        """
        This function returns the location of header
        """

        #Return location if layout is horizontal and role is on display only mode
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]
        return None


    def setData(self, index, value, role):
        """
        This function sets value to a field
        """

        #Checker to see if given index location is valid
        if not index.isValid():
            return False

        #Checker to see if desired field is set on edit mode
        if role != Qt.ItemDataRole.EditRole:
            return False


        #Check if row number for desired index is valid
        row = index.row()
        if row < 0 or row >= len(self._data.values):
            return False


        #Check if column number for desired index is valid
        column = index.column()
        if column < 0 or column >= self._data.columns.size:
            return False

        
        #If all above conditions are true only then set value at given index
        self._data.iloc[row][column] = value
        self.dataChanged.emit(index, index)

        return True

    def flags(self, index):
        """
        This function basically sets the default windows button bar
        """

        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemFlag.ItemIsEditable
        flags |= Qt.ItemFlag.ItemIsSelectable
        flags |= Qt.ItemFlag.ItemIsEnabled
        flags |= Qt.ItemFlag.ItemIsDragEnabled
        flags |= Qt.ItemFlag.ItemIsDropEnabled

        return flags


class UIFunctions(QMainWindow):

    #---------------------------------Getting global variables---------------------------------------
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True
    #------------------------------------------------------------------------------------------------


    def maximize_restore(self):
        """
        This function takes window to maximize state and back to normal state
        Gets triggered when maximize button is clicked
        """

        global GLOBAL_STATE
        status = GLOBAL_STATE


        #If window is in normal state maximize it
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/16x16/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            self.ui.frame_size_grip.hide()

        #if window is in maximize state turn it back to normale
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/16x16/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            self.ui.frame_size_grip.show()

    
    def returnStatus(self):
        """
        This function checks if window is in normal state or full screen
        """
        return GLOBAL_STATE

    
    def setStatus(status):
        """
        This function sets the state of windows, either maximized or normal
        """
        
        global GLOBAL_STATE
        GLOBAL_STATE = status


    def enableMaximumSize(self, width, height):
        """
        This function sets maximum size of windows once it gets resized
        """

        #Check if height and width are not empty
        if width != '' and height != '':

            #If they are not, set current size as maximum size
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.hide()


    def toggleMenu(self, maxWidth, enable):
        """
        This function makes side menu appear
        """

        if enable:
            # Get current width
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            #-------------------------------------Set new width-------------------------------------

            #If menu is already 70 in width make it disappear
            if width == 70:
                widthExtended = maxExtend

            #If menu is not 70 in width make it appear
            else:
                widthExtended = standard
            #---------------------------------------------------------------------------------------


            #---------------------Set animation of appearing and disappearing-----------------------
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            #---------------------------------------------------------------------------------------

    #-----------------------------------Header functions-------------------------------------------- 
    def removeTitleBar(status):
        """
        This function removes header of given window
        """
        
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def labelTitle(self, text):
        """
        This function sets text of title window
        """
        self.ui.label_title_bar_top.setText(text)

    def labelDescription(self, q_thread_output_description):
        """
        This function sets the description
        """
        self.ui.label_top_info_1.setText(q_thread_output_description)
    #-----------------------------------------------------------------------------------------------
    

    #-------------------------------------Menu functions-------------------------------------------- 
    def addNewMenu(self, name, objName, icon, isTopMenu):
        """
        This function takes attributes as input and uses them to create a menu on runtime
        """
        
        font = QFont()
        font.setFamily(u"Cascadia")
        button = QPushButton(str(count),self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 70))
        button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.Button)

        if isTopMenu:                                       #If menu is at top put widgets on top
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)    #Otherwise put them on bottom

    def selectMenu(getStyle):
        """
        This function runs when an item is selected from menu
        """

        select = getStyle + ("QPushButton { border-right: 7px solid #00FF9C; }")
        return select

    def deselectMenu(getStyle):
        """
        This function runs when an item is deselected from menu
        """

        deselect = getStyle.replace("QPushButton { border-right: 7px solid #00FF9C; }", "")
        return deselect

    def selectStandardMenu(self, widget):
        """
        This function runs when selection starts
        """
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    def resetStyle(self, widget):
        """
        This function runs when selection stops
        """

        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    def labelPage(self, text):
        """
        This function changes page label
        """

        newText = '| ' + text.upper()
        self.ui.label_top_info_2.setText(newText)
    #-----------------------------------------------------------------------------------------------
    

    def userIcon(self, initialsTooltip, icon, showHide):
        """
        This function sets user icon along with text
        """

        if showHide:
            # Set text for user icon
            self.ui.label_user_icon.setText(initialsTooltip)

            # Set user icon
            if icon:
                style = self.ui.label_user_icon.styleSheet()
                setIcon = "QLabel { background-image: " + icon + "; }"
                self.ui.label_user_icon.setStyleSheet(style + setIcon)
                self.ui.label_user_icon.setText('')
                self.ui.label_user_icon.setToolTip(initialsTooltip)
        else:
            self.ui.label_user_icon.hide()

    def set_stellar_network(self):
        """
        This function takes network name from combobox and sets it
        """

        # get current selected text from combo box
        network_name = self.ui.networkComboBox.currentText()

        # set the label description to display network
        UIFunctions.labelDescription(self, 'Network: ' + network_name.upper())

        # import settings file
        app_env = EnvHelpers()
        if network_name.upper() == 'PUBLIC':
            app_env.set_public_network()
            
        else:
            app_env.set_testnet_network()

        self.customize_text('The network name was switched to: ' + os.getenv('NETWORK'))

    def search_creator_by_accounts(self):
        """
        Take address from search bar and search it on internet
        """

        # get input text from search bar
        search_input = self.ui.line_edit_search_input.text()

        # check if stellar address is valid
        if self.is_valid_stellar_address(search_input):
            search_str = 'Searched input is valid: ' + str(search_input)
            UIFunctions.labelDescription(self, search_str)
            self.customize_text(search_str)

            # call the function to walk up creator accounts
            self.customize_text('Searching on network: ' + os.getenv('BASE_SE_NETWORK_ACCOUNT'))
            stellar_account_url_link = os.getenv('BASE_SE_NETWORK_ACCOUNT') + search_input
            # self.loading_dataset_to_ui(stellar_account_url_link)
            self.loading_dataset_to_ui(search_input)
            # self.cba = CreatedByAccounts(search_input)

            # set env
            # import settings file
            # app_env = EnvHelpers()
            # app_env.set_public_network()
            # app_env.set_testnet_network()

            #stellar_account = 'GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5'
            # stellar_account = 'GCQTGZQQ5G4PTM2GL7CDIFKUBIPEC52BROAQIAPW53XBRJVN6ZJVTG6V'
            # uc = CreatedByAccounts(stellar_account)

        else:
            # print on ui and terminal then clear the search bar
            search_str = 'Searched input is NOT valid: ' + str(search_input)
            UIFunctions.labelDescription(self, search_str)
            self.customize_text(search_str)
            self.ui.line_edit_search_input.clear


    # ------------------------------ output functions ---------------------------------------
    # def description_feed(self, out_description):
    #     # labelDescription
    #     self.ui.label_top_info_1.setText(out_description)


        

    #-------------------------------GUI definitions------------------------------------------
    def uiDefinitions(self):
        
        
        def dobleClickMaximizeRestore(event):
            """
            If user double clicks top header maximize or minimize
            """
            
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))



        # Remove the default title bar
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()


        #------------------------------------Set shadow effects-----------------------------------
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)
        #-----------------------------------------------------------------------------------------


        #-------------------------------------Resize window---------------------------------------
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")
        #-----------------------------------------------------------------------------------------



        #------------------------------Maximize, Minimize and Close-------------------------------
        
        #Minimize        
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        #Maximize
        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        #Close
        self.ui.btn_close.clicked.connect(lambda: self.close())
    #-----------------------------------------------------------------------------------------

