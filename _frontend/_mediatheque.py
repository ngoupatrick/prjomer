import importlib as lib

from _backend._file_manager import *
from _config._config import *
from _backend._login_logout_user import *

sts = lib.import_module(CH_STREAMLIT_IMPORT)


def main_mediatheque(st):
    st = st.empty()
    st.write('flush')
    #show the mediatheque, if and only if he is log in
    if not is_connect():
        st.markdown(f":sweat: [{CH_MUST_BE_CONNECT}]", unsafe_allow_html=True)
        return    
    themes = get_mediatheque_themes()
    main_container = st.container()
    if is_admin():
        media_expand = main_container.expander(label="Gestion de la médiathèque")
        col_action, col_mng = media_expand.columns([1,2])
        menu_ajout_theme, menu_modif_theme, menu_ajout_video= "Ajouter un thème","Modifer un thème", "Ajouter une vidéo"
        media_mng_option = [CH_VIDE, menu_ajout_theme, menu_modif_theme , menu_ajout_video]
        choix_action = col_action.selectbox(label = "Actions", options = media_mng_option)
        if choix_action==menu_ajout_theme:
            form_ajout_theme(component=col_mng, key_form=menu_ajout_theme)
        if choix_action == menu_modif_theme:
            form_modif_theme(component=col_mng, nested_component=col_action, key_form=menu_modif_theme)
        if choix_action == menu_ajout_video:
            form_ajout_video(component=col_mng, nested_component=col_action, key_form=menu_modif_theme)
        
    
    video_container = main_container.expander(label="Médiathèque", expanded=True)#.container()
    
    themes_media = video_container.selectbox(label="Thèmes de la médiathèque:", options=themes)
    if themes_media:
        option_video = get_mediatheque_themes_files(theme=themes_media)
        choix_video = video_container.selectbox(label = "Vidéos du thème:", options = option_video)
        if choix_video:            
            read_video(st=st, component=video_container, _file=choix_video)        

            
def read_video(st, component, _file):
    video_bytes = get_bytes(_file=_file)
    component.video(video_bytes)  

@sts.cache        
def get_bytes(_file):
    with open( get_mediatheque_fullpath(_file), 'rb') as video_file:
        video_bytes = video_file.read()        
    return video_bytes  

def form_ajout_theme(component, key_form):
    ct = component.form(key=key_form, clear_on_submit=True)
    ct.markdown(f":heavy_plus_sign: <ins>Ajout de thème</ins>", unsafe_allow_html=True)
    _theme = ct.text_input(label = "Titre du thème")
    _etat = ct.checkbox(label = "Actif", value=True)
    submitted = ct.form_submit_button("Ajouter")
    if submitted:
        if _theme.strip()=='':
            ct.error("Veuillez renseigner un titre de thème")
            return
        data_themes = dict()
        #["theme"], ["etat"]
        data_themes["theme"] = _theme.strip()
        data_themes["etat"] = _etat
        data_themes["files"] = []
        add_theme(data_themes=data_themes)
        ct.success("Ajout éffectué")
        
def form_modif_theme(component, nested_component, key_form):
    l_theme =[CH_VIDE]
    l_theme.extend(get_mediatheque_themes(_etat=False))
    choix_theme = nested_component.selectbox(label = "Choisissez un thème", options=l_theme)
    if choix_theme!=CH_VIDE:
        data_them = get_mediatheque_themes_data(theme=choix_theme)    
        ct = component.form(key=key_form, clear_on_submit=True)
        ct.markdown(f":pencil2: <ins>Modification de thème</ins>", unsafe_allow_html=True)
        ct.markdown(f":file_folder: <ins>{data_them['files']}</ins>", unsafe_allow_html=True)
        _theme = ct.text_input(label = "Titre du thème", value = choix_theme)
        _etat = ct.checkbox(label = "Actif", value=bool(int(data_them["etat"])))
        submitted = ct.form_submit_button("Modifier")
        if submitted:
            if _theme.strip()=='':
                ct.error("Veuillez renseigner un titre de thème")
                return
            data_themes = dict()
            data_themes["theme"] = _theme.strip()
            data_themes["etat"] = _etat
            data_themes["files"] = data_them["files"]
            add_theme(data_themes=data_themes)
            ct.success("Modification éffectuée")
            
def form_ajout_video(component, nested_component, key_form):
    l_theme =[CH_VIDE]
    l_theme.extend(get_mediatheque_themes(_etat=True))
    choix_theme = nested_component.selectbox(label = "Choisissez un thème", options=l_theme)
    if choix_theme!=CH_VIDE:
        data_them = get_mediatheque_themes_data(theme=choix_theme)    
        ct = component.form(key=key_form, clear_on_submit=True)
        ct.markdown(f":movie_camera: <ins>{choix_theme}</ins>", unsafe_allow_html=True)
        ct.markdown(f":file_folder: <ins>{data_them['files']}</ins>", unsafe_allow_html=True)
        files = ct.file_uploader(label = "Selectionner les fichiers", type ="mp4", accept_multiple_files=True)
        submitted = ct.form_submit_button("Ajouter la vidéo")
        if submitted:
            if not files:
                ct.error("Veuillez selectionner des fichiers")
                return
            #Sauvegarder le fichier dans le dossier
            ls_name_file = []
            for file in files:
                save_upload_file(_dir = PATH_FOLDER_MEDIATHEQUE, _file = file, _file_name= file.name)
                ls_name_file.append(file.name)
            #Sauvegarder le fichier dans le fichier de configuration
            ls_name_file.extend(data_them["files"])
            data_themes = dict()
            data_themes["theme"] = choix_theme.strip()
            data_themes["etat"] = data_them["etat"]
            data_themes["files"] = ls_name_file
            add_theme(data_themes=data_themes)
            ct.success("Modification éffectuée")