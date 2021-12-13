from _data_process._data_process import *


##valeur introuvable dans sonu.json mais visible dans excel
#Foudiougne
#Birkilane
#Malen Hodar
#Tambacouda
#Tivaoune
#Thionk-Essy        

def remove_space(val):
    '''
    remove space in str or list
    '''
    if isinstance(val, list):
        return [str(_val).replace(" ", "").strip() for _val in val]
    if isinstance(val, tuple):
        return (str(_val).replace(" ", "").strip() for _val in val)
    return str(val).replace(" ", "").strip()

def get_df_filter(_user_tel):
    '''
    looking for rows regarding his tel, in excel file
    '''
    df = load_df_data(file_path = get_path_fiche_evaluation())
    df[CH_COL_TEL] = convert_df_column(df=df, column_name=CH_COL_TEL, _type=PANDAS_TYPE_STRING)#force columns to be string
    df = filter_df_data(df=df, col_filter=CH_COL_TEL, val_filter=_user_tel)#find matching rows (tel with no space between numbers)
    return df

def extract_user_rows_from_tel(username, user_tel, clean_space=True):
    
    '''
    extract specific rows in excel file for a user base on his tel
    '''
    
    _user_tel = remove_space(val=user_tel) if clean_space else user_tel   
    #dictionnary to store all important data excel from user and save it in session (for graph)
    dict_sonu_rows_excel = dict()
    dict_sonu_rows_excel["username"] = username
    dict_sonu_rows_excel["tel_origin"] = user_tel
    dict_sonu_rows_excel["tel_no_space"] = _user_tel
    n_iter=0
    
    df = get_df_filter(_user_tel=_user_tel)
    cols = df_columns(df=df)#get columns of dataframe
    for index, row in df.iterrows():
        #collecting data from excel rows
        n_iter = n_iter + 1
        dict_tampon = dict() 
        dict_tampon["df_index"] = index
        
        #pattern col district: "District de [Dakar]  :"
        _district = row[CH_COL_REGION]
        
        dict_tampon["col_region"] = CH_COL_REGION #saving excel col of region
        dict_tampon["region"] = _district.strip() #saving region
        
        col_district = f"District de {_district.strip()}  :" #district column name in pandas
        
        if col_district in cols:
            _sonu = row[col_district]
            dict_tampon["col_district"] = col_district #saving excel col of district
            dict_tampon["district"] = _sonu.strip() #saving district
            
            #pattern col sonu: "District de [Dakar Centre] :"
            col_sonu = f"District de {_sonu.strip()} :" #sonu column name in pandas
            if col_sonu in cols:
                vrai_sonu = row[col_sonu]
                dict_tampon["col_sonu"] = col_sonu #saving excel col of sonu
                dict_tampon["sonu"] = vrai_sonu.strip() #saving sonu
        #saving tampon data
        dict_sonu_rows_excel[n_iter] = dict_tampon.copy()    
    
    return df, dict_sonu_rows_excel

def extract_user_rows_based_on(df_orig, dict_filter):
    
    '''
    extract specific rows in excel file for a user base on his tel
    '''
    if df_orig is None: return None
    if dict_filter is None: return None
       
    n_region = dict_filter.get("region", None)
    if n_region is None: return df_orig
    
    cols = df_columns(df=df_orig)#get columns of dataframe     
    df_return = df_init(cols=cols)#init the dataFrame to return
    
    for _, row in df_orig.iterrows():        
        _district = row[CH_COL_REGION]
        if n_region == _district:
            n_district = dict_filter.get("district", None)
            if n_district is None:
                df_return = df_add_rows(df=df_return, rows=row)
                continue
            col_district = f"District de {_district.strip()}  :"
            if col_district in cols:
                _sonu = row[col_district]
                if _sonu==n_district:
                    n_sonu = dict_filter.get("sonu", None)
                    if n_sonu is None:
                        df_return = df_add_rows(df=df_return, rows=row)
                        continue
                    col_sonu = f"District de {_sonu.strip()} :"
                    if col_sonu in cols:
                        vrai_sonu = row[col_sonu]
                        if vrai_sonu!=n_sonu: continue
                        df_return = df_add_rows(df=df_return, rows=row)        
        
    return df_return


