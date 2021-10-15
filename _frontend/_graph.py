import importlib as lib

from _config._config import *
from _backend._session import *
from _data_process._data_process import *
from _backend._file_manager import *

plt = lib.import_module(CH_MATPLOTLIB)
sb = lib.import_module(CH_SEABORN)

def graph_plot(df, component, _type_plot, title, kwargs):
    '''
    plot all graph except pie chart
    '''
    if _type_plot == 'pie':
        pie(df=df, component=component, kwargs=kwargs, title=title)
    else:
        l_del = ["_col_col","_col_type", "plot_title", "file_data"]
        _kwargs = kwargs.copy()
        for key in l_del:
            _kwargs.pop(key)
            
        plot_func = eval("sb."+str(_type_plot))
        fig, ax = plt.subplots()
        chart = plot_func(data = df, **_kwargs)
        chart.set_title(title)
        chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right') 
        chart.set_yticklabels(chart.get_yticklabels(), rotation=45, horizontalalignment='right') 
        component.pyplot(fig)
    #save graph datas
    save_global_session_objet(session=get_state(), key=kwargs["_col_col"], values=kwargs)
    
def pie(df, component, kwargs, title):
    '''
    plot a pie
    '''
    palette = None
    if 'y' in kwargs: column = kwargs['y']
    if 'x' in kwargs: column = kwargs['x']
    if 'palette' in kwargs: palette = kwargs['palette']
    df_valcount = df[column].value_counts()
    l = df_valcount.shape[0]#number of type in column

    #Using matplotlib
    pie, ax = plt.subplots(figsize=[10,6])
    labels = df_valcount.keys()
    colors = sb.color_palette(palette)
    plt.pie(x=df_valcount, autopct="%.1f%%", explode=[0.05]*l, labels=labels, pctdistance=0.3, colors= colors)
    plt.title(title, fontsize=10)    
    component.pyplot(pie)
    
def plot_from_session(key_session, graph_component):
    '''
    plot a graph with parameters store in session
    '''
    data = get_global_session_objet(session=get_state(), key=key_session)
    if not data: return
    file_path= get_data_fullpath(_file=data["file_data"])
    df = load_df_data(file_path=file_path)
    graph_plot(df=df, component=graph_component, _type_plot = data["_col_type"], title=data["plot_title"], kwargs=data)
    
    