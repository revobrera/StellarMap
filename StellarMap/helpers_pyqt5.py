import json
import os
import sys
import time

import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

try:
    from .generics import (GenericDataframeOutputWorkerThread,
                           GenericDescriptionOutputWorkerThread,
                           GenericJSONOutputWorkerThread,
                           GenericRequestsWorkerThread,
                           GenericTerminalOutputWorkerThread)
    from .main_file import MainWindow, PandasModel
    from .settings.env import EnvHelpers
    from .ui_functions import UIFunctions
except:
    from generics import (GenericDataframeOutputWorkerThread,
                          GenericDescriptionOutputWorkerThread,
                          GenericJSONOutputWorkerThread,
                          GenericRequestsWorkerThread,
                          GenericTerminalOutputWorkerThread)
    from main_file import MainWindow, PandasModel
    from settings.env import EnvHelpers
    from ui_functions import UIFunctions


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

    def stop_requests_thread(self):
        self.GenericRequestsWorkerThread.stop()
        self.q_description.quit()
        self.q_description.wait()
    
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
        # d_description = DisplayOutput()
        # d_description
        # UIFunctions.labelDescription(self, q_thread_output_description)
        print(q_thread_output_description)

    def call_df_fn(self, q_thread_output_df):
        # do_df = DisplayOutput()
        # do_df.loading_df(q_thread_output_df)
        # MainWindow.loading_df(self, q_thread_output_df)
        print(q_thread_output_df)

    def call_json_fn(self, q_thread_output_json):
        # do_json = DisplayOutput()
        # do_json.loading_json(q_thread_output_json)
        # MainWindow.loading_json(self, q_thread_output_json)
        print(q_thread_output_json)
    
    def call_terminal_fn(self, q_thread_output_terminal):
        # do_terminal = DisplayOutput()
        # do_terminal.loading_terminal(q_thread_output_terminal)
        # MainWindow.customize_text(self, q_thread_output_terminal)
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
        self.q_thread.wait()

        # adding time delay to avoid rate limiting from stellar api service
        # time.sleep(1)
            

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
        d_str_f = "#"*49 + " \n %s" % d_str
        print(d_str)

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


def main():

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 200)
    w.move(300, 300)

    w.setWindowTitle('Simple')
    w.show()

    # set env
    # import settings file
    app_env = EnvHelpers()
    app_env.set_public_network()
    # app_env.set_testnet_network()

    #stellar_account = 'GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5'
    stellar_account = 'GCQTGZQQ5G4PTM2GL7CDIFKUBIPEC52BROAQIAPW53XBRJVN6ZJVTG6V'
    uc = CreatedByAccounts(stellar_account)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
