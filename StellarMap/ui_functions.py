#Importing libraries for


import json  # Performing operating system operations
import os
import time

import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import (  # PyQt5 libraries and sub-libaries
    QPropertyAnimation, QSize, Qt)
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import (QGraphicsDropShadowEffect, QMainWindow,
                             QPushButton, QSizeGrip, QSizePolicy)

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
            self.cba = CreatedByAccounts(search_input) 

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

class CreatedByAccounts():
    def __init__(self, stellar_account):
        super().__init__()


        self.q_thread_headers = None
        self.q_thread_text = None
        self.q_thread_status_code = None
        self.q_thread_json = None
        self.q_thread_home_domain = None
        self.q_thread_creator_account = None
        self.q_thread_xlm_balance = 0
        self.q_thread_df_row = {
            'Creator Account': [],
            'Home Domain': [],
            'XLM Balance': [],
            'Stellar.Expert': []
        }
        self.creator_df = pd.DataFrame(self.q_thread_df_row)

        self.initCall(stellar_account)

    def initCall(self, stellar_account):
        
        # tesnet
        # stellar_account = 'GAIH3ULLFQ4DGSECF2AR555KZ4KNDGEKN4AFI4SU2M7B43MGK3QJZNSR'
        # stellar_account = 'GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5'

        # public
        # stellar_account = 'GCQTGZQQ5G4PTM2GL7CDIFKUBIPEC52BROAQIAPW53XBRJVN6ZJVTG6V' # contains a creator account that was deleted
        
        # run q_thread
        # self.set_account_from_api(stellar_account)

        # creator accounts upstream crawl
        self.call_upstream_crawl_on_stellar_account(stellar_account)

    def output_description(self, input_txt):
        # create instance of GenericDescriptionOutputWorkerThread
        self.q_description = GenericDescriptionOutputWorkerThread(input_txt)
        self.q_description.q_thread_output_description.connect(self.call_description_fn)
        self.q_description.start()
        time.sleep(1)
        # self.q_description.finished(self.stop_description_thread)

    def output_df(self, input_df):
        # create instance of GenericDataframeOutputWorkerThread
        self.q_df = GenericDataframeOutputWorkerThread(input_df)
        self.q_df.q_thread_output_df.connect(self.call_df_fn)
        self.q_df.start()
        time.sleep(1)
        # self.q_df.finished(self.stop_df_thread)

    def output_json(self, input_json_txt):
        # create instance of GenericJSONOutputWorkerThread
        self.q_json = GenericJSONOutputWorkerThread(input_json_txt)
        self.q_json.q_thread_output_json.connect(self.call_json_fn)
        self.q_json.start()
        time.sleep(1)
        # self.q_json.finished(self.stop_json_thread)

    def output_terminal(self, input_txt):
        # create instace of GenericTerminalOutputWorkerThread
        self.q_terminal = GenericTerminalOutputWorkerThread(input_txt)
        self.q_terminal.q_thread_output_terminal.connect(self.call_terminal_fn)
        self.q_terminal.start()
        time.sleep(1)
        # self.q_terminal.finished(self.stop_terminal_thread)

    def stop_description_thread(self):
        self.GenericDescriptionOutputWorkerThread.stop()
        self.q_description.quit()
        self.q_description.wait()

    def stop_df_thread(self):
        self.GenericDataframeOutputWorkerThread.stop()
        self.q_df.quit()
        self.q_df.wait()

    def stop_json_thread(self):
        self.GenericJSONOutputWorkerThread.stop()
        self.q_json.quit()
        self.q_json.wait()

    def stop_terminal_thread(self):
        self.GenericTerminalOutputWorkerThread.stop()
        self.q_terminal.quit()
        self.q_terminal.wait()

    def call_description_fn(self, q_thread_output_description):
        UIFunctions.labelDescription(self, q_thread_output_description)
        print(q_thread_output_description)

    def call_df_fn(self, q_thread_output_df):
        self.loading_df(self, q_thread_output_df)
        print(q_thread_output_df)

    def call_json_fn(self, q_thread_output_json):
        self.loading_json(self, q_thread_output_json)
        print(q_thread_output_json)
    
    def call_terminal_fn(self, q_thread_output_terminal):
        self.customize_text(self, q_thread_output_terminal)
        print(q_thread_output_terminal)



    def set_account_from_api(self, stellar_account, callback_fn, api_name):
        # print(api_name)
        if api_name == 'stellar_expert':
            # stellar.expert
            self.stellar_account_url = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(stellar_account)
        else:
            # horizon
            self.stellar_account_url = os.getenv('BASE_HORIZON_ACCOUNT') + str(stellar_account)

        progress_str = 'Running QThread: ' + str(self.stellar_account_url)
        print(progress_str)

        # res = requests.get(self.stellar_account_url)
        self.q_thread = GenericRequestsWorkerThread(self.stellar_account_url, callback_fn)
        self.q_thread.start()
        self.q_thread.requests_response.connect(self.get_account_from_api)
        
        # self.q_thread.finished.connect(self.stop_requests_thread)
        # self.q_thread.wait() # Destroyed Destroyed while thread is still running

        # adding time delay to avoid rate limiting from stellar api service
        # time.sleep(1)

    def stop_requests_thread(self):
        self.GenericRequestsWorkerThread.stop()
        self.q_thread.quit()
        self.q_thread.wait()     

    def get_account_from_api(self, requests_account):
        # print info into terminal tab
        self.q_thread_headers = requests_account.headers
        self.q_thread_text = requests_account.text
        self.q_thread_status_code = requests_account.status_code
        self.q_thread_json = requests_account.json()

        # debug print
        d_str = "\n status_code: %d \n| headers: %s \n| text: %s \n| json: %s \n" % (requests_account.status_code,
                                                                                     requests_account.headers,
                                                                                     requests_account.text,
                                                                                     requests_account.json())

        print(d_str)


    def call_upstream_crawl_on_stellar_account(self, stellar_account):
        # chaining method algorithm to crawl upstream and identify creator accounts
        d_str = "QThread is on step 0: init call to crawl upstream"
        d_str_f = "#"*49 + " \n%s" % d_str
        print(d_str_f)

        self.call_step_1_make_https_request(stellar_account)

    def call_step_1_make_https_request(self, stellar_account):
        d_str = "QThread is on step 1: making the HTTPS request"
        print(d_str)
        self.set_account_from_api(stellar_account, self.call_step_2_get_creator_from_account, 'stellar_expert')

    def call_step_2_get_creator_from_account(self):
        d_str = "QThread is on step 2: retreiving and parsing the creator account from HTTPS response"
        print(d_str)

        # json string
        res_string = json.dumps(self.q_thread_json)
        print(res_string)

        # reading json into df
        df = pd.read_json(res_string)

        # return a new dataframe by dropping a
        # row 'yearly' from dataframe
        df_monthly = df.drop('yearly')

        # adding abbrev columns
        df_monthly['account_abbrev'] = str(df_monthly['account'])[-6:]
        df_monthly['creator_abbrev'] = str(df_monthly['creator'])[-6:]

        # adding stellar.expert url
        df_monthly['account_url'] = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(df_monthly['account'])
        df_monthly['creator_url'] = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(df_monthly['creator'])
        
        # return creator
        for index, row in df_monthly.iterrows():
            print('Creator found: ' + str(row['creator']))
            # return row['creator']
            # use the creator account to check the home_domain element exists from the horizon api
            self.q_thread_creator_account = row['creator']
            if pd.isna(row['creator']):
                self.call_step_7_concluding_upstream_crawl()
            else:
                self.set_account_from_api(row['creator'], self.call_step_3_check_home_domain_element_exists, 'horizon')


    def call_step_3_check_home_domain_element_exists(self):
        d_str = "QThread is on step 3: checking if home_domain element of creator account exists from horizon api"
        print(d_str)
        
        self.q_thread_home_domain = ''
        # print(get_pretty_json_string(response_horizon.json()))
        if 'home_domain' in self.q_thread_json:
            # json string
            self.q_thread_home_domain = json.dumps(self.q_thread_json['home_domain'])

            # full json
            print(json.dumps(self.q_thread_json))
        else:
            self.q_thread_home_domain = 'No home_domain element found.'
            
        d_str = "home_domain: " + str(self.q_thread_home_domain)
        print(d_str)

        self.call_step_4_check_xlm_balance_element_exists()

    def call_step_4_check_xlm_balance_element_exists(self):
        d_str = "QThread is on step 4: checking if xlm_balance element of creator account exists from horizon api"
        print(d_str)
        
        self.q_thread_xlm_balance = 0

        if 'balances' not in self.q_thread_json:
            self.q_thread_xlm_balance = 0
            self.call_step_5_get_xlm_balance_from_api()
        else:
            self.call_step_5_get_xlm_balance_from_api()
        
    def call_step_5_get_xlm_balance_from_api(self):
        # print(get_pretty_json_string(res))
        # print(res['home_domain'])
        # print(res['last_modified_time'])
        # print(res['_links']['data']['href'])
        d_str = "QThread is on step 5: retrieving balances element from creator account from horizon api"
        print(d_str)

        try:
            # check if balances is a list or a string
            res_string = ''
            if isinstance(self.q_thread_json['balances'], list):
                # iterate through list of assets
                for item in self.q_thread_json['balances']:
                    # print(item)
                    # check if balance element exists
                    if 'asset_code' in item:
                        # print('inside an item with asset_code')
                        if item['asset_code'] == 'XLM':
                            res_string = item['balance']
                            # print('found XLM')
                            # print(item['balance'])
                    elif 'asset_type':
                        # print('inside an item with asset_type')
                        if item['asset_type'] == 'native':
                            res_string = item['balance']
                            # print('found XLM')
                            # print(item['balance'])
                    else:
                        # print('Element not found')
                        res_string = '0'
            
            else:
                # json string
                res_string = json.dumps(self.q_thread_json['balances'])

            self.q_thread_xlm_balance = res_string
            
        except:
            # if resource is not available - most likely an account (deleted)
            self.q_thread_xlm_balance = 'Account (deleted)'

        self.call_step_6_append_creator_to_df(self.q_thread_creator_account,
                                                self.q_thread_home_domain,
                                                self.q_thread_xlm_balance)


    def call_step_6_append_creator_to_df(self, creator_account, home_domain, xlm_balance):
        d_str = "QThread is on step 6: appending row dictionary row to pandas dataframe"
        print(d_str)

        # stellar.expert site
        stellar_expert_site_url = os.getenv('BASE_SITE_NETWORK_ACCOUNT') + str(creator_account)

        d_str = "creator: %s, home_domain: %s, XLM: %s, stellar.expert: %s" % (creator_account, home_domain,
                                                                             xlm_balance, stellar_expert_site_url)

        print(d_str)

        # the list to append as row
        row_ls = [creator_account, home_domain, xlm_balance, stellar_expert_site_url]

        # create a pandas series from the list
        row_s = pd.Series(row_ls, index=self.creator_df.columns)

        # append the row to the dataframe. [wARNING] .append would be deprecated soon, use .concat instead
        self.creator_df = self.creator_df.append(row_s, ignore_index=True)

        # real time outupt df to data tab - in case the algorithm is disrupted it will still display results retreived
        self.output_df(self.creator_df)

        # recursive call
        if pd.isna(creator_account) or self.q_thread_status_code == 'status_code: 200':
            self.call_step_7_concluding_upstream_crawl()
        else:
            self.call_upstream_crawl_on_stellar_account(creator_account)
    
    def call_step_7_concluding_upstream_crawl(self):
        d_str = "QThread is on step 7: completed chaining algorithm to crawl upstream successfully"
        print(d_str)

        # display max rows
        pd.set_option('display.max_rows', None)
        
        # adjust max column widths
        pd.set_option('display.max_colwidth', 0)
        self.output_df(self.creator_df)

        print("done! \n " + "#"*49)
