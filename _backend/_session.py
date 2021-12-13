from _config._config import *
import importlib as lib

sts = lib.import_module(CH_STREAMLIT_IMPORT)

#@sts.cache
#@sts.experimental_memo
@sts.experimental_singleton
def get_state():
    print("*****Session*****")
    return sts.session_state

#global session functions
def save_global_session_objet(session, key, values):
   session[key] = values

def get_global_session_objet(session, key, if_None=None):
    if key in session:
        return session[key]
    return if_None

def del_global_session_objet(session, key):
    #del(session[key])
    save_global_session_objet(session=session, key=key, values=None)