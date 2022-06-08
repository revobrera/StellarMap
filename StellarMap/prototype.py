
import os
import sys
import requests
from settings.env import envHelpers
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import (QThread, pyqtSignal, pyqtSlot)


class CustomClass():
    def __init__(self):
        super().__init__()
        
        self.initCall()

    def initCall(self):
        # stellar_account
        stellar_account = 'GAECL2FYQAMR2YFVCMOBBAIOOZGEAER6HART2MW7JWGNRDN53Q3S2WOB'
        
        # run q_thread
        self.set_account_from_stellar_expert(stellar_account)
    

    def set_account_from_stellar_expert(self, stellar_account):
            self.stellar_account_url = os.getenv('BASE_SE_NETWORK_ACCOUNT') + str(stellar_account)
            print('Running QThread: ' + str(self.stellar_account_url))
            # res = requests.get(self.stellar_account_url)
            self.q_thread = GenericRequestsWorkerThread(self.stellar_account_url)
            self.q_thread.start()
            self.q_thread.requests_response.connect(self.get_account_from_stellar_expert)

    def get_account_from_stellar_expert(self, requests_account):
        # print info into terminal tab
        print("\n headers: %s \n| text: %s \n| json: %s \n" % (requests_account.headers,
                                                                    requests_account.text,
                                                                    requests_account.json))

class GenericRequestsWorkerThread(QThread):
    """
    Generic HTTPS Requests Worker Thread
    """
    # the requests_response variable is the variable used to
    # emit the requests response to send out a signal out of the thread
    requests_response = pyqtSignal(requests.Response)

    def __init__(self, initial_https_url_link):
        super().__init__()
        self.url_link = initial_https_url_link

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