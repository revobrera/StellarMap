import json
import os
import time

import pandas as pd

try:
    from .helpers.custom_pandas import PandasModel
    from .helpers.generics import (
        GenericAppendCreatorToDfWorkerThread,
        GenericCheckInternetConnectivityWorkerThread,
        GenericDataframeOutputWorkerThread,
        GenericDescriptionOutputWorkerThread, GenericGetCreatorWorkerThread,
        GenericGetHomeDomainWorkerThread, GenericGetXLMBalanceWorkerThread,
        GenericJSONOutputWorkerThread, GenericRequestsWorkerThread,
        GenericTerminalOutputWorkerThread)

except:
    from helpers.custom_pandas import PandasModel
    from helpers.generics import (GenericAppendCreatorToDfWorkerThread,
                                  GenericCheckInternetConnectivityWorkerThread,
                                  GenericDataframeOutputWorkerThread,
                                  GenericDescriptionOutputWorkerThread,
                                  GenericGetCreatorWorkerThread,
                                  GenericGetHomeDomainWorkerThread,
                                  GenericGetXLMBalanceWorkerThread,
                                  GenericJSONOutputWorkerThread,
                                  GenericRequestsWorkerThread,
                                  GenericTerminalOutputWorkerThread)


class CreatedByAccounts:
    # swimming upstream crawl for creator accounts
    def initCall(self, stellar_account):

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
        self.q_thread_is_user_internet_connected = False
        # self.initCall(stellar_account)

        #---------------------------

        # reset outputs when a new search is made by the user
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
        time.sleep(0.0017)

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
        time.sleep(0.0017)

    def output_json(self, input_json_txt, reset_val=None):
        # create instance of GenericJSONOutputWorkerThread
        self.q_json = GenericJSONOutputWorkerThread(input_json_txt)
        if reset_val:
            self.q_json.q_thread_output_json.connect(self.reset_json_fn)
        else:
            self.q_json.q_thread_output_json.connect(self.call_json_fn)
        self.q_json.start()
        time.sleep(0.0017)

    def output_terminal(self, input_txt, reset_val=None):
        # create instace of GenericTerminalOutputWorkerThread
        self.q_terminal = GenericTerminalOutputWorkerThread(input_txt)
        if reset_val:
            self.q_terminal.q_thread_output_terminal.connect(self.reset_terminal_fn)
        else:
            self.q_terminal.q_thread_output_terminal.connect(self.call_terminal_fn)
        self.q_terminal.start()
        time.sleep(0.0017)

    def stop_requests_thread(self):
        if self.q_thread.isRunning():
            self.q_thread.stop()
            self.q_thread.quit()
            self.q_thread.wait() 

    def stop_description_thread(self):
        if self.q_description.isRunning():
            self.q_description.stop()
            self.q_description.quit()
            self.q_description.wait()

    def stop_df_thread(self):
        if self.q_df.isRunning():
            self.q_df.stop()
            self.q_df.quit()
            self.q_df.wait()

    def stop_json_thread(self):
        if self.q_json.isRunning():
            self.q_json.stop()
            self.q_json.quit()
            self.q_json.wait()

    def stop_terminal_thread(self):
        if self.q_terminal.isRunning():
            self.q_terminal.stop()
            self.q_terminal.quit()
            self.q_terminal.wait()

    def stop_append_df_thread(self):
        if self.q_thread_creator.isRunning():
            self.q_thread_creator.stop()
            self.q_thread_creator.quit()
            self.q_thread_creator.wait()

    def call_description_fn(self, q_thread_output_description):
        self.labelDescription(q_thread_output_description)

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

    def check_user_internet(self):

        # dictionary of sites to check connectivity
        sites_dict = {
            "stellar_github": "https://github.com/stellar",
            "stellar_org": "https://www.stellar.org",
            "stellar_doc": "https://stellar-documentation.netlify.app/api/"
        }

        self.q_thread_conn = GenericCheckInternetConnectivityWorkerThread(sites_dict)
        self.q_thread_conn.start()
        self.q_thread_conn.q_thread_is_connected.connect(self.is_user_internet_on)

    def is_user_internet_on(self, q_thread_is_connected):
        self.q_thread_is_user_internet_connected = q_thread_is_connected

        if self.q_thread_is_user_internet_connected:
            print("ONLINE")
        else:
            print("OFFLINE")

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

        # check if valid stellar address
        if self.is_valid_stellar_address(stellar_account):
            self.set_account_from_api(stellar_account, self.call_step_2_get_creator_from_account, 'stellar_expert')
        else:
            # captures nan value
            self.call_step_7_concluding_upstream_crawl()

    def call_step_2_get_creator_from_account(self):
        d_str = "QThread is on step 2: retrieving and parsing the creator account from HTTPS response"
        self.output_terminal(d_str)

        if self.q_thread_status_code == 404:
            # gracefully handling 404 errors and preventing the app to crash
            d_str_status = "ERROR: It is likely that you are searching for a stellar account that is no longer found on this network: " + str(os.getenv("NETWORK"))

            # self.output_description(d_str_status)
            self.output_terminal(d_str_status)

            # rerouting to end of algorithm
            self.call_step_8_graceful_exit()

        else:
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

    # DO NOT uncomment this def! #################################################################################
    # The code is able to continue even when a 404 error is encountered to identify the subsequent creator(s) of the account.
    # Otherwise, the code exits when the first 404 error is encountered, which is not what we want.
    # The 404 error code from the Horizon API is a result of an account being deleted from the network.
    # We are recursively swimming upstream to identify all creator accounts INCLUDING all deleted accounts.
    # def call_step_2_3_handle_404_errors(self):
    #     d_str = "QThread is on step 2.3: handling 404 errors from response"
    #     self.output_terminal(d_str)

    #     if self.q_thread_status_code == 404:
    #         # gracefully handling 404 errors and preventing the app to crash
    #         d_str_status = "ERROR: It is likely that you are searching for a stellar account that is no longer found on this network: " + str(os.getenv("NETWORK"))

    #         # self.output_description(d_str_status)
    #         self.output_terminal(d_str_status)

    #         # rerouting to end of algorithm
    #         self.call_step_8_graceful_exit()
    #     else:
    #         self.call_step_3_check_home_domain_element_exists()
    # DO NOT uncomment this def! #################################################################################

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
        
    def call_step_5_get_xlm_balance_from_api(self):
        # print(get_pretty_json_string(res))
        # print(res['home_domain'])
        # print(res['last_modified_time'])
        # print(res['_links']['data']['href'])
        d_str = "QThread is on step 5: retrieving balances element from creator account from horizon api"
        self.output_terminal(d_str)

        self.q_thread_xlm = GenericGetXLMBalanceWorkerThread(self.q_thread_json)
        self.q_thread_xlm.start()
        self.q_thread_xlm.q_thread_xlm_balance.connect(self.call_step_5_1_print_xlm_balance)

    def call_step_5_1_print_xlm_balance(self, q_thread_xlm_balance):
        self.q_thread_xlm_balance = q_thread_xlm_balance
        d_str = "XLM Balance: " + str(self.q_thread_xlm_balance)
        self.output_terminal(d_str)

        self.call_step_6_append_creator_to_df()


    def call_step_6_append_creator_to_df(self):
        d_str = "QThread is on step 6: appending row dictionary row to pandas dataframe"
        self.output_terminal(d_str)

        # generating stellar.expert site
        stellar_expert_site_url = os.getenv('BASE_SITE_NETWORK_ACCOUNT') + str(self.q_thread_creator_account)

        d_str = "creator: %s, home_domain: %s, XLM: %s, stellar.expert: %s" % (self.q_thread_creator_account, self.q_thread_home_domain,
                                                                             self.q_thread_xlm_balance, stellar_expert_site_url)

        self.output_terminal(d_str)

        # dictionary appended to dataframe
        row_dict = {
            "creator_df": self.creator_df,
            "creator_account": self.q_thread_creator_account,
            "home_domain": self.q_thread_home_domain,
            "xlm_balance": self.q_thread_xlm_balance,
            "stellar_expert_url": stellar_expert_site_url
        }

        self.q_thread_append_df = GenericAppendCreatorToDfWorkerThread(row_dict)
        self.q_thread_append_df.start()
        self.q_thread_append_df.q_thread_output_df.connect(self.call_step_6_1_print_df_and_recursive_upstream_crawl)

    def call_step_6_1_print_df_and_recursive_upstream_crawl(self, q_thread_output_df):
        # real time outupt df to data tab - in case the algorithm is disrupted it will still display results retrieved
        self.creator_df = q_thread_output_df
        self.output_df(self.creator_df)

        # checks if valid address
        if self.is_valid_stellar_address(self.q_thread_creator_account):
            # valid creator account
            # recursive call
            self.call_upstream_crawl_on_stellar_account(self.q_thread_creator_account)
        else:
            # captures nan and exits
            self.call_step_7_concluding_upstream_crawl()
    
    def call_step_7_concluding_upstream_crawl(self):
        d_str = "QThread is on step 7: completed chaining algorithm to crawl upstream successfully \n"
        self.output_terminal(d_str)

        # Permanently changes the pandas settings
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        self.output_df(self.creator_df)

        # select columns to print
        print_df = self.creator_df[self.creator_df.columns[0:3]]
        self.output_terminal(print_df.to_csv())

        self.output_terminal("done! \n " + "#"*49)

        self.call_step_8_graceful_exit()

    def call_step_8_graceful_exit(self):
        self.output_terminal("Gracefully Exiting! \n " + "#"*49)

        # exiting any running threads
        # self.stop_requests_thread()
        # self.stop_df_thread()
        # self.stop_json_thread()
        # self.stop_terminal_thread()
        # self.stop_append_df_thread()
