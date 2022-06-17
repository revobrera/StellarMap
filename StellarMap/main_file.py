#Importing libraries for 

import datetime                 #   Managing date and time
import json                     #   Handling json format files
import platform                 #   Getting system information
import re                       #   Regular expressions (For putting checks on emails, names etc)
import sys                      #   To perform system level operations
from threading import Thread    #   To handle multiple threads (processes) at once

import pandas as pd             #   For managing and handling text data
from PIL.ImageQt import rgb     #   For managing and handling image data



#-----------------------------PyQt5 libraries and extensions----------------------------------

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

#----------------------------------------------------------------------------------------------


#----------------------------------Importing UI files------------------------------------------

try:
    from .app_modules import *
    from .icons_rc import *
    from .settings.env import EnvHelpers

except:
    from app_modules import *
    from icons_rc import *
    from settings.env import EnvHelpers

#----------------------------------------------------------------------------------------------




class MainWindow(QMainWindow):


    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """ Display system info"""

        print('System: ' + platform.system())
        print('Version: ' + platform.release())


        #--------------------------- init variables for CreatedByAccounts()
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

        # self.initCall(stellar_account)

        #---------------------------

        #----------------Remove top bar (The one with close, minimize and maximize buttons)----------------
        UIFunctions.removeTitleBar(True)
        #--------------------------------------------------------------------------------------------------

        #--------------------------------Set names of window-----------------------------------------------
        self.setWindowTitle('StellarMap [Prototype] - v0.1.2')
        UIFunctions.labelTitle(self, 'StellarMap [Prototype] - v0.1.2')
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




    def initCall(self, stellar_account):
        
        # tesnet
        # stellar_account = 'GAIH3ULLFQ4DGSECF2AR555KZ4KNDGEKN4AFI4SU2M7B43MGK3QJZNSR'
        # stellar_account = 'GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5'

        # public
        # stellar_account = 'GCQTGZQQ5G4PTM2GL7CDIFKUBIPEC52BROAQIAPW53XBRJVN6ZJVTG6V' # contains a creator account that was deleted
        
        # run q_thread
        # self.set_account_from_api(stellar_account)

        # reset outputs
        self.output_df("clear", reset_val=True)
        self.output_json("clear", reset_val=True)
        self.output_terminal("clear", reset_val=True)

        # creator accounts upstream crawl
        self.call_upstream_crawl_on_stellar_account(stellar_account)

    def output_description(self, input_txt):
        # create instance of GenericDescriptionOutputWorkerThread
        self.q_description = GenericDescriptionOutputWorkerThread(input_txt)
        self.q_description.q_thread_output_description.connect(self.call_description_fn)
        self.q_description.start()
        time.sleep(0.17)
        # self.q_description.finished(self.stop_description_thread)

    def output_df(self, input_df, reset_val=None):
        # create instance of GenericDataframeOutputWorkerThread

        if reset_val:
            # reset df in self
            self.q_thread_df_row = {
                'Creator Account': [],
                'Home Domain': [],
                'XLM Balance': [],
                'Stellar.Expert': []
            }
            self.creator_df = pd.DataFrame(self.q_thread_df_row)
            input_df = self.creator_df
        
        self.q_df = GenericDataframeOutputWorkerThread(input_df)
        self.q_df.q_thread_output_df.connect(self.call_df_fn)
        self.q_df.start()
        time.sleep(0.17)
        # self.q_df.finished(self.stop_df_thread)

    def output_json(self, input_json_txt, reset_val=None):
        # create instance of GenericJSONOutputWorkerThread
        self.q_json = GenericJSONOutputWorkerThread(input_json_txt)
        if reset_val:
            self.q_json.q_thread_output_json.connect(self.reset_json_fn)
        else:
            self.q_json.q_thread_output_json.connect(self.call_json_fn)
        self.q_json.start()
        time.sleep(0.17)
        # self.q_json.finished(self.stop_json_thread)

    def output_terminal(self, input_txt, reset_val=None):
        # create instace of GenericTerminalOutputWorkerThread
        self.q_terminal = GenericTerminalOutputWorkerThread(input_txt)
        if reset_val:
            self.q_terminal.q_thread_output_terminal.connect(self.reset_terminal_fn)
        else:
            self.q_terminal.q_thread_output_terminal.connect(self.call_terminal_fn)
        self.q_terminal.start()
        time.sleep(0.17)
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
        self.labelDescription(q_thread_output_description)
        # print(q_thread_output_description)

    def call_df_fn(self, q_thread_output_df):
        # put fetched data in a model
        q_model = PandasModel(q_thread_output_df)
        self.ui.tableView.setModel(q_model)

    def call_json_fn(self, q_thread_output_json):
        self.ui.text_edit_json.acceptRichText()
        my_json_obj = json.loads(q_thread_output_json)
        my_json_str_formatted = json.dumps(my_json_obj, indent=4)
        self.ui.text_edit_json.append(my_json_str_formatted)
    
    def call_terminal_fn(self, q_thread_output_terminal):
        self.ui.textEdit.append(q_thread_output_terminal)

    def reset_json_fn(self):
        self.ui.text_edit_json.clear()

    def reset_terminal_fn(self):
        self.ui.textEdit.clear()

    def set_account_from_api(self, stellar_account, callback_fn, api_name):
        # print(api_name)
        if api_name == 'stellar_expert':
            # stellar.expert
            self.stellar_account_url = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(stellar_account)
        else:
            # horizon
            self.stellar_account_url = os.getenv('BASE_HORIZON_ACCOUNT') + str(stellar_account)

        progress_str = 'Running QThread: ' + str(self.stellar_account_url)
        self.output_terminal(progress_str)

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

        self.output_json(json.dumps(requests_account.json()))
        self.output_terminal(d_str)


    def call_upstream_crawl_on_stellar_account(self, stellar_account):
        # chaining method algorithm to crawl upstream and identify creator accounts
        d_str = "QThread is on step 0: init call to crawl upstream"
        d_str_f = "#"*49 + " \n%s" % d_str
        self.output_terminal(d_str_f)

        self.call_step_1_make_https_request(stellar_account)

    def call_step_1_make_https_request(self, stellar_account):
        d_str = "QThread is on step 1: making the HTTPS request"
        self.output_terminal(d_str)
        self.set_account_from_api(stellar_account, self.call_step_2_get_creator_from_account, 'stellar_expert')

    def call_step_2_get_creator_from_account(self):
        d_str = "QThread is on step 2: retreiving and parsing the creator account from HTTPS response"
        self.output_terminal(d_str)

        self.q_thread_creator = GenericGetCreatorWorkerThread(self.q_thread_json)
        self.q_thread_creator.start()
        self.q_thread_creator.q_thread_output_json.connect(self.call_step_2_1_print_output_json)
        self.q_thread_creator.q_thread_creator_account.connect(self.call_step_2_2_check_creator_account)

    def call_step_2_1_print_output_json(self, q_thread_output_json):
        d_str = "QThread is on step 2.1: printing out json"
        self.output_terminal(d_str)
        self.output_json(q_thread_output_json)

    def call_step_2_2_check_creator_account(self, q_thread_creator_account):
        d_str = "QThread is on step 2.2: checking creator account"
        self.output_terminal(d_str)

        self.q_thread_creator_account = q_thread_creator_account

    
        # check if valid stellar address
        if self.is_valid_stellar_address(self.q_thread_creator_account):
            self.set_account_from_api(self.q_thread_creator_account, self.call_step_3_check_home_domain_element_exists, 'horizon')
        else:
            # captures nan value
            self.call_step_7_concluding_upstream_crawl()


    def call_step_3_check_home_domain_element_exists(self):
        d_str = "QThread is on step 3: checking if home_domain element of creator account exists from horizon api"
        self.output_terminal(d_str)
        
        self.q_thread_hd = GenericGetHomeDomainWorkerThread(self.q_thread_json)
        self.q_thread_hd.start()
        self.q_thread_hd.q_thread_home_domain.connect(self.call_step_3_1_print_hd)

    def call_step_3_1_print_hd(self, q_thread_home_domain):
        self.q_thread_home_domain = q_thread_home_domain
        d_str = "home_domain: " + str(self.q_thread_home_domain)
        self.output_terminal(d_str)

        self.call_step_4_check_xlm_balance_element_exists()

    def call_step_4_check_xlm_balance_element_exists(self):
        d_str = "QThread is on step 4: checking if xlm_balance element of creator account exists from horizon api"
        self.output_terminal(d_str)
        
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
        self.output_terminal(d_str)

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
        self.output_terminal(d_str)

        # stellar.expert site
        stellar_expert_site_url = os.getenv('BASE_SITE_NETWORK_ACCOUNT') + str(creator_account)

        d_str = "creator: %s, home_domain: %s, XLM: %s, stellar.expert: %s" % (creator_account, home_domain,
                                                                             xlm_balance, stellar_expert_site_url)

        self.output_terminal(d_str)

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
        self.output_terminal(d_str)

        # display max rows
        pd.set_option('display.max_rows', None)
        
        # adjust max column widths
        pd.set_option('display.max_colwidth', 0)
        self.output_df(self.creator_df)

        self.output_terminal("done! \n " + "#"*49)


def runall():
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('/StellarMap/fonts/Cascadia.ttf')
    window = MainWindow()

    e = EnvHelpers()
    e.set_testnet_network()

    sys.exit(app.exec_())
