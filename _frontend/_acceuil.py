from _backend._session import *
from _backend._file_manager import *
from _backend._login_logout_user import *
from _config._config import *

def load_accueil(st):
    empty_bloc_accueil = st.empty()
    save_global_session_objet(session=get_state(), key=KEY_SESSION_COMPONENT_ACCUEIL, values=empty_bloc_accueil)
    
    username = get_global_session_objet(session=get_state(), key=KEY_SESSION_USERNAME)
    data_user = get_user_data_by_name(username=username)
    
    if not data_user: return
    
    group = data_user["group"]
    ets = data_user["ets"]
    list_files = []
    
    if ets: 
        list_files.extend(get_ets_files(ets=ets))    
    if group:
        list_files.extend(get_group_files(group=group))
        
    list_files = list(set(list_files))    
    
    bloc_accueil = empty_bloc_accueil.container()
    bloc_accueil.write(list_files)