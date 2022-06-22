import json
import os
import time
from xmlrpc.client import boolean

import pandas as pd
import requests
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class GenericRequestsWorkerThread(QThread):
    """
    Generic HTTPS Requests Worker QThread
    """
    # the requests_response variable is the variable used to
    # emit the requests response to send out a signal out of the thread
    requests_response = pyqtSignal(requests.Response)

    def __init__(self, initial_https_url_link, slotOnFinished=None):
        super().__init__()
        self.url_link = initial_https_url_link

        if slotOnFinished:
            self.finished.connect(slotOnFinished)

    @pyqtSlot()
    def run(self):
        try:
            # use requests
            res = requests.get(self.url_link, timeout=3)

            print(res.text)

            # emit the response of the requests from the thread
            self.requests_response.emit(res)
            res.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("HTTP(S) Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("Uh Oh: Something broke... ",err)

        # exit thread
        return

    def send_url_link(self, https_url_link):
        self.url_link = https_url_link


class GenericDescriptionOutputWorkerThread(QThread):
    """
    Generic Output Worker QThread To Display Output Description
    """

    q_thread_output_description = pyqtSignal(str)

    def __init__(self, input_description):
        super().__init__()

        # labelDescription
        self.label_description = input_description

    @pyqtSlot()
    def run(self):
        # emit the description from the thread
        self.q_thread_output_description.emit(self.label_description)

        # exit thread
        return


class GenericDataframeOutputWorkerThread(QThread):
    """
    Generic Output Worker QThread To Display Output Dataframe
    """
    q_thread_output_df = pyqtSignal(pd.DataFrame)

    def __init__(self, input_df):
        super().__init__()

        self.input_df = input_df

    @pyqtSlot()
    def run(self):
        self.q_thread_output_df.emit(self.input_df)

        # exit thread
        return

class GenericJSONOutputWorkerThread(QThread):
    """
    Generic Output Worker QThread To Display Output JSON
    """
    q_thread_output_json = pyqtSignal(str)

    def __init__(self, input_json):
        super().__init__()

        self.input_json = input_json

    @pyqtSlot()
    def run(self):
        self.q_thread_output_json.emit(self.input_json)

        # exit thread
        return

class GenericTerminalOutputWorkerThread(QThread):
    """
    Generic Output Worker QThread To Display Output Terminal
    """
    q_thread_output_terminal = pyqtSignal(str)

    def __init__(self, input_terminal):
        super().__init__()

        self.input_terminal = input_terminal

    @pyqtSlot()
    def run(self):
        self.q_thread_output_terminal.emit(self.input_terminal)

        # exit thread
        return


class GenericGetCreatorWorkerThread(QThread):
    """
    Generic Worker QThread To Retrieve Creator Account
    """
    q_thread_output_json = pyqtSignal(str)
    q_thread_creator_account = pyqtSignal(str)
    

    def __init__(self, input_json):
        super().__init__()

        self.input_json = input_json

    @pyqtSlot()
    def run(self):
        # json string
        res_string = json.dumps(self.input_json)
        self.q_thread_output_json.emit(res_string)

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
            self.q_thread_creator_account.emit(str(row['creator']))
            

        # exit thread
        return


class GenericGetHomeDomainWorkerThread(QThread):
    """
    Generic Worker QThread To Retrieve Home Domain
    """
    q_thread_home_domain = pyqtSignal(str)

    def __init__(self, input_json):
        super().__init__()

        self.input_json = input_json

    @pyqtSlot()
    def run(self):

        home_domain_str = ""
        if 'home_domain' in self.input_json:
            # json string
            home_domain_str = json.dumps(self.input_json['home_domain'])

        else:
            home_domain_str = 'No home_domain element found.'

        self.q_thread_home_domain.emit(home_domain_str)

        # exit thread
        return


class GenericGetXLMBalanceWorkerThread(QThread):
    """
    Generic Worker QThread To Retrieve XLM Balance
    """
    q_thread_xlm_balance = pyqtSignal(str)

    def __init__(self, input_json):
        super().__init__()

        self.input_json = input_json

    @pyqtSlot()
    def run(self):

        try:
            # check if balances is a list or a string
            res_string = ''
            if isinstance(self.input_json['balances'], list):
                # iterate through list of assets
                for item in self.input_json['balances']:
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
                res_string = json.dumps(self.input_json['balances'])

            self.q_thread_xlm_balance.emit(res_string)
            
        except:
            # if resource is not available - most likely an account (deleted)
            self.q_thread_xlm_balance.emit('Account (deleted)')

        # exit thread
        return


class GenericAppendCreatorToDfWorkerThread(QThread):
    """
    Generic Worker QThread To Append Creator Account To DataFrame
    """
    q_thread_output_df = pyqtSignal(pd.DataFrame)

    def __init__(self, row_dict):
        super().__init__()

        # example of row_dict
        # row_dict = {"creator_df": pandas_dataframe_object
        #             "creator_account": "GCO2IP3MJNUOKS4PUDI4C7LGGMQDJGXG3COYX3WSB4HHNAHKYV5YL3VC",
        #             "home_domain": "No home domain element found",
        #             "xlm_balance": 4.9998397,
        #             "stellar_expert_url": "https://stellar.expert/explorer/public/account/GCO2IP3MJNUOKS4PUDI4C7LGGMQDJGXG3COYX3WSB4HHNAHKYV5YL3VC",
        #             }

        self.creator_df = row_dict['creator_df']
        self.creator_account = row_dict['creator_account']
        self.home_domain = row_dict['home_domain']
        self.xlm_balance = row_dict['xlm_balance']
        self.stellar_expert_url = row_dict['stellar_expert_url']

    @pyqtSlot()
    def run(self):
        # the list to append as row
        row_ls = [self.creator_account, self.home_domain,
                    self.xlm_balance, self.stellar_expert_url]

        # create a pandas series from the list
        row_s = pd.Series(row_ls, index=self.creator_df.columns)

        # append the row to the dataframe. [WARNING] .append would be deprecated soon, use .concat instead
        self.creator_df = self.creator_df.append(row_s, ignore_index=True)

        # emit the dataframe
        self.q_thread_output_df.emit(self.creator_df)

        print(self.creator_df)

        # exit thread
        return


class GenericCheckInternetConnectivityWorkerThread(QThread):
    """
    Generic Worker QThread To Check User Internet Connectivity
    """
    q_thread_is_connected = pyqtSignal(boolean)

    def __init__(self, sites_dict):
        super().__init__()

        # example of sites_dict
        # sites_dict = {
        #     "stellar_github": "https://github.com/stellar",
        #     "stellar_org": "https://www.stellar.org",
        #     "stellar_doc": "https://stellar-documentation.netlify.app/api/"
        # }

        self.q_threads_conn = {}
        self.sites_dict = sites_dict
        self.bool_val = False
        self.sites_bool_dict = {}
        self.output_bool_val = False

    @pyqtSlot()
    def run(self):
        print(self.sites_dict)

        # loop through dictionary
        for ky, vl in self.sites_dict.items():

            # call GenericRequestsWorkerThread() dynamically
            self.q_threads_conn[ky] = GenericRequestsWorkerThread(vl)
            self.q_threads_conn[ky].start()
            self.q_threads_conn[ky].requests_response.connect(self.is_connected)
            
            time.sleep(0.17)

            # assign boolean value to dict
            self.sites_bool_dict[ky] = self.bool_val

        print(self.sites_bool_dict)
        # loop through assigned boolean value dict
        for ky, vl in self.sites_bool_dict.items():
            # if one or more received 200 status code
            if vl is True:
                self.output_bool_val = True

        # emit connectivity
        self.q_thread_is_connected.emit(self.output_bool_val)

    def is_connected(self, requests_response):
        if requests_response.status_code == 200:
            self.bool_val = True
        else:
            self.bool_val = False
