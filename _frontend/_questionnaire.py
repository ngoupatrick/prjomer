import importlib as lib

from _backend._file_manager import *
from _config._config import *

sts = lib.import_module(CH_STREAMLIT_IMPORT)

def main_questionnaire(st):
    #st.write("Questionnaire")
    st.markdown('Veuillez utiliser ce lien pour acceder au questionnaire: [Questionnaire](https://ee.humanitarianresponse.info/x/exTcLaHt "crtl+click pour ouvrir dans un nouvel onglet").')