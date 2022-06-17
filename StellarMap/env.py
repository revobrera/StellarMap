import os


class EnvHelpers:
    def __init__(self):
        # set init environment variables
        self.set_testnet_network()

    def set_testnet_network(self):
        os.environ['DEBUG'] = 'True'
        os.environ['NETWORK'] = 'testnet'
        os.environ['BASE_HORIZON'] = 'https://horizon-testnet.stellar.org'
        self.set_base_network()

    def set_public_network(self):
        os.environ['DEBUG'] = 'False'
        os.environ['NETWORK'] = 'public'
        os.environ['BASE_HORIZON'] = 'https://horizon.stellar.org'
        self.set_base_network()

    def set_base_network(self):
        # stellar.expert site
        os.environ['BASE_SITE'] = 'https://stellar.expert'
        os.environ['BASE_SITE_NETWORK'] = os.getenv('BASE_SITE') + '/explorer/' + os.getenv('NETWORK')
        os.environ['BASE_SITE_NETWORK_ACCOUNT'] = os.getenv('BASE_SITE_NETWORK') + '/account/'

        # stellar.expert api
        os.environ['BASE_SE'] = 'https://api.stellar.expert'
        os.environ['BASE_SE_NETWORK'] = os.getenv('BASE_SE') + '/explorer/' + os.getenv('NETWORK')
        os.environ['BASE_SE_NETWORK_ACCOUNT'] = os.getenv('BASE_SE_NETWORK') + '/account/'
        os.environ['BASE_SE_NETWORK_DIR'] = os.getenv('BASE_SE_NETWORK') + '/directory/'

        # horizon
        os.environ['BASE_HORIZON_ACCOUNT'] = os.getenv('BASE_HORIZON') + '/accounts/'