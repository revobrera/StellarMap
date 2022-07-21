import json
import time

import pandas as pd

try:
    from .helpers.data_model import PandasModel
    from .helpers.q_thread_generics import (
        GenericDataframeOutputWorkerThread,
        GenericDescriptionOutputWorkerThread, GenericJSONOutputWorkerThread,
        GenericTerminalOutputWorkerThread)

except:
    from helpers.data_model import PandasModel
    from helpers.q_thread_generics import (
        GenericDataframeOutputWorkerThread,
        GenericDescriptionOutputWorkerThread, GenericJSONOutputWorkerThread,
        GenericTerminalOutputWorkerThread)

class DataOutput:
    """Class DataOutput contains methods to output results data to the UI

    """    
    def call_description_fn(self, q_thread_output_description):
        """Method to call labelDescription() to set the single line notification on the UI

        Args:
            q_thread_output_description (str): line notification displayed to user shown on UI
        """
        self.labelDescription(q_thread_output_description)

    def call_df_fn(self, q_thread_output_df):
        """Method to set the model for tableView on the UPSTREAM CREATOR ACCOUNTS tab UI

        Args:
            q_thread_output_df (pd.Dataframe): dataset formatted as pandas dataframe
        """        
        # put fetched data in a model
        q_model = PandasModel(q_thread_output_df)
        self.ui.tableView.setModel(q_model)

    def call_json_fn(self, q_thread_output_json):
        """Method to append the json string on the JSON tab UI

        Args:
            q_thread_output_json (str): dataset formatted as json string
        """        
        self.ui.text_edit_json.acceptRichText()
        my_json_obj = json.loads(q_thread_output_json)
        my_json_str_formatted = json.dumps(my_json_obj, indent=4)
        self.ui.text_edit_json.append(my_json_str_formatted)
    
    def call_terminal_fn(self, q_thread_output_terminal):
        """Method to append the string on the TERMINAL tab UI

        Args:
            q_thread_output_terminal (str): dataset formatted as string for debugging and printing of data results
        """        
        self.ui.textEdit.append(q_thread_output_terminal)

    def reset_json_fn(self):
        self.ui.text_edit_json.clear()

    def reset_terminal_fn(self):
        self.ui.textEdit.clear()

    def output_description(self, input_txt):
        # create instance of GenericDescriptionOutputWorkerThread
        self.q_description = GenericDescriptionOutputWorkerThread(input_txt)
        self.q_description.q_thread_output_description.connect(self.call_description_fn)
        self.q_description.start()
        time.sleep(0.017)

    def output_df(self, input_df, reset_val=None):
        # create instance of GenericDataframeOutputWorkerThread

        if reset_val:
            # reset df in self
            self.q_thread_df_row = {
                'Active': [],
                'Created': [],
                'Account': [],
                'Home Domain': [],
                'XLM Balance': [],
                'Stellar.Expert': []
            }
            self.creator_df = pd.DataFrame(self.q_thread_df_row)
            input_df = self.creator_df
        
        self.q_df = GenericDataframeOutputWorkerThread(input_df)
        self.q_df.q_thread_output_df.connect(self.call_df_fn)
        self.q_df.start()
        time.sleep(0.017)

    def output_json(self, input_json_txt, reset_val=None):
        # create instance of GenericJSONOutputWorkerThread
        self.q_json = GenericJSONOutputWorkerThread(input_json_txt)
        if reset_val:
            self.q_json.q_thread_output_json.connect(self.reset_json_fn)
        else:
            self.q_json.q_thread_output_json.connect(self.call_json_fn)
        self.q_json.start()
        time.sleep(0.017)

    def output_terminal(self, input_txt, reset_val=None):
        # create instace of GenericTerminalOutputWorkerThread
        self.q_terminal = GenericTerminalOutputWorkerThread(input_txt)
        if reset_val:
            self.q_terminal.q_thread_output_terminal.connect(self.reset_terminal_fn)
        else:
            self.q_terminal.q_thread_output_terminal.connect(self.call_terminal_fn)
        self.q_terminal.start()
        time.sleep(0.017)
