import json
import os
import sys

import pandas as pd
import requests
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QWidget

from settings.env import envHelpers


class CustomClass():
    def __init__(self):
        super().__init__()

        self.q_thread_headers = None
        self.q_thread_text = None
        self.q_thread_status_code = None
        self.q_thread_json = None
        
        self.initCall()

    def initCall(self):
        # stellar_account
        stellar_account = 'GAECL2FYQAMR2YFVCMOBBAIOOZGEAER6HART2MW7JWGNRDN53Q3S2WOB'
        
        # run q_thread
        # self.set_account_from_stellar_expert(stellar_account)
        self.get_creator_from_account(stellar_account)
    

    def set_account_from_stellar_expert(self, stellar_account, callback_fn):
            self.stellar_account_url = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(stellar_account)
            print('Running QThread: ' + str(self.stellar_account_url))
            # res = requests.get(self.stellar_account_url)
            self.q_thread = GenericRequestsWorkerThread(self.stellar_account_url, callback_fn)
            self.q_thread.start()
            self.q_thread.requests_response.connect(self.get_account_from_stellar_expert)
            

    def get_account_from_stellar_expert(self, requests_account):
        # print info into terminal tab
        self.q_thread_headers = requests_account.headers
        self.q_thread_text = requests_account.text
        self.q_thread_status_code = requests_account.status_code
        self.q_thread_json = requests_account.json()

        print("\n status_code: %d \n| headers: %s \n| text: %s \n| json: %s \n" % (requests_account.status_code,
                                                                                    requests_account.headers,
                                                                                    requests_account.text,
                                                                                    requests_account.json()))

    def thread_has_finished(self):
        print("Thread has finished.")
        print(
            self.q_thread,
            self.q_thread.isRunning(),
            self.q_thread.isFinished(),
        )

    def get_creator_from_account(self, stellar_account):
        self.set_account_from_stellar_expert(stellar_account, self.thread_has_finished)

        # res = get_account_from_stellar_expert(stellar_account)
        # res = self.q_thread_response
        

        # json string
        # res_string = json.dumps(self.q_thread_json)
        print('printing q thread text')
        # res_string = json.dumps(self.q_thread_json)

        # reading json into pdf
        # df = pd.read_json(res_string)

        # # return a new dataframe by dropping a
        # # row 'yearly' from dataframe
        # df_monthly = df.drop('yearly')

        # # adding abbrev columns
        # df_monthly['account_abbrev'] = str(df_monthly['account'])[-6:]
        # df_monthly['creator_abbrev'] = str(df_monthly['creator'])[-6:]

        # # adding stellar.expert url
        # df_monthly['account_url'] = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(df_monthly['account'])
        # df_monthly['creator_url'] = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(df_monthly['creator'])

        # # display(df_monthly)
        
        # # return creator
        # for index, row in df_monthly.iterrows():
        #     print('Creator found: ' + str(row['creator']))
        #     return row['creator']

class GenericRequestsWorkerThread(QThread):
    """
    Generic HTTPS Requests Worker Thread
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
        # use requests
        res = requests.get(self.url_link)

        # emit the response of the requests from the thread
        self.requests_response.emit(res)

        # exit thread
        return

    def send_url_link(self, https_url_link):
        self.url_link = https_url_link


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
