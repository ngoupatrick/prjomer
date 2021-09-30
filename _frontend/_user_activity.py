from _backend._session import *
from _backend._file_manager import *
from _backend._login_logout_user import *
from _frontend._graph import *
from _config._config import *
from _data_process._data_process import *


def show_files_list(st, component, component_details, component_parent, list_files):
    '''
    show the files list of specific user
    '''
    ch_markdown = f" **<u>Liste des établissements</u>** ({len(list_files)})"
    component.markdown(ch_markdown, unsafe_allow_html=True)
    option = component.selectbox(
        label='Sélectionnez un établissement', 
        options = get_file_without_ext_list(list_files)
    )
    if option:
        filename = find_file_in_list(list_files=list_files, _file=option)
        if not filename: return
        show_file_info(st=st, component=component_details, _file = filename)
        load_data_file(st=st, component=component_parent, _file=filename)
        #save current file in session state
        save_global_session_objet(session=get_state(), key=KEY_SESSION_CURRENT_FILE_DATA, values=filename)
    
    
def show_file_info(st,component, _file):
    '''
    show process file in progress
    '''
    ch_markdown = ''
    # file path
    file_path= get_data_fullpath(_file=_file)
    component.markdown(f"Fichier: ***[{_file}]***")
    #load data
    df = load_df_data(file_path=file_path)
    #component.markdown(":ballot_box_with_check: Load Data")
    ch_markdown = f"> <u>**Colonnes**</u>: {df_columns(df)} \n > <u>**Dimension**</u>: {df_shape(df)} \n\n > <u>**Duplicated values**</u>: {df_duplicated(df)} "
    component.markdown(ch_markdown, unsafe_allow_html=True)
    #count NaN
    #df = drop_df_duplicate(df)
    #component.markdown(":ballot_box_with_check: Drop duplicated data")

def create_settings_plot(df, expander_plot, component_parent, dfcol, col_graph_1, col_graph_2, col_graph_3, col_graph_4):    
    expander_container_plot = expander_plot.container()
    c1, _ = expander_container_plot.columns(2)
    plot_title = c1.text_input(label="Graph Title:")    
    col_x, col_y, col_type  = expander_container_plot.columns(3)
    col_hue, col_palette, col_col = expander_container_plot.columns(3)
    
    #graph settings
    list_graph = []
    list_graph.extend(LIST_PLOT_UN)
    list_graph.extend(LIST_PLOT_DEUX)
    list_graph.extend(LIST_PLOT_TROIS)
    
    list_type = [CH_VIDE]
    list_type .extend(list_graph)
    
    list_x = [CH_VIDE]
    list_x.extend(dfcol)
    
    list_y = [CH_VIDE]
    list_y.extend(dfcol)
    
    list_hue = [CH_VIDE]
    list_hue.extend(dfcol)
    
    list_col = LIST_COL_PLOT
    
    list_palette = [CH_VIDE]
    list_palette.extend(LIST_PLOT_PALETTE)
    
    _col_x = col_x.selectbox(label="Indicateur 1 =", options=list_x)
    _col_y = col_y.selectbox(label="Indicateur 2 =", options=list_y)
    _col_type = col_type.selectbox(label="Type de graphe:", options=list_type)
    _col_hue = col_hue.selectbox(label="Filtrer", options=list_hue)
    _col_palette = col_palette.selectbox(label="Couleurs:", options=list_palette)
    _col_col = col_col.selectbox(label="Autres graphes:", options=list_col)
    
    cc1, cc2, _ = expander_container_plot.columns(3)
    btn_plot_graph = cc1.button(label="Déssiner le graphe")
    cc2.button(label="Reinitialisez les graphes", on_click = reset_all_graph)
    
    graph_component = component_parent #component where plot graph
    _kwargs = dict()
    
    #if _col_type or _col_x or _col_y or _col_hue or _col_palette: pass 
    if _col_col:
        list_col_graph = [col_graph_1, col_graph_2, col_graph_3, col_graph_4]
        #load all plots if exist
        load_all_plot_in_session(list_col_graph=list_col_graph)         
    
    if btn_plot_graph:
        if _col_type == CH_VIDE or (_col_x==CH_VIDE and _col_y==CH_VIDE):
            pass
        else:
            err = ""
            if _col_type in LIST_PLOT_TROIS and _col_x != CH_VIDE and _col_y != CH_VIDE:
                err = "Précisez juste un indicateur pour ce graphe"                
            
            if _col_type in LIST_PLOT_UN:
                if (_col_x != CH_VIDE and _col_y == CH_VIDE):
                    if not df_is_numeric(df=df,column_name= _col_x):
                        err="pass"
                if (_col_x == CH_VIDE and _col_y != CH_VIDE):
                    if not df_is_numeric(df=df,column_name= _col_y):
                        err="pass"
                if _col_x != CH_VIDE and _col_y != CH_VIDE and not(df_is_numeric(df=df,column_name= _col_x) or df_is_numeric(df=df,column_name= _col_y)): 
                    err = "Un des deux indicateurs doit être de type numérique pour ce graphe"
                
            if err=="pass":
                return
            if err:
                component_parent.error(body = err)
                return                                   
            
            if _col_col != CH_VIDE: graph_component = eval(_col_col)
            
            if _col_x != CH_VIDE: _kwargs["x"] = _col_x
            if _col_y != CH_VIDE: _kwargs["y"] = _col_y
            if _col_hue != CH_VIDE: _kwargs["hue"] = _col_hue
            if _col_palette != CH_VIDE: _kwargs["palette"] = _col_palette
            
            _kwargs["_col_col"] = _col_col
            _kwargs["_col_type"] = _col_type
            _kwargs["plot_title"] = plot_title
            _kwargs["file_data"] = get_global_session_objet(session=get_state(), key=KEY_SESSION_CURRENT_FILE_DATA)            
            save_global_session_objet(session=get_state(), key=KEY_SESSION_CURRENT_COL_GRAPH, values=_col_col) 
            graph_plot(df=df, component=graph_component, _type_plot = _col_type, title=plot_title, kwargs=_kwargs)
    

