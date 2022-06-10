
try:
    # GUI FILE
    from .ui_main import Ui_MainWindow

    # IMPORT QSS CUSTOM
    from .ui_styles import Style

    # IMPORT FUNCTIONS
    from .ui_functions import *

except:
    # GUI FILE
    from ui_main import Ui_MainWindow

    # IMPORT QSS CUSTOM
    from ui_styles import Style

    # IMPORT FUNCTIONS
    from ui_functions import *
