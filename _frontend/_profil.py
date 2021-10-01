import importlib as lib
from os import error

from _backend._file_manager import *
from _backend._login_logout_user import *
from _backend._mail import *
from _config._config import *

sts = lib.import_module(CH_STREAMLIT_IMPORT)

def main_profil(st):
    '''
    bloc principal de gestion de profil
    '''
    
    st = st.empty()
    st.write('flush')
    
    username = username_connect()
    data_user = get_user_data_by_name(username=username)
    _is_admin = is_admin()
    
    user_container = st.container()
    
    user_expand = user_container.expander(label="Mes informations personnelle")
    load_info_user(component=user_expand, data_user=data_user, is_admin=_is_admin)
    #gestion des utilisateur
    if _is_admin:
        users_expand = user_container.expander(label="Gestion des comptes utilisateurs")
        load_all_users(component=users_expand, is_admin_=_is_admin)
        
    #gestion des fichiers des etablissement
    if _is_admin:
        users_expand = user_container.expander(label="Gestion des Fichiers des établissements")
        #TODO: set the bloc for managing ets files
        users_expand.markdown(f":sweat: [{CH_ON_CONSTRUCTION}]")
    

def load_info_user(component, data_user, is_admin = False):
    '''
    load personnal data for current user, using markdown style
    '''
    user_exp_container = component.container()
    col_info, col_modif = user_exp_container.columns(2)
    col_info.markdown(markdown_info_user(data_user=data_user), unsafe_allow_html=True)
    ch_act_0, ch_act_1, ch_act_2, ch_act_3 = CH_VIDE, 'modifier les infos', 'modifier mon mot de passe', "modifier l'email d'administration"
    list_actions = [ch_act_0, ch_act_1, ch_act_2]
    if is_admin: list_actions.extend([ch_act_3])
    choix_action = col_info.selectbox(label = 'Actions', options = list_actions)
    if choix_action == ch_act_1:
        click_btn_modifier( component = col_modif, data_user=data_user, is_admin=is_admin)
    if choix_action == ch_act_2:
        click_btn_modif_pass( component = col_modif, data_user=data_user, is_admin=is_admin)
    if choix_action == ch_act_3:
        #TODO: set the admin email settings
        col_modif.markdown(f":sweat: [{CH_ON_CONSTRUCTION}]")

   
def markdown_info_user(data_user):
    '''
    create a markdown info for the user
    '''    
    if not data_user: return ""
    ch_markdown = f"<u>Profil de l'utilisateur:</u>  ***{data_user['username']}*** <br>"
    ch_markdown += f"<u>Nom complet:</u>  ***{data_user['nom']}*** <br>"
    ch_markdown += f"<u>Mail:</u>  ***{data_user['email']}*** <br>"
    ch_markdown += f"<u>Group:</u>  ***{data_user['group']}*** <br>"
    ch_markdown += f"<u>Etablissement:</u>  ***{data_user['ets']}*** <br>"
    ch_markdown += f"<u>Metiers:</u>  ***{data_user['metier']}*** <br>"
    ch_markdown += f"<u>Etat:</u>  ***{transform_etat(data_user['actif'])}*** <br>"
    return ch_markdown

def click_btn_modifier(component, data_user, is_admin = False):
    '''
    call when we want to modify user current data
    '''
    load_form_modif(component=component, data_user=data_user, is_admin=is_admin)

def click_btn_modif_pass(component, data_user, is_admin = False):
    '''
    call when we want to modify current user password
    '''
    load_form_modif_pass(component=component, data_user=data_user, is_admin=is_admin)    

