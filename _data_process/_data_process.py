import importlib as lib
from _config._config import *
from _backend._file_manager import *

pd = lib.import_module(CH_PANDAS)
np = lib.import_module(CH_NUMPY)
sts = lib.import_module(CH_STREAMLIT_IMPORT)

#@sts.cache#(suppress_st_warning=True)
#@sts.experimental_singleton
def load_df_data(file_path, filter= None, col_filter=None, val_filter=None):
    '''
    read data with pandas
    '''
    type_file = get_type_file(file_name=file_path)
    df = None
    if type_file == TYPE_DATA_EXCEL: df = pd.read_excel(file_path)
    if type_file == TYPE_DATA_CSV: df = pd.read_csv(file_path)
    if filter:
        df = df[df[col_filter]==val_filter]
    return df

#@sts.cache#(suppress_st_warning=True)
def filter_df_data(df, col_filter, val_filter):
    '''
    filter data with pandas.
    we get all rows where [col_filter==val_filter]
    we assume that fields are string
    '''
    mask = df[col_filter].str.fullmatch(val_filter, case = False, na = False)#contains, match
    df = df[mask]
    return df

@sts.cache
def df_columns(df):
    '''
    return the columns list of df
    '''
    return list(df.columns)

#@sts.cache(suppress_st_warning=True)
def drop_df_columns(df, columns, verifcation = False):
    '''
    drop some columns in a pandas dataFrame
    '''
    if not verifcation:
        if isinstance(columns, (list, tuple)):
            return df.drop(columns=columns)
        if isinstance(columns, str):
            return df.drop(columns=[columns])
        else: return df
    else:
        cols = df.columns
        if isinstance(columns, str):
            if columns in cols:
                return df.drop(columns=[columns])
        if isinstance(columns, (list, tuple)):
            df_inter=df
            for col in columns:
                if col in cols:
                    df_inter = df_inter.drop(columns=[col])
            return df_inter
        else: return df

@sts.cache
def merge_df_columns(df, col_one, col_two):
    '''
    Merge columns one and two in one
    '''
    return df[col_one]+" "+df[col_two]

#@sts.cache(suppress_st_warning=True)
def reorder_df_columns(df, columns):
    '''
    reorder dataFrame with the new columns order
    '''
    return df[columns]

@sts.cache
def convert_df_column(df, column_name, _type):
    '''
    Convert a column to a specific type
    '''
    if _type == PANDAS_TYPE_DATE:
        return pd.to_datetime(df[column_name])
    if _type in(PANDAS_TYPE_STRING, PANDAS_TYPE_INT):
        return df[column_name].astype(_type)

@sts.cache
def extract_df_year(df, column_name):
    '''
    extract a year in column
    '''
    return pd.DatetimeIndex(df[column_name]).year

@sts.cache
def extract_df_month(df, column_name):
    '''
    extract a month in column
    '''
    return pd.DatetimeIndex(df[column_name]).month

@sts.cache
def pd_min(df, column_name):
    '''
    extract the min in column
    '''
    return df[column_name].min()

@sts.cache
def pd_max(df, column_name):
    '''
    extract the max in column
    '''
    return df[column_name].max()

@sts.cache
def col_nan(df, column_name):
    '''
    extract NaN values number in column
    '''
    return df[column_name].isna().sum()

@sts.cache
def df_nan(df):
    '''
    extract NaN values number in df
    '''
    return df.isna().sum().values.sum()

@sts.cache
def drop_df_duplicate(df):
    '''
    Remove all duplicated values in df
    '''
    return df.drop_duplicates()

@sts.cache
def df_duplicated(df):
    '''
    number of duplicated rows
    '''
    return df.duplicated().sum()

@sts.cache
def df_shape(df):
    '''
    get the shape of df
    '''
    return df.shape

@sts.cache
def df_get_type_col(df, column_name):
    '''
    pd.api.types.is_datetime64_dtype
    pd.api.types.is_numeric_dtype
    pd.api.types.is_object_dtype
    pd.api.types.is_bool_dtype
    https://pandas.pydata.org/docs/reference/api/pandas.api.types.is_bool_dtype.html
    '''
    try: return df[column_name].dtype
    except: return None

@sts.cache
def df_is_datetime(df, column_name):
    try: return pd.api.types.is_datetime64_dtype(df[column_name])
    except: return False

@sts.cache
def df_is_numeric(df, column_name):
    try: return pd.api.types.is_numeric_dtype(df[column_name])
    except: return False

@sts.cache
def df_is_object(df, column_name):
    try: return pd.api.types.is_object_dtype(df[column_name])
    except: return False

@sts.cache
def df_is_bool(df, column_name):
    try: return pd.api.types.is_bool_dtype(df[column_name])
    except: return False
    
def df_init(cols):
    '''
    init a dataframe with columns
    '''
    return pd.DataFrame(columns = cols)

def df_add_rows(df, rows):
    '''
    add a row in df at the end
    '''
    _df = df.copy()
    _df.loc[len(_df)]=rows
    return _df