def create_plot_space(df, component):
    #print("ici")
    '''
    create settings plots and plot graph
    '''
    dfcol = df_columns(df=df)
    
    expander_plot = component.expander('Paramètres des graphes')
    
    #bloc for 4 graphs    
       
    col_graph = component.container()
    col_graph_1, col_graph_2 = col_graph.columns(2)
    col_graph_3, col_graph_4 = col_graph.columns(2)
    
    col_graph_1.write("graph 1")
    col_graph_2.write("graph 2")
    col_graph_3.write("graph 3")
    col_graph_4.write("graph 4")
    
        
    create_settings_plot(df=df, expander_plot=expander_plot, component_parent=col_graph, dfcol=dfcol, 
                         col_graph_1=col_graph_1, col_graph_2=col_graph_2, col_graph_3=col_graph_3, col_graph_4=col_graph_4)


def load_all_plot_in_session(list_col_graph):
    list_col = LIST_COL_PLOT
    for pos, col_graph in enumerate(list_col):
        col_en_cours = get_global_session_objet(session=get_state(), key=KEY_SESSION_CURRENT_COL_GRAPH)
        #if col_en_cours == col_graph: continue
        plot_from_session(key_session=col_graph, graph_component=list_col_graph[pos])
        
def reset_all_graph():
    for col_graph in LIST_COL_PLOT:
        del_global_session_objet(session=get_state(), key=col_graph)    
    
def load_data_file(st, component, _file):
    '''
    load data in the file
    '''
    file_path= get_data_fullpath(_file=_file)
    df = load_df_data(file_path=file_path)
    dfcol = df_columns(df=df)
    #component.balloons()
    #bloc of filter before show
    expander_data = component.expander('Visualisez les données')
    expander_container_data = expander_data.container()
    column_option = expander_container_data.multiselect(#select columns to show
        label = 'Les indicateurs:',
        options = dfcol,
        default = dfcol
    )
    nb_rows = expander_container_data.number_input(#number max of row to show
        label='Nombre de lignes:',
        min_value=10,
        value=100,
        step=5
    )
    if column_option or nb_rows:
        expander_container_data.dataframe(df[column_option].head(int(nb_rows)))
    else: expander_container_data.dataframe(df.head(100))
    #bloc of data plots
    create_plot_space(df = df, component=component)
         

def show_props_user(st, component):
    '''
    show the user files in a component
    '''
    username = get_global_session_objet(session=get_state(), key=KEY_SESSION_USERNAME)
    data_user = get_user_data_by_name(username=username)
    
    if not data_user: return
    
    group = data_user["group"]
    ets = data_user["ets"]   
    list_files = get_user_files(ets=ets, group=group)
    
    expander_info =  component.expander(label = "Choisissez un établissement")
    col1, col2 = expander_info.columns(2)    
    
    show_files_list(st=st, component=col1, component_details=col2, component_parent=component, list_files=list_files)
 
 
def load_user_activity(st):
    empty_main_bloc = st.empty()
    save_global_session_objet(session=get_state(), key=KEY_SESSION_COMPONENT_MAIN, values=empty_main_bloc)
    #main container
    bloc_main = empty_main_bloc.container()
    
    #load files or proprities of user
    show_props_user(st=st, component=bloc_main)
    