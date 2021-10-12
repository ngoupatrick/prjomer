from _config._config import *

import os
import json
import importlib as lib
import re

sts = lib.import_module(CH_STREAMLIT_IMPORT)

@sts.cache
def _get_fullpath(_folder,_file):
    return os.path.join(_folder, _file)

@sts.cache
def get_data_fullpath(_file):
    return _get_fullpath(_folder = PATH_FOLDER_DATA, _file=_file)

@sts.cache
def get_ressource_fullpath(_file):
    return _get_fullpath(_folder = PATH_FOLDER_RESSOURCES, _file=_file)

@sts.cache
def get_credential_fullpath(_file):
    return _get_fullpath(_folder = PATH_FOLDER_CREDENTIALS, _file=_file)

@sts.cache
def get_mediatheque_fullpath(_file):
    return _get_fullpath(_folder = PATH_FOLDER_MEDIATHEQUE, _file=_file)

def get_mediatheque_themes():
    chemin = get_mediatheque_fullpath(_file = PATH_FILE_MEDIATHEQUE_CONF)
    if not os.path.isfile(chemin): return None
    with open(chemin, 'r') as f:
        data = json.load(f)
        return list(data["themes"].keys())
    return None

def get_mediatheque_themes_files(theme):
    chemin = get_mediatheque_fullpath(_file = PATH_FILE_MEDIATHEQUE_CONF)
    if not os.path.isfile(chemin): return None
    with open(chemin, 'r') as f:
        data = json.load(f)        
        return data["themes"][theme]["files"]
    return None

#@sts.cache
def get_credentials_data():
    chemin = get_credential_fullpath(_file = PATH_FILE_CREDENTIALS)
    if not os.path.isfile(chemin): return None
    with open(chemin, 'r') as f:
        data = json.load(f)
        return data["credentials"]
    return None

def get_all_credentials_data():
    chemin = get_credential_fullpath(_file = PATH_FILE_CREDENTIALS)
    if not os.path.isfile(chemin): return None
    with open(chemin, 'r') as f:
        data = json.load(f)
        return data
    return None

def add_user_credentials(data_user):
    du = data_user
    dt_user = dict()
    dt_user["username"] = du['username']
    dt_user["pw"] = du['pw']
    dt_user["email"] = du['email']
    dt_user["nom"] = du['nom']
    dt_user["group"] = du['group']
    dt_user["gender"] = du['gender']
    dt_user["ets"] = du['ets']
    dt_user["metier"] = du['metier']
    dt_user["tel"] = du['tel']
    dt_user["structure"] = str(du['structure'])
    dt_user["actif"] = int(du['actif'])
    data = get_all_credentials_data()
    data["credentials"][dt_user["username"]] = dt_user
    #ecriture dans le fichier de credentials
    chemin = get_credential_fullpath(_file = PATH_FILE_CREDENTIALS)
    with open(chemin, 'w') as fp:
        json.dump(data, fp)
    

#@sts.cache
def get_conf_data():
    chemin  = get_data_fullpath(PATH_FILE_CONFIG)
    if not os.path.isfile(chemin): return None
    with open(chemin, 'r') as f:
        data = json.load(f)
        return data
    return None

#@sts.cache
def get_data_ets(ets):
    data = get_conf_data()
    if ets in data["data"]:        
        return data["data"][ets]
    else:
        return None


#@sts.cache
def get_ets_files(ets):
    data = get_data_ets(ets=ets)
    if not data: return None
    return data["files"]

#@sts.cache
def get_group_files(group):
    '''
    Given a group, we return a list of files associate to this group
    '''
    data = get_conf_data()
    if not data: return None
    list_files = []
    for key,val in data["data"].items():
        if key in ["codes","groups", "admin_email","pass_email"]: continue
        if key in ["groups_unique"]: 
            if group in val:
                break
            continue
        if group not in val["group"]: continue
        list_files.extend(val["files"])
    
    list_files = list(set(list_files))
    return list_files

#@sts.cache
def get_user_files(ets = None, group = None):
    list_files = []
    if ets: 
        _f = get_ets_files(ets=ets)
        if _f:
            list_files.extend(_f)    
    if group:
        _f = get_group_files(group=group)
        if _f:
            list_files.extend(_f)
    list_files = list(set(list_files))
    return list_files

#@sts.cache
def get_admin_email():
    '''
    get the admin adresse mail
    '''
    data = get_conf_data()
    if not data: return None
    return data["data"]["admin_email"]

def get_admin_email_credentials():
    '''
    get the admin adresse mail
    '''
    data = get_conf_data()
    if not data: return None
    return data["data"]["admin_email"], data["data"]["pass_email"]

#@sts.cache
def is_file_in(ets, group, _file):
    list_files = get_user_files(ets=ets, group=group)
    return _file in list_files

#@sts.cache
def files_in_folder(_folder):
    '''
    get all files in a folder
    '''
    return os.listdir(_folder)

#@sts.cache
def find_file_in_folder(_folder, _file):
    '''
    Find a file which don't have an extension in folder
    '''
    list_files = files_in_folder(_folder = _folder)
    return find_file_in_list(list_files=list_files, _file=_file)

#@sts.cache
def find_file_in_list(list_files, _file):
    '''
    find the file name from a list
    '''
    ls_first = [ch for ch in list_files if re.search(_file, ch, re.IGNORECASE)]
    ls_second = [ch.split('.')[-2] for ch in ls_first]
    for pos, ch in enumerate(ls_second):
        if ch.lower()==_file.lower():
            return ls_first[pos]
    return None

#@sts.cache
def get_file_without_ext_folder(_folder):
    '''
    return a list of name file without extensions from a folder
    '''
    list_files = files_in_folder(_folder = _folder)
    return get_file_without_ext_list(list_files=list_files)

#@sts.cache
def get_file_without_ext_list(list_files):
    '''
    return a list of name file without extensions from a list
    '''
    return [ch.split('.')[-2] for ch in list_files]

#@sts.cache
def get_file_and_extension(file_name):
    '''
    return the couple (filename, ext)
    ext is like '.py'
    '''
    return os.path.splitext(file_name)

#sts.cache
def get_type_file(file_name):
    '''
    get a type of file given his extensions
    '''
    _,ext = get_file_and_extension(file_name=file_name)
    _type = None
    if ext.lower() == '.csv': _type = TYPE_DATA_CSV
    if ext.lower() == '.xls' or ext.lower()=='.xlsx': _type = TYPE_DATA_EXCEL
    return _type

#sts.cache
def get_all_sonu():
    '''
    get the list of all sonu
    '''
    chemin  = get_data_fullpath(_file = PATH_FILE_SONU)
    if not os.path.isfile(chemin): return None
    with open(chemin, 'r') as f:
        data = json.load(f)
        return data
    return None

#sts.cache
def get_sonu_by_key(key):
    '''
    find a sonu by key
    '''
    sonu = get_all_sonu()
    if not sonu: return None
    return sonu.get(key, None)

#sts.cache
def get_sonu_by_structure(structure):
    '''
    get a sonu (key, value), given his structure
    '''
    sonu = get_all_sonu()
    if not sonu: return None
    for key,val in sonu.items():
        if val["structure"].lower()==structure.lower():
            return key, val
    return None

#sts.cache        
def get_all_sonu_region():
    '''
    get all regions oof sonu
    '''
    sonu = get_all_sonu()
    if not sonu: return None
    region = set()
    for _, val in sonu.items():
        region.add(val["Region"])
    return list(region)

#sts.cache
def get_all_sonu_district(region):
    '''
    get all district given a sonu region
    '''
    sonu = get_all_sonu()
    if not sonu: return None
    district = set()
    for _, val in sonu.items():        
        if region.lower()==val["Region"].lower():
            district.add(val["District"])
    return list(district)

#sts.cache
def get_all_sonu_structure(district):
    '''
    get all structure sonu given his district
    '''
    sonu = get_all_sonu()
    if not sonu: return None
    structure = set()
    for _, val in sonu.items():        
        if district.lower()==val["District"].lower():
            structure.add(val["structure"])
    return list(structure)

#sts.cache
def find_key_sonu(region, district, structure):
    '''
    find a sonu key given his (region, district, structure) couple
    '''
    sonu = get_all_sonu()
    if not sonu: return None
    if None in [region, district, structure]: return None
    _key = 0
    for key, val in sonu.items():        
        if region.lower()==val["Region"].lower() and district.lower()==val["District"].lower() and structure.lower()==val["structure"].lower():
            _key = key
    return _key