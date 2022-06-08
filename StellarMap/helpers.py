import pandas as pd

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