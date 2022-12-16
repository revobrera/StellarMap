import json
import os

import pandas as pd

try:
    
    from .helpers.data_output import DataOutput
    from .helpers.q_thread_generics import (
        GenericAppendCreatorToDfWorkerThread,
        GenericCheckInternetConnectivityWorkerThread,
        GenericCollectIssuersWorkerThread, GenericGetCreatorWorkerThread,
        GenericGetHomeDomainWorkerThread, GenericGetXLMBalanceWorkerThread,
        GenericParseOperationsWorkerThread,
        GenericReconstructCollectionIssuersWorkerThread,
        GenericRequestsWorkerThread)

except:
    from helpers.data_output import DataOutput
    from helpers.q_thread_generics import (
        GenericAppendCreatorToDfWorkerThread,
        GenericCheckInternetConnectivityWorkerThread,
        GenericCollectIssuersWorkerThread, GenericGetCreatorWorkerThread,
        GenericGetHomeDomainWorkerThread, GenericGetXLMBalanceWorkerThread,
        GenericParseOperationsWorkerThread,
        GenericReconstructCollectionIssuersWorkerThread,
        GenericRequestsWorkerThread)


class CreatedByAccounts(DataOutput):
    # swimming upstream crawl for creator accounts
    def initCall(self, stellar_account):

        #--------------------------- init variables for CreatedByAccounts()
        self.recursive_count = 0
        self.stellar_account = stellar_account
        self.current_stellar_account = None
        self.q_thread_headers = None
        self.q_thread_text = None
        self.q_thread_status_code = None
        self.q_thread_json = None
        self.q_thread_home_domain = None
        self.q_thread_account = None
        self.q_thread_creator_account = None
        self.q_thread_account_active = None
        self.q_thread_account_info = {}
        self.q_thread_xlm_balance = 0
        self.q_thread_df_row = {
            'Active': [],
            'Created': [],
            'Account': [],
            'Home Domain': [],
            'XLM Balance': [],
            'Stellar.Expert': []
        }
        self.creator_df = pd.DataFrame(self.q_thread_df_row)
        self.q_thread_is_user_internet_connected = False
        self.collection_issuers_dict = {}
        # self.initCall(stellar_account)

        #---------------------------

        # reset outputs when a new search is made by the user
        self.output_df("clear", reset_val=True)
        self.output_json("clear", reset_val=True)
        self.output_terminal("clear", reset_val=True)

        # creator accounts upstream crawl
        self.call_upstream_crawl_on_stellar_account(stellar_account)

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
            self.set_account_from_api(stellar_account, self.call_step_2_get_account_info, 'stellar_expert')
        else:
            # captures nan value
            self.call_step_8_concluding_upstream_crawl()

    def call_step_2_1_collect_stellar_expert_issuers(self):
        # collect stellar_expert json dictionary 

        # issuer_dict = {}
        # issuer_dict = self.q_thread_json
        # self.collection_issuers_dict['ISSUER_' + str(self.recursive_count)] = issuer_dict

        # dictionary appended to dataframe
        param_dict = {}
        param_dict = {
            "issuer_count": self.recursive_count,
            "issuer_data": self.q_thread_json,
            "issuer_cumulative_dict": self.collection_issuers_dict
        }

        self.q_thread_issuers = GenericCollectIssuersWorkerThread(param_dict)
        self.q_thread_issuers.start()
        self.q_thread_issuers.collected_issuers.connect(self.call_step_2_2_set_cumulative_issuers)

    def call_step_2_2_set_cumulative_issuers(self, collected_issuers):
        self.collection_issuers_dict = collected_issuers.copy()
        # self.output_json(json.dumps(self.collection_issuers_dict))

    def call_step_2_get_account_info(self):
        d_str = "QThread is on step 2: retrieving account info from stellar.expert"
        self.output_terminal(d_str)

        if self.q_thread_status_code == 404:
            # gracefully handling 404 errors and preventing the app to crash
            d_str_status = "ERROR: It is likely that you are searching for a stellar account that is no longer found on this network: " + str(os.getenv("NETWORK"))

            # self.output_description(d_str_status)
            self.output_terminal(d_str_status)

            # rerouting to end of algorithm
            self.call_step_9_graceful_exit()

        else:
            self.call_step_2_1_collect_stellar_expert_issuers()

            self.q_thread_creator = GenericGetCreatorWorkerThread(self.q_thread_json)
            self.q_thread_creator.start()
            self.q_thread_creator.q_thread_output_json.connect(self.call_step_3_1_print_output_json)
            self.q_thread_creator.q_thread_account_dict.connect(self.call_step_3_set_account_info)

    def call_step_3_set_account_info(self, q_thread_account_dict):
        d_str = "QThread is on step 3: setting account info to variables"
        self.output_terminal(d_str)

        self.q_thread_account_info = q_thread_account_dict.copy()

        self.q_thread_json = self.q_thread_account_info['json_str']
        self.q_thread_account = self.q_thread_account_info["account"]
        self.q_thread_account_active = self.q_thread_account_info["account_active"]
        self.q_thread_creator_account = self.q_thread_account_info["creator_account"]
        self.q_thread_created_datetime = self.q_thread_account_info["created"]

        # first recursive call is the starting stellar account
        # if self.recursive_count == 0:
        #     self.current_stellar_account = self.stellar_account
        # else:
        #     self.current_stellar_account = self.q_thread_account_info["creator_account"]

        # check if valid stellar address
        if self.is_valid_stellar_address(self.q_thread_account):
            self.set_account_from_api(self.q_thread_account, self.call_step_4_check_home_domain_element_exists, 'horizon')
        else:
            # captures nan value
            self.call_step_8_concluding_upstream_crawl()

    # def call_step_2_get_creator_from_account(self):
    #     d_str = "QThread is on step 2: retrieving and parsing the creator account from HTTPS response"
    #     self.output_terminal(d_str)

    #     if self.q_thread_status_code == 404:
    #         # gracefully handling 404 errors and preventing the app to crash
    #         d_str_status = "ERROR: It is likely that you are searching for a stellar account that is no longer found on this network: " + str(os.getenv("NETWORK"))

    #         # self.output_description(d_str_status)
    #         self.output_terminal(d_str_status)

    #         # rerouting to end of algorithm
    #         self.call_step_8_graceful_exit()

    #     else:
    #         self.q_thread_creator = GenericGetCreatorWorkerThread(self.q_thread_json)
    #         self.q_thread_creator.start()
    #         self.q_thread_creator.q_thread_output_json.connect(self.call_step_2_1_print_output_json)
    #         self.q_thread_creator.q_thread_account_dict.connect(self.call_step_2_2_check_creator_account)

    def call_step_3_3_collect_horizon_issuers(self, horizon_json):
        # collect horizon json dict 

        issuer_dict = {}
        issuer_dict = horizon_json

        if horizon_json:
            # join issuer stellar_expert and horizon issuers jsons
            if 'ISSUER_' + str(self.recursive_count) in self.collection_issuers_dict:
                self.collection_issuers_dict['ISSUER_' + str(self.recursive_count)].update(issuer_dict)
            else:
                self.collection_issuers_dict['ISSUER_' + str(self.recursive_count)] = issuer_dict
        else:
            self.output_terminal('HORIZON_JSON')
            self.output_terminal(horizon_json)


    def call_step_3_1_print_output_json(self, q_thread_output_json):
        d_str = "QThread is on step 3.1: printing out json"
        self.output_terminal(d_str)
        self.output_json(q_thread_output_json)
        

    # def call_step_2_2_check_creator_account(self, q_thread_account_dict):
    #     d_str = "QThread is on step 2.2: checking creator account"
    #     self.output_terminal(d_str)

    #     self.q_thread_account_info = q_thread_account_dict.copy()

    #     self.q_thread_account_active = self.q_thread_account_info["account_active"]
    #     self.q_thread_creator_account = self.q_thread_account_info["creator_account"]
    #     self.q_thread_created_datetime = self.q_thread_account_info["created"]

    #     # first recursive call is the starting stellar account
    #     if self.recursive_count == 0:
    #         self.current_stellar_account = self.stellar_account
    #     else:
    #         self.current_stellar_account = self.q_thread_account_info["creator_account"]

    #     # check if valid stellar address
    #     if self.is_valid_stellar_address(self.current_stellar_account):
    #         self.set_account_from_api(self.current_stellar_account, self.call_step_3_check_home_domain_element_exists, 'horizon')
    #     else:
    #         # captures nan value
    #         self.call_step_7_concluding_upstream_crawl()

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

    def call_step_4_check_home_domain_element_exists(self):
        d_str = "QThread is on step 4: checking if home_domain element of creator account exists from horizon api"
        self.output_terminal(d_str)

        self.call_step_3_3_collect_horizon_issuers(self.q_thread_json)

        if self.q_thread_status_code == 404:
            # gracefully handling 404 errors and preventing the app to crash
            d_str_status = "ERROR: It is likely that you are searching for a stellar account that is no longer found on this network: " + str(os.getenv("NETWORK"))

            # self.output_description(d_str_status)
            self.output_terminal(d_str_status)

            self.q_thread_home_domain = '404 Error: No home_domain element found!'
            self.q_thread_xlm_balance = '404 Error: No balances element found!'

            # rerouting to end of algorithm
            # self.call_step_9_graceful_exit()
            # benign condition --> keep the algorithm going
        
        self.q_thread_hd = GenericGetHomeDomainWorkerThread(self.q_thread_json)
        self.q_thread_hd.start()
        self.q_thread_hd.q_thread_home_domain.connect(self.call_step_4_1_print_hd)

    def call_step_4_1_print_hd(self, q_thread_home_domain):
        self.q_thread_home_domain = q_thread_home_domain
        d_str = "home_domain: " + str(self.q_thread_home_domain)
        self.output_terminal(d_str)

        self.call_step_5_check_xlm_balance_element_exists()

    def call_step_5_check_xlm_balance_element_exists(self):
        d_str = "QThread is on step 5: checking if xlm_balance element of creator account exists from horizon api"
        self.output_terminal(d_str)
        
        self.q_thread_xlm_balance = 0
        if 'balances' not in self.q_thread_json:
            self.q_thread_xlm_balance = 0
            
        self.call_step_6_get_xlm_balance_from_api()
        
    def call_step_6_get_xlm_balance_from_api(self):
        # print(get_pretty_json_string(res))
        # print(res['home_domain'])
        # print(res['last_modified_time'])
        # print(res['_links']['data']['href'])
        d_str = "QThread is on step 6: retrieving balances element from creator account from horizon api"
        self.output_terminal(d_str)

        self.q_thread_xlm = GenericGetXLMBalanceWorkerThread(self.q_thread_json)
        self.q_thread_xlm.start()
        self.q_thread_xlm.q_thread_xlm_balance.connect(self.call_step_6_1_print_xlm_balance)

    def call_step_6_1_print_xlm_balance(self, q_thread_xlm_balance):
        self.q_thread_xlm_balance = q_thread_xlm_balance
        d_str = "XLM Balance: " + str(self.q_thread_xlm_balance)
        self.output_terminal(d_str)

        self.output_terminal(self.q_thread_account_active)
        self.output_terminal(str(self.q_thread_created_datetime))

        self.call_step_7_append_creator_to_df()


    def call_step_7_append_creator_to_df(self):
        d_str = "QThread is on step 7: appending row dictionary row to pandas dataframe"
        self.output_terminal(d_str)

        # generating stellar.expert site
        stellar_expert_site_url = os.getenv('BASE_SITE_NETWORK_ACCOUNT') + str(self.q_thread_account_info["account"])

        d_str = "active: %s, created: %s, account: %s, creator: %s, home_domain: %s, XLM: %s, stellar.expert: %s" % (self.q_thread_account_info["account_active"], self.q_thread_created_datetime,
                                                                             self.q_thread_account_info["account"], self.q_thread_creator_account, self.q_thread_home_domain,
                                                                             self.q_thread_xlm_balance, stellar_expert_site_url)

        self.output_terminal(d_str)
        print(d_str)

        # dictionary appended to dataframe
        row_dict = {}
        row_dict = {
            "creator_df": self.creator_df,
            "account_active": self.q_thread_account_info["account_active"],
            "created": self.q_thread_created_datetime,
            "account": self.q_thread_account_info["account"],
            "creator_account": self.q_thread_creator_account,
            "home_domain": self.q_thread_home_domain,
            "xlm_balance": self.q_thread_xlm_balance,
            "stellar_expert_url": stellar_expert_site_url
        }

        self.q_thread_append_df = GenericAppendCreatorToDfWorkerThread(row_dict)
        self.q_thread_append_df.start()
        self.q_thread_append_df.q_thread_output_df.connect(self.call_step_7_1_print_df_and_recursive_upstream_crawl)

    def call_step_7_1_print_df_and_recursive_upstream_crawl(self, q_thread_output_df):
        # real time outupt df to data tab - in case the algorithm is disrupted it will still display results retrieved
        self.creator_df = q_thread_output_df
        self.output_df(self.creator_df)

        # checks if valid address
        if self.is_valid_stellar_address(self.q_thread_creator_account):
            # valid creator account
            # increments recursive count
            self.recursive_count = self.recursive_count + 1

            # recursive call
            self.call_upstream_crawl_on_stellar_account(self.q_thread_creator_account)
        else:
            # captures nan and exits
            self.call_step_8_concluding_upstream_crawl()
    
    def call_step_8_concluding_upstream_crawl(self):
        d_str = "QThread is on step 8: completed chaining algorithm to crawl upstream successfully \n"
        self.output_terminal(d_str)

        # Permanently changes the pandas settings
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        self.output_df(self.creator_df)

        # select columns to print
        print_df = self.creator_df[self.creator_df.columns[0:6]]
        #self.output_terminal(print_df.to_csv())
        self.output_json(print_df.to_json())

        self.output_terminal("done! \n " + "#"*49)

        self.call_step_9_graceful_exit()

    def call_step_9_graceful_exit(self):
        self.output_terminal("Gracefully Exiting! \n " + "#"*49)

        self.output_json(json.dumps(self.collection_issuers_dict))
        self.output_terminal(json.dumps(self.collection_issuers_dict))

        self.output_terminal("Gracefully Exiting! \n " + "#"*49)
        self.output_terminal(json.dumps(self.collection_issuers_dict))

        # self.collect_all_issuers()
        
        # exiting any running threads
        # self.stop_requests_thread()
        # self.stop_df_thread()
        # self.stop_json_thread()
        # self.stop_terminal_thread()
        # self.stop_append_df_thread()

    def collect_all_issuers(self):
        # loop through all issuer accounts
        # TODO refactor into a WorkerThread()

        for idx, row in self.creator_df.iterrows():
            # self.output_terminal(row['Account'])
            self.recursive_collect_operations_records(row['Account'])

    def recursive_collect_operations_records(self, issuer_account, cursor):
        horizon_operations_url = os.getenv('BASE_HORIZON_ACCOUNT') + str(issuer_account) + '/operations?cursor=' + cursor + '&limit=200&order=asc'
        self.q_thread = GenericRequestsWorkerThread(horizon_operations_url)
        self.q_thread.start()
        self.q_thread.requests_response.connect(self.collect_operations_records)
        self.q_thread.requests_response.connect(self.recursive_collect_operations_records)

    def collect_operations_records(self, requests_response):
        """Method to extract data from Horizon API and output to UI"""
        if requests_response is None:
            return None
        else:
            # check if more records
            if requests_response['_links']['next']:
                cursor = requests_response['_links']['next']['href'].split('cursor=')[1]
                self.recursive_collect_operations_records(issuer_account=self.ui.lineEdit.text(), cursor=cursor)

    
    def call_operations_records(self, requests_ops):
        # print info into terminal tab
        # self.q_thread_headers = requests_ops.headers
        # self.q_thread_text = requests_ops.text
        # self.q_thread_status_code = requests_ops.status_code
        # self.q_thread_json = requests_ops.json()

        # debug print
        d_str = "\n status_code: %d \n| headers: %s \n| text: %s \n| json: %s \n" % (requests_ops.status_code,
                                                                                     requests_ops.headers,
                                                                                     requests_ops.text,
                                                                                     requests_ops.json())

        # self.output_terminal(d_str)
        # self.output_terminal(requests_ops.json())

        # GenericParseOperationsWorkerThread based on account
        self.q_thread_parse_ops = GenericParseOperationsWorkerThread(requests_ops.json())
        self.q_thread_parse_ops.start()
        self.q_thread_parse_ops.cumulative_operations.connect(self.set_operations_records)

    def set_operations_records(self, ops_dict):
        # generates the children node for each ISSUER
        child_node = {}
        child_list = []
        child_list.append(ops_dict)
        child_node = {
            "children": child_list
        }
        if ops_dict:
            if 'ISSUER_' + str(self.recursive_count) in self.collection_issuers_dict:
                self.collection_issuers_dict['ISSUER_' + str(self.recursive_count)].update(child_node)
            else:
                self.collection_issuers_dict['ISSUER_' + str(self.recursive_count)] = child_node
        else:
            self.output_terminal('child_node was not created')

        self.format_issuers_to_radial_tree()

    def format_issuers_to_radial_tree(self):

         # dictionary appended to dataframe
        param_dict = {}
        param_dict = {
            "collection_issuers": self.collection_issuers_dict,
            "recursive_count": self.recursive_count
        }

        # formatting collection_issuers_dict into radial tree data structure
        self.q_thread_rt_format = GenericReconstructCollectionIssuersWorkerThread(param_dict)
        self.q_thread_rt_format.start()
        self.q_thread_rt_format.q_thread_radial_tree_data.connect(self.set_format_issuers_to_radial_tree)

    def set_format_issuers_to_radial_tree(self, radial_tree_data_dict):
        # convert dictionary to json str
        json_str = json.dumps(radial_tree_data_dict)

        self.output_json(json_str)


    #TODO recursively call collect_operations_records() from response _links.next.href



