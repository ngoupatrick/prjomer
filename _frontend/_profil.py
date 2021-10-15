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
    
    #show the profiles, if and only if he is log in
    if not is_connect():
        st.markdown(f":sweat: [{CH_MUST_BE_CONNECT}]")
        return 
    
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
    ch_act_0, ch_act_1, ch_act_2, ch_act_3 = CH_VIDE, 'modifier les ipassnfos', 'modifier mon mot de passe', "modifier l'email d'administration"
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
    ch_markdown += f"<u>Tel:</u>  ***{data_user['tel']}*** <br>"
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
        new_tel = form_modif.text_input(label = "Tel", value = data_user["tel"])
        new_group = form_modif.selectbox(label = 'Groupe', options = LIST_GROUP_USERS, index = LIST_GROUP_USERS.index(data_user['group']))
        new_gender = form_modif.selectbox(label = 'Sexe', options = LIST_GENDER, index = LIST_GENDER.index(data_user['gender']))
        
        data_new = {
                "new_name": new_name,
                "new_mail":new_mail,
                "new_group":new_group,
                "new_gender":new_gender,
                "new_ets": new_ets,
                "new_metier": new_metier,
                "new_tel": new_tel
                }
        if is_admin:#Montrer actif si admin
            new_actif = form_modif.checkbox(label="Activer", value = bool(int(data_user['actif'])))
            data_new["new_actif"] = new_actif
                
        if form_modif.form_submit_button(label="Modifier"):
            ch_rep = update_modif(data_user=data_user, data_new=data_new, is_admin=is_admin)
            ch_rep = ""
            if ch_rep: form_modif.error(ch_rep)
            else:                 
                if ch_key == "modif_user":#modification venant de l'admin
                    #si c'est une activation
                    act_old, act_new = data_user["actif"], data_new["new_actif"]
                    if type(act_old) == int: act_old = bool(act_old)
                    if type(act_new) == int: act_new = bool(act_new)
                    if act_new == True and act_old == False: #activation de compte
                        #TODO: send mail
                        _data_user = get_user_data_by_name(username=data_user["username"])
                        send_email_activation(datareturn=_data_user)
                form_modif.success("Utilisateur Mis A jour!!")

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
            
def load_form_modif_sonu(component, data_user, is_admin=False):
    '''
    create the SONU modification form
    '''
    #get user structure
    _val, index_region, index_district, index_structure = None, None, None, None
    if data_user:
        _val = get_sonu_by_key(key=data_user["structure"])
        old_region = _val["Region"]
        old_district = _val["District"]
        old_structure = _val["structure"]
    #end
    form_container = component.container()
    ls_region = [CH_VIDE]
    ls_region.extend(get_all_sonu_region())
    #find region index
    try:
        if _val: index_region = ls_region.index(_val["Region"])
        else: index_region = 0 
    except: index_region = 0
    #end        
    group_region = form_container.selectbox(label = 'Région(*)', options = ls_region, index=index_region)
    ls_district = [CH_VIDE]
    if group_region:
        if group_region==CH_VIDE: return
        ls_district = [CH_VIDE]
        ls_district.extend(get_all_sonu_district(region = group_region))
    #find district index
    try:
        if _val: index_district = ls_district.index(_val["District"])
        else: index_district = 0 
    except: index_district = 0
    #end            
    group_district = form_container.selectbox(label = 'District(*)', options = ls_district, index=index_district)
    ls_structure = [CH_VIDE]
    if group_district:
        if group_district==CH_VIDE: return
        ls_structure = [CH_VIDE]
        ls_structure.extend(get_all_sonu_structure(district=group_district))
    
    #find structure index
    try:
        if _val: index_structure = ls_structure.index(_val["structure"])
        else: index_structure = 0 
    except: index_structure = 0
    #end     
    group_structure = form_container.selectbox(label = 'Structure(*)', options = ls_structure, index = index_structure)
    btn = form_container.button(label="Modifier")
    data_new = None
    if btn:
        data_new = {
            "Region": group_region,
            "District": group_district,
            "structure": group_structure
        }
        ch_rep = update_modif_structure(data_user=data_user, data_new=data_new, is_admin=is_admin)
        if ch_rep:
            form_container.error(ch_rep)
        else: form_container.success("Structure de l'utilisateur Mis A jour!!")

def update_modif_structure(data_user, data_new, is_admin=False):
    '''
    Check and save new user structure
    '''
    if not is_admin: return "Vous devez être administrateur"
    if data_user==None or data_new == None: return "Veuillez remplir les champs"
    region, district, structure = data_new["Region"], data_new["District"], data_new["structure"]
    if None in [region, district, structure]: return "Veuillez remplir tous les champs"
    if CH_VIDE in [region, district, structure]: return "Veuillez remplir tous les champs"
    _key = find_key_sonu(region=region, district=district, structure=structure)
    if int(_key)==0: return "Structure inconue"
    dt_user = data_user.copy()
    dt_user["structure"] = _key
    add_user_credentials(data_user=dt_user)
    return ""
    
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
    dt_user["tel"] = data_new["new_tel"].strip()
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
    col_info, col_modif = user_exp_container.columns([1,2])
    list_users = [CH_VIDE]
    _list_users = [k for k,v in credentials.items() if not is_admin(username=v["username"])]
    list_users.extend(_list_users)
    choix_user = col_info.selectbox(label = "Liste des utilisateurs", options = list_users)
    ch_act_0, ch_act_1, ch_act_2 = CH_VIDE, "modifier l'utilisateur", 'modifier la structure'
    list_actions = [ch_act_0, ch_act_1, ch_act_2]
    choix_action = col_info.selectbox(label = "Actions", options = list_actions)
    
    if choix_user!=CH_VIDE and choix_action!=CH_VIDE:
        if choix_action==ch_act_1:
            load_form_modif(component=col_modif, data_user=credentials[choix_user], ch_key='modif_user', is_admin=is_admin_)
        if choix_action==ch_act_2:
            load_form_modif_sonu(component=col_modif, data_user=credentials[choix_user], is_admin=is_admin_)
            
                
        