def clean_columns_from_excel_all(df, verification):
    
    '''
    drop some columns in dataframe
    '''
    
    df_clean = df
    regions = get_all_sonu_region()
    for region in regions:
        districts = get_all_sonu_district(region=region)
        for district in districts:
            sonus = get_all_sonu_structure(district=district)
            sonus = [sonu.strip() for sonu in sonus]
            df_clean = drop_df_columns(df=df_clean, columns=sonus, verifcation=verification)
        col_districts = [f"District de {district.strip()} :" for district in districts]
        col_districts_ = [f"District de {district.strip()}" for district in districts]
        districts = [district.strip() for district in districts]        
        df_clean = drop_df_columns(df=df_clean, columns=districts, verifcation=verification)
        df_clean = drop_df_columns(df=df_clean, columns=col_districts, verifcation=verification)
        df_clean = drop_df_columns(df=df_clean, columns=col_districts_, verifcation=verification)
    col_regions = [f"District de {region.strip()}  :" for region in regions]
    col_regions_ = [f"District de {region.strip()}" for region in regions]
    regions = [region.strip() for region in regions]
    df_clean = drop_df_columns(df=df_clean, columns=col_regions, verifcation=verification)
    df_clean = drop_df_columns(df=df_clean, columns=col_regions_, verifcation=verification)
    df_clean = drop_df_columns(df=df_clean, columns=regions, verifcation=verification)
    return df_clean

def clean_columns_from_excel_partial(df, verification):
    '''
    drop limited columns in dataframe
    '''
    df_clean = df
    regions = get_all_sonu_region()
    for region in regions:
        districts = get_all_sonu_district(region=region)
        for district in districts:
            sonus = get_all_sonu_structure(district=district)
            sonus = [sonu.strip() for sonu in sonus]
            df_clean = drop_df_columns(df=df_clean, columns=sonus, verifcation=verification)
        districts = [district.strip() for district in districts]        
        df_clean = drop_df_columns(df=df_clean, columns=districts, verifcation=verification)
    regions = [region.strip() for region in regions]
    df_clean = drop_df_columns(df=df_clean, columns=regions, verifcation=verification)
    return df_clean

def find_all_region(dict_iter):
    '''
    find all the regions names in the [dict_iter]
    '''
    if dict_iter is None:
        return None
    ls_region = []
    for key, value in dict_iter.items():
        if key in ["username", "tel_origin", "tel_no_space"]:
            continue
        ls_region.append(value.get("region", None))
    if len(ls_region)==0: return None
    return ls_region

def find_district_from_region(dict_iter, region):
    '''
    find all district from a specific region in [dict_iter]
    '''
    if dict_iter is None:
        return None
    ls_district = []
    for key, value in dict_iter.items():
        if key in ["username", "tel_origin", "tel_no_space"]:
            continue
        if value.get("region")==region:
            ls_district.append(value.get("district", None))    
    if len(ls_district)==0: return None
    return ls_district

def find_sonu_from_district(dict_iter, district):
    '''
    find all sonu in a specific district
    '''
    if dict_iter is None:
        return None
    ls_sonu = []
    for key, value in dict_iter.items():
        if key in ["username", "tel_origin", "tel_no_space"]:
            continue
        if value.get("district")==district:
            ls_sonu.append(value.get("sonu", None))    
    if len(ls_sonu)==0: return None
    return ls_sonu

def count_data(dict_iter):
    '''
    count the number off row in a specific 
    '''
    if dict_iter is None:
        return 0
    counter = 0
    for key, _ in dict_iter.items():
        if key in ["username", "tel_origin", "tel_no_space"]:
            continue
        counter = counter+1   
    return counter