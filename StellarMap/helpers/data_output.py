import time

import pandas as pd

try:
    from .helpers.q_thread_generics import (
        GenericDataframeOutputWorkerThread,
        GenericDescriptionOutputWorkerThread, GenericJSONOutputWorkerThread,
        GenericTerminalOutputWorkerThread)

except:
    from helpers.q_thread_generics import (
        GenericDataframeOutputWorkerThread,
        GenericDescriptionOutputWorkerThread, GenericJSONOutputWorkerThread,
        GenericTerminalOutputWorkerThread)

class DataOutput:
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
