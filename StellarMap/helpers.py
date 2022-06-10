import pandas as pd
import requests
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot


class creatorAccountHelpers:
    def __init__(self):
        # set init variables

        upstream_creator_domain_list = []
        upstream_creator_domain_list = {}

        # count elements in the list
        creator_domain_iter = 0

    def increment_creator_domain_iter(self):
        creator_domain_iter = len(self.upstream_creator_domain_list) + 1

    def get_creator_domain_iter(self):
        return self.get_creator_domain_iter

    def append_upstream_creator_domain_list_to_list(self, creator_account, home_domain, xlm_balance):
        creator_domain_list = [
            self.get_creator_domain_iter(),
            str(creator_account),
            str(home_domain),
            str(xlm_balance) + ' XLM'
        ]

        self.upstream_creator_domain_list.append(creator_domain_dict)

    def get_upstream_creator_domain_list(self):
        return self.upstream_creator_domain_list

    def get_upstream_creator_domain_df(self):
        df = pd.DataFrame(self.upstream_creator_domain_list, columns = ['No.', 'creator_account', 'home_domain', 'xlm_balance'])  
        return df


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
        try:
            # use requests
            res = requests.get(self.url_link, timeout=3)

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
