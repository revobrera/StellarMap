import pandas as pd
import requests
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import json


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
    Generic Output Worker Thread To Display Output Description
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
    Generic Output Worker Thread To Display Output Dataframe
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
    Generic Output Worker Thread To Display Output JSON
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
    Generic Output Worker Thread To Display Output Terminal
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
