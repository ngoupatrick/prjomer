import importlib as lib

from _backend._file_manager import *
from _config._config import *
from _backend._login_logout_user import *

sts = lib.import_module(CH_STREAMLIT_IMPORT)

def main_questionnaire(st):
    #show the questionnaires, if and only if he is log in
    if not is_connect():
        st.markdown(f":sweat: [{CH_MUST_BE_CONNECT}]", unsafe_allow_html=True)
        return    
    #show the questionnaires, if and only if the connected user group is mentorat or superviseur
    group_user = group_user_connect()
    if not group_user:
        st.markdown(f":sweat: [{CH_ACCESS_RIGHT}]")
        return    
    if not (group_user.lower() in [CH_MENTORAT.lower(), CH_SUPERVISEUR.lower()]):
        st.markdown(f":sweat: [{CH_ACCESS_RIGHT}]")
        return
    #everything is OKAY!!
    st.markdown('Veuillez utiliser ce lien pour acceder au questionnaire: [Questionnaire](https://ee.humanitarianresponse.info/x/exTcLaHt "crtl+click pour ouvrir dans un nouvel onglet").')