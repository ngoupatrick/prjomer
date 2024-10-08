import importlib as lib
st = lib.import_module("streamlit")

from _config._config import *
from _config._components import *
from _frontend._sidebar import *
from _frontend._login_logout import *
from _frontend._acceuil import *
from _frontend._user_activity import *
from _frontend._mediatheque import *
from _frontend._profil import *
from _frontend._questionnaire import *

def hide_menu(st):
    
    hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}    
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            footer:after {
                content:'Projet OMER'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: gray;
                padding: 5px;
                top: 2px;
            }       
               
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def footer_end(st):    
    footer="""
        <style> footer:after {
                content:'Projet OMER'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: gray;
                padding: 5px;
                top: 2px;
            } </style>
        <div class='footer'>
            <p>the word you want to tell
            <a style='visibility: visible;display:block;position: relative;padding: 5px;top: 2px;text-align:center;' 
                href='https://www.streamlit.io' target='_blank'>your email address put here
            </a>
        </p></div>"""
    st.markdown(footer, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title=CH_APP,
        page_icon="🧊",
        initial_sidebar_state="collapsed"
    )
    #hide footer and header
    hide_menu(st=st)
    #st.title(":chart_with_upwards_trend: Dashboard page")
    #*******sidebar********#
    sbar = st.sidebar
    main_sidebar(st = st, sbar=sbar)
    
    rad_menu = get_global_session_objet(session=get_state(), key=KEY_SESSION_RADMENU)
    if rad_menu=="Accueil":
        #login
        main_login_logout(st)
        #load accueil if connect
        if is_connect(): load_accueil(st = st)        
    
    if rad_menu=='Dashboard': 
        load_user_activity(st = st)
            
    if rad_menu=='Médiathèque':        
        main_mediatheque(st=st)
        
    if rad_menu == 'Profil':        
        main_profil(st=st)
        
    if rad_menu == "Enquete":  
        main_questionnaire(st=st)  
        
    #add customize footer    
    #footer_end(st=st)
 
if __name__ == '__main__':
    main()