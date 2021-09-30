import importlib as lib

from _backend._file_manager import *
from _config._config import *

sts = lib.import_module(CH_STREAMLIT_IMPORT)


def main_mediatheque(st):
    st = st.empty()
    st.write('flush')
    #options = files_in_folder(PATH_FOLDER_MEDIATHEQUE)
    themes = get_mediatheque_themes()
    #option_container = st.container()    
    video_container = st.container()
    
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