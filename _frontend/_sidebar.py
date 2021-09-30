import importlib as lib

from _config._components import *
from _backend._login_logout_user import *
from _backend._session import *
from _frontend._user_activity import *

sts = lib.import_module(CH_STREAMLIT_IMPORT) 


def init_sidebar(st, sbar):
    session = get_state()
    save_global_session_objet(session = session,key=KEY_SESSION_SBAR, values=sbar)

def create_info_user(st, sbar):
    '''
    Create component for user login informations
    '''    
    session = get_state()
    sbar = get_global_session_objet(session=session, key=KEY_SESSION_SBAR)
    #create the components blocs    
    log_cont = sbar.container()
    log_empty = log_cont.empty()   
    log_col1, log_col2 = log_cont.columns(2)
    bloc_1 = log_col1.empty()    
    bloc_2 = log_col2.empty()
    #saving them in session                
    save_global_session_objet(session=session, key=KEY_SESSION_BLOC_1, values=bloc_1)
    save_global_session_objet(session=session, key=KEY_SESSION_BLOC_2, values=bloc_2)
    
def login_sidebar_update(st, user=None):
    '''
    Update user infos on sidebar
    '''
    #if we add 'logout' button
    add_logout_button = True
    #get components to load user data
    session = get_state()
    bloc_1 = get_global_session_objet(session=session, key= KEY_SESSION_BLOC_1)
    bloc_2 = get_global_session_objet(session=session, key= KEY_SESSION_BLOC_2)
    # if not exist, return
    if not bloc_1 or not bloc_2: return None
    #find user infos
    _user = user
    #breakpoint()
    if _user is None:   
        try: _user = get_global_session_objet(session=session, key= KEY_SESSION_USERNAME)#check in session
        except: 
            _user = CH_GUEST_NAME
    if _user is None:
        _user = CH_GUEST_NAME
    if _user == CH_GUEST_NAME:
        add_logout_button = False
    #show user infos
    afficher_user(st=st, component= bloc_1, user=_user)
    if add_logout_button:
        afficher_btn_deconnect(st=st, component=bloc_2)          
    
    
    
def afficher_user(st, component,user):
    '''
    Just put user data in allocated components
    '''    
    component.markdown(f":white_check_mark: Bienvenu {user}")


@sts.cache(hash_funcs={sts.delta_generator.DeltaGenerator: id})
def afficher_btn_deconnect(st, component):
    '''
    Just add logout button.
    Before adding it, we must check if it exist first in session.
    if not exist in session, save it
    '''
    btn = component.button(label = "Deconnexion", on_click = logout_user, kwargs = {"session":get_state()}, key = KEY_SESSION_BTN_DECONNECT)
    #check if click        
    if btn:
        login_sidebar_update(st=None)

def menu_sidebar(st, sbar):
    '''
    Menu side bar
    '''
    rad_menu = cmp_choose_menu(component=sbar)
    #save radmenu in session
    save_global_session_objet(session=get_state(), key=KEY_SESSION_RADMENU, values=rad_menu)
    

def main_sidebar(st , sbar):
    '''
    Init all components at sidebar
    '''
    #save the sidebar
    init_sidebar(st=st, sbar=sbar)
    #create the first time the user info at sidebar
    create_info_user(st=st, sbar=sbar)
    #set user infos
    login_sidebar_update(st = st)
    sbar.markdown("---")
    #create for first time the menu at sidebar
    menu_sidebar(st=st, sbar=sbar)
    sbar.markdown("---")
    

    
    