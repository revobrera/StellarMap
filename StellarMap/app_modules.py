try:
    from .ui_main import Ui_MainWindow # GUI FILE
    from .ui_styles import Style # IMPORT QSS CUSTOM
    from .ui_functions import * # IMPORT FUNCTIONS

except:
    from ui_main import Ui_MainWindow
    from ui_styles import Style
    from ui_functions import *
