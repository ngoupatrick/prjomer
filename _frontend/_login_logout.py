import importlib as lib

from _config._config import * 
from _config._components import *
from _backend._login_logout_user import *
from _frontend._sidebar import *
from _backend._session import *
from _backend._file_manager import *
from _backend._mail import *

PIL = lib.import_module(CH_PIL)

def loginForm(component):
    '''
    Create a login form.
    Return: dict of user connexion
    '''
    form = component.form(key='login_form')
    col1, col2 = form.columns(2)
    username = col1.text_input(label = 'Username or Email')
    pw = col1.text_input(label='Password', type = "password")
    
    bas_1, bas_2 = form.empty().columns(2)
    submit_button = bas_1.form_submit_button(label='Connexion')
    label_info = bas_2.empty()
    
    return {"type": CH_TYPE_LOGIN,
            "btn":submit_button,
            "label_info": label_info,
            "username":username,
            "pw":pw
            }

def signupForm(component):
    '''
    Create signup form.
    return: dict of new user infos
    '''
    form = component.form(key='signup_form', clear_on_submit=True)
    col1, col2 = form.columns(2)
    form.markdown("---")   
      
    nom_prenom = col1.text_input(label = 'Noms et prénoms(*)')
    username = col1.text_input(label = 'Compte utilisateur(*)')
    email = col1.text_input(label = 'Email(*)')
    pw = col1.text_input(label='Mot de passe(*)', type = "password")
     
    tel = col2.text_input(label = "Numéro de téléphone(*)")
    ets = col2.text_input(label = "Etablissement(*)")
    gender = col2.selectbox(label = 'Sexe(*)', options = LIST_GENDER)
    metier = col2.text_input(label = "Métiers(*)")
    group_user = col2.selectbox(label = 'Groupe(*)', options = LIST_GROUP_USERS)
    #actif = col2.checkbox(label="Actif", value=True)
    
    bas_1, bas_2 = form.empty().columns(2)
    submit_button = bas_1.form_submit_button(label='Enregistrer')
    label_info = bas_2.empty()
    return {"type": CH_TYPE_SIGNUP,
            "btn":submit_button,
            "label_info": label_info,
            "username":username,
            "pw":pw,
            "email":email,
            "nom":nom_prenom,
            "group":group_user,
            "gender":gender,
            "ets": ets,
            "metier": metier,
            "tel": tel,
            "actif": 0
            }

def main_is_login(st, username):
    '''
    If user is already connect, we update his informations
    at the left sidebar and add the button 'logout'.
    The component to load his login infos is save in 'KEY_SESSION_COMPONENT_LOG'
    of the session object
    '''
    session = get_state()
    emp_connect = get_global_session_objet(session=session, key=KEY_SESSION_COMPONENT_LOG)
    if not emp_connect: return  #TODO: check if he is logged in. if not, call function to set him as visitor                   
    emp_connect.empty()#disable the 'login/register' form
    #show infos in sidebar
    login_sidebar_update(st=st, user=username)

def load_form_login_signup(st):
    '''
    Load form of login/signup
    '''
    session = get_state()
    #space to create login/signup. We save it in session.
    emp_connect = st.empty()
    save_global_session_objet(session=session, key=KEY_SESSION_COMPONENT_LOG, values=emp_connect)
    #create choose box (login or signup)
    connect_space = emp_connect.container()
    my_expander = connect_space.expander(label = "Identification!!")
    with my_expander:
        col1, col2, col3, col4 = st.columns(4)        
        login_signup = col1.selectbox(
            label = "Connecter/Enregistrer", 
            options = LIST_CONNEXION            
        )   
        empty = st.empty()    
    #the login/signup space
    contLogin = empty.container()
    #the HomePage data
    home_page(st=st, component=connect_space)
    #show choosen type(login or signup) form
    if login_signup:
        if str(login_signup).lower()=="connexion":
            f_form = loginForm
        if str(login_signup).lower()=="enregistrer":
            f_form = signupForm
        data_return = f_form(contLogin)
    #actions depending on which button(login or signup) is pressed    
    if data_return.get("btn", None):#submit login or signup
        if data_return.get("type") == CH_TYPE_LOGIN:#login button
            if login_user(
                session = get_state(),
                username=data_return.get("username"),
                pw=data_return.get("pw")
                ):
                main_is_login(st=st, username=data_return.get("username"))
            else: data_return["label_info"].error("Compte ou mot de passe érroné")
                
        if data_return.get("type") == CH_TYPE_SIGNUP:#signup button            
            if signup_user(
                session = get_state(),
                data_return=data_return
                ):
                #send Email to admin                
                ch_rep_email = send_confirmation_email(datareturn=data_return)
                if ch_rep_email: data_return["label_info"].error(ch_rep_email) #il y'a erreur lors de l'envoi du mail
                else: 
                    data_return["label_info"].success("Enregistrement éffectué. Veuillez Patienter, le temps de l'activation de votre compte.")
                    #TODO:sleep
                    #TODO: reinit fields                
            else: data_return["label_info"].error("Veuillez bien vérifier les champs (email ou nom d'utlisateur) ou utiliser un autre nom d'utilisateur")                  

  

def home_page(st, component):
    '''
    fill the home page with some tricks and tips
    '''
    img_graph = PIL.Image.open(get_ressource_fullpath(PATH_FILE_IMAGE_GRAPH))
    component.image(img_graph, caption='OMER and Open Mind At DIT')

def main_login_logout(st):
    username = username_connect()
    if username:
        main_is_login(st=st, username=username)
    else:
        load_form_login_signup(st=st)
    
    
                
        
    