def load_form_modif(component, data_user, is_admin=False, ch_key = "modificaton"):
    '''
    create the modifcation form
    '''
    form_container = component.container()
    form_modif = form_container.form(key=ch_key, clear_on_submit=False)
    with form_modif:
        new_name = form_modif.text_input(label = "Nom", value = data_user["nom"])
        new_mail = form_modif.text_input(label = "Username or Email", value = data_user["email"])
        new_ets = form_modif.text_input(label = "Etablissement", value = data_user["ets"])
        new_metier = form_modif.text_input(label = "Metier", value = data_user["metier"])
        new_group = form_modif.selectbox(label = 'Groupe', options = LIST_GROUP_USERS, index = LIST_GROUP_USERS.index(data_user['group']))
        new_gender = form_modif.selectbox(label = 'Sexe', options = LIST_GENDER, index = LIST_GENDER.index(data_user['gender']))
        
        data_new = {
                "new_name": new_name,
                "new_mail":new_mail,
                "new_group":new_group,
                "new_gender":new_gender,
                "new_ets": new_ets,
                "new_metier": new_metier
                }
        if is_admin:#Montrer actif si admin
            new_actif = form_modif.checkbox(label="Activer", value = bool(int(data_user['actif'])))
            data_new["new_actif"] = new_actif
                
        if form_modif.form_submit_button(label="Modifier"):
            ch_rep = update_modif(data_user=data_user, data_new=data_new, is_admin=is_admin)
            if ch_rep: form_modif.error(ch_rep)
            else: form_modif.success("Utilisateur Mis A jour!!")        

def load_form_modif_pass(component, data_user, is_admin=False):
    '''
    create the password modification form
    '''
    form_container = component.container()
    form_modif = form_container.form(key="modif_pass", clear_on_submit=True)
    with form_modif:
        old_pass = form_modif.text_input(label = "Ancien Mot de passe", type = "password")
        new_pass = form_modif.text_input(label = "Nouveau Mot de passe", type = "password")
        new_pass_again = form_modif.text_input(label = "Confirmation du nouveau mot de passe", type = "password")
        
        data_new = {
                "old_pass":old_pass,
                "new_pass":new_pass,
                "new_pass_again": new_pass_again
                }
                
        if form_modif.form_submit_button(label="Modifier"):
            ch_rep = update_modif_pass(data_user=data_user, data_new=data_new, is_admin=is_admin)
            if ch_rep:
                form_modif.error(ch_rep)
            else: form_modif.success("Mot de passe utilisateur Mis A jour!!")
    
def update_modif(data_user, data_new, is_admin = False): 
    '''
    save user new informations
    '''   
    #check new data
    if data_new["new_name"].strip() == "": return "Veuillez saisir un nom!!!"
    if not check_email(adr_email=data_new["new_mail"].strip()): return "Votre adresse email est incorrect!!!"
    #save new data
    dt_user = data_user.copy()
    dt_user["nom"] = data_new["new_name"].strip()
    dt_user["email"] = data_new["new_mail"].strip()
    dt_user["group"] = data_new["new_group"]
    dt_user["gender"] = data_new["new_gender"] 
    dt_user["ets"] = data_new["new_ets"].strip()
    dt_user["metier"] = data_new["new_metier"].strip()
    if is_admin:
        dt_user["actif"] = int(data_new["new_actif"])#mettre a jour si actif
    add_user_credentials(data_user=dt_user)
    return ""
    
def update_modif_pass(data_user, data_new, is_admin = False):
    '''
    save the user new data
    '''
    if data_new["old_pass"] == "" or data_new["new_pass"] == "" or data_new["new_pass_again"] == "": return "Veuillez remplir tous les champs"
    if data_new["old_pass"] != data_user["pw"]: return "Ancien mot de passe érroné"
    if data_new["new_pass"] != data_new["new_pass_again"]: return "Nouveau mot de passe différent de la confirmation"
    dt_user = data_user.copy()
    dt_user["pw"] = data_new["new_pass"]
    add_user_credentials(data_user=dt_user)
    return ""

def transform_etat(etat):
    '''
    transforms the state to ch string
    '''    
    if etat == None: return "Inconu"
    _etat = int(etat)
    if _etat: return "Actif"
    if _etat: return "Inactif"
    
def load_all_users(component, is_admin_):
    '''
    show all the users
    '''
    credentials = get_credentials_data()
    if not credentials: return "Aucun utilisateur dans le système"
    
    user_exp_container = component.container()
    col_info, col_modif = user_exp_container.columns(2)
    list_users = [CH_VIDE]
    _list_users = [k for k,v in credentials.items() if not is_admin(username=v["username"])]
    list_users.extend(_list_users)
    choix_user = col_info.selectbox(label = "Liste des utilisateurs", options = list_users)
    
    if choix_user!=CH_VIDE:
        load_form_modif(component=col_modif, data_user=credentials[choix_user], ch_key='modif_user', is_admin=is_admin_)
        
