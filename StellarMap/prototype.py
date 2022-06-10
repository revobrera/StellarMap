import json
import os
import sys
import time

import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget # PyQt5 will not work with this QThread algorithm

from helpers import GenericRequestsWorkerThread
from settings.env import envHelpers


class CustomClass():
    def __init__(self):
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
        
        self.initCall()

    def initCall(self):
        
        # tesnet
        # stellar_account = 'GAIH3ULLFQ4DGSECF2AR555KZ4KNDGEKN4AFI4SU2M7B43MGK3QJZNSR'
        stellar_account = 'GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5'

        # public
        # stellar_account = 'GCQTGZQQ5G4PTM2GL7CDIFKUBIPEC52BROAQIAPW53XBRJVN6ZJVTG6V' # contains a creator account that was deleted
        
        # run q_thread
        # self.set_account_from_api(stellar_account)

        # creator accounts upstream crawl
        self.call_upstream_crawl_on_stellar_account(stellar_account)

    def set_account_from_api(self, stellar_account, callback_fn, api_name):
        # print(api_name)
        if api_name == 'stellar_expert':
            # stellar.expert
            self.stellar_account_url = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(stellar_account)
        else:
            # horizon
            self.stellar_account_url = os.getenv('BASE_HORIZON_ACCOUNT') + str(stellar_account)

        print('Running QThread: ' + str(self.stellar_account_url))
        # res = requests.get(self.stellar_account_url)
        self.q_thread = GenericRequestsWorkerThread(self.stellar_account_url, callback_fn)
        self.q_thread.start()
        self.q_thread.requests_response.connect(self.get_account_from_api)

        # adding time delay to avoid rate limiting from stellar api service
        time.sleep(1)
            

    def get_account_from_api(self, requests_account):
        # print info into terminal tab
        self.q_thread_headers = requests_account.headers
        self.q_thread_text = requests_account.text
        self.q_thread_status_code = requests_account.status_code
        self.q_thread_json = requests_account.json()

        # debug print
        # print("\n status_code: %d \n| headers: %s \n| text: %s \n| json: %s \n" % (requests_account.status_code,
        #                                                                             requests_account.headers,
        #                                                                             requests_account.text,
        #                                                                             requests_account.json()))


    def call_upstream_crawl_on_stellar_account(self, stellar_account):
        # chaining method algorithm to crawl upstream and identify creator accounts
        print("#################################################")
        print("QThread is on step 0: init call to crawl upstream")
        self.call_step_1_make_https_request(stellar_account)

    def call_step_1_make_https_request(self, stellar_account):
        print("QThread is on step 1: making the HTTPS request")
        self.set_account_from_api(stellar_account, self.call_step_2_get_creator_from_account, 'stellar_expert')

    def call_step_2_get_creator_from_account(self):
        print("QThread is on step 2: retreiving and parsing the creator account from HTTPS response")

        # json string
        res_string = json.dumps(self.q_thread_json)

        # reading json into pdf
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
                self.call_step_8_concluding_upstream_crawl()
            else:
                self.set_account_from_api(row['creator'], self.call_step_3_check_home_domain_element_exists, 'horizon')


    def call_step_3_check_home_domain_element_exists(self):
        print("QThread is on step 3: checking if home_domain element of creator account exists from horizon api")
        self.q_thread_home_domain = ''
        # print(get_pretty_json_string(response_horizon.json()))
        if 'home_domain' in self.q_thread_json:
            # json string
            self.q_thread_home_domain = json.dumps(self.q_thread_json['home_domain'])
        else:
            self.q_thread_home_domain = 'No home_domain element found.'
            
        print('home_domain: ' + self.q_thread_home_domain)
        self.set_account_from_api(self.q_thread_creator_account, self.call_step_4_get_home_domain_from_api, 'horizon')

    def call_step_4_get_home_domain_from_api(self):
        print("QThread is on step 4: retrieving home_domain element from creator account from horizon api")
        self.set_account_from_api(self.q_thread_creator_account, self.call_step_5_check_xlm_balance_element_exists, 'horizon')

    def call_step_5_check_xlm_balance_element_exists(self):
        print("QThread is on step 5: checking if xlm_balance element of creator account exists from horizon api")
        self.q_thread_xlm_balance = 0

        if 'balances' not in self.q_thread_json:
            self.q_thread_xlm_balance = 0
            self.call_step_6_get_xlm_balance_from_api()
        else:
            self.set_account_from_api(self.q_thread_creator_account, self.call_step_6_get_xlm_balance_from_api, 'horizon')
        
    def call_step_6_get_xlm_balance_from_api(self):
        # print(get_pretty_json_string(res))
        # print(res['home_domain'])
        # print(res['last_modified_time'])
        # print(res['_links']['data']['href'])
        print("QThread is on step 6: retrieving balances element from creator account from horizon api")

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

        self.call_step_7_append_creator_to_df(self.q_thread_creator_account,
                                                self.q_thread_home_domain,
                                                self.q_thread_xlm_balance)


    def call_step_7_append_creator_to_df(self, creator_account, home_domain, xlm_balance):
        print("QThread is on step 7: appending row dictionary row to pandas dataframe")
        
        # print("creator: %s, home_domain: %s, XLM: %s, stellar.expert: %s" % (creator_account, home_domain,
        #                                                                      xlm_balance, stellar_expert_url))

        # stellar.expert site
        stellar_expert_site_url = os.getenv('BASE_SITE_NETWORK_ACCOUNT') + str(creator_account)

        # the list to append as row
        row_ls = [creator_account, home_domain, xlm_balance, stellar_expert_site_url]

        # create a pandas series from the list
        row_s = pd.Series(row_ls, index=self.creator_df.columns)

        # append the row to the dataframe. [wARNING] .append would be deprecated soon, use .concat instead
        self.creator_df = self.creator_df.append(row_s, ignore_index=True)

        # real time outupt df to data tab - in case the algorithm is disrupted it will still display results retreived
        print(self.creator_df)

        # recursive call
        if pd.isna(creator_account) or self.q_thread_status_code == 'status_code: 200':
            self.call_step_8_concluding_upstream_crawl()
        else:
            self.call_upstream_crawl_on_stellar_account(creator_account)
    
    def call_step_8_concluding_upstream_crawl(self):
        print("QThread is on step 8: completed chaining algorithm to crawl upstream successfully")

        # display max rows
        pd.set_option('display.max_rows', None)
        
        # adjust max column widths
        pd.set_option('display.max_colwidth', 0)
        print(self.creator_df)


def main():

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 200)
    w.move(300, 300)

    w.setWindowTitle('Simple')
    w.show()

    # set env
    # import settings file
    app_env = envHelpers()
    # app_env.set_public_network()
    app_env.set_testnet_network()

    
    cm = CustomClass()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
