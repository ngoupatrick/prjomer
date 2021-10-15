from _backend._session import *
from _backend._file_manager import *
from _backend._login_logout_user import *
from _config._config import *


from _frontend._user_activity import *
from _frontend._mediatheque import *
from _frontend._profil import *
from _frontend._questionnaire import *

def load_accueil(st):
    empty_bloc_accueil = st.empty()
    save_global_session_objet(session=get_state(), key=KEY_SESSION_COMPONENT_ACCUEIL, values=empty_bloc_accueil)
    
    username = get_global_session_objet(session=get_state(), key=KEY_SESSION_USERNAME)
    data_user = get_user_data_by_name(username=username)    
    if not data_user: return
    
    bloc_accueil = empty_bloc_accueil.container()    
    bloc_accueil.markdown(f":white_check_mark: Bienvenu {username}", unsafe_allow_html=True)
    
    key_structure = data_user["structure"]
    region, district, structure, type_sonu, type_structure = (CH_VIDE,)*5#CH_VIDE,CH_VIDE,CH_VIDE,CH_VIDE 
    if key_structure: 
        sonu = get_sonu_by_key(key=key_structure)
        if sonu:
            region = sonu.get('Region', CH_VIDE)
            district = sonu.get('District', CH_VIDE)
            structure = sonu.get('structure', CH_VIDE)
            type_sonu = sonu.get('type sonu', CH_VIDE)
            type_structure = sonu.get('type structure', CH_VIDE)
    
    #showing sonu information
    bloc_accueil.markdown(f"> ### <u>REGION</u>:  {region}", unsafe_allow_html=True)
    bloc_accueil.markdown(f"> ### <u>DISTRICT</u>:  {district}", unsafe_allow_html=True)
    bloc_accueil.markdown(f"> ### <u>STRUCTURE</u>:  {structure}", unsafe_allow_html=True)
    bloc_accueil.markdown(f"> ### <u>TYPE DE SONU</u>:  {type_sonu}", unsafe_allow_html=True)
    bloc_accueil.markdown(f"> ### <u>TYPE DE STRUCTURE</u>:  {type_structure}", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = bloc_accueil.columns(4)
    btn_visualiser = col1.button(label="Visualiser les données")
    btn_mediatheque = col2.button(label="Accéder à la Médiathèque")
    btn_enquette = col3.button(label="Accéder aux Enquêtes")
    btn_profil = col4.button(label="Gérer les profils utilisateurs")
    
    rad_menu = get_global_session_objet(session=get_state(), key=KEY_SESSION_RADMENU)
    
    if btn_visualiser:
        #if user is connect or not 
        load_user_activity(st = st)
        
    if btn_mediatheque:
        main_mediatheque(st=st)
        
    if btn_profil:
        main_profil(st=st)
        
    if btn_enquette:
        main_questionnaire(st=st)