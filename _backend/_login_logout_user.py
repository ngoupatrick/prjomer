import importlib as lib

from _config._config import *
from _backend._session import *
from _backend._file_manager import *

ve = lib.import_module(CH_VALIDATE_EMAIL)


def save_user_session(session, username):    
    save_global_session_objet(session = session, key=KEY_SESSION_USERNAME, values=username)  

def clean_user_session(session):
    '''
    Clean user session infos
    Return: bool. if all is correct, it return 'True'
    ''' 
    try:
        del_global_session_objet(session = session, key=KEY_SESSION_USERNAME)
        del_global_session_objet(session = session, key=KEY_SESSION_USEREMAIL)
    except: return False
    return True

def is_connect():
    '''
    Check if a user is connect
    return: true if it is connect
    '''        
    return bool(username_connect())

def username_connect():
    '''
    return the username if he is connect and None else
    '''
    session = get_state()
    return get_global_session_objet(session=session, key=KEY_SESSION_USERNAME)



def find_user(username):
    '''
    Find a user in data.
    return id (database) or key (credentials) else None
    '''
    if type(username) is not str: return None
    credentials = get_credentials_data()
    for key,val in credentials.items():
        if val.get("username").lower() == username.lower():            
            return key  
    return None

def get_user_data_by_key(key, by=CH_TYPE_CREDENTIALS_KEY):
    '''
    get user informations by key or id
    '''
    data = None
    if by == CH_TYPE_CREDENTIALS_KEY:
        credentials = get_credentials_data()
        data = credentials[key]
    if by == CH_TYPE_CREDENTIALS_BD:
        pass
    return data

def get_user_data_by_name(username, by=CH_TYPE_CREDENTIALS_KEY):
    '''
    get user informations by username
    '''
    key = find_user(username=username)
    if not key: return None
    
    data = None
    if by == CH_TYPE_CREDENTIALS_KEY:
        data = get_user_data_by_key(key=key)
    if by == CH_TYPE_CREDENTIALS_BD:
        pass
    return data

def check_login_user(username, pw):
    '''
    Check if user credentials are correct.
    return: bool. True if user credentials are correct
    '''
    if type(username) is not str: return False
    if type(pw) is not str: return False
    
    credentials = get_credentials_data()
    for _,val in credentials.items():
        if val.get("username").lower() == username.lower() and val.get("pw") == pw:            
            if int(val.get("actif", 0))==1: return True  #if it is active
    return False

def check_signup_user(kwargs):
    '''
    Check if credentials of new user are valid
    '''
    d_user = kwargs['kwargs']
    #if user missed some fields
    if d_user['username'].strip()=='' or d_user['pw'].strip()=='' or d_user['email'].strip()=='' or d_user['nom'].strip()=='' or d_user['metier'].strip()=='':
        return False        
    #if user already exist
    if find_user(d_user['username'].strip()): return False
    #check user email    
    if not ve.validate_email(d_user['email'].strip()): return False 
    return True  

def check_user(type_op = CH_TYPE_LOGIN, **kwargs):
    if type_op == CH_TYPE_LOGIN: return check_login_user(username=kwargs['username'], pw=kwargs['pw'])
    if type_op == CH_TYPE_SIGNUP: return check_signup_user(kwargs=kwargs)
    
def login_user(session, username, pw):
    if not check_user(username=username, pw=pw): return False
    save_user_session(session = session, username = username)
    return True
    
def logout_user(session):
    return clean_user_session(session = session)

def signup_user(session, data_return):
    if not check_user(type_op=CH_TYPE_SIGNUP, kwargs= data_return): return False
    #save user info
    add_user_credentials(data_user=data_return)
    return True
        