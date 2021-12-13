LIST_MENU = ["Accueil", "Dashboard", "Médiathèque", "Enquete", "Profil"]
LIST_GENDER =  ['Masculin','Feminin']
CH_MENTORE = 'mentore'
CH_MENTORAT = 'mentorat'
CH_SUPERVISEUR = 'superviseur'
LIST_GROUP_USERS = [CH_MENTORE, CH_MENTORAT, CH_SUPERVISEUR]
LIST_CONNEXION = ["Connexion", "Enregistrer"]

LIST_PLOT_UN = [ "barplot", "boxplot"]
LIST_PLOT_DEUX = ["histplot", "scatterplot", "lineplot"]
LIST_PLOT_TROIS = ["pie", "countplot"]

LIST_PLOT_PALETTE = [ "husl", "Set2", "Paired", "pastel", "tab10", "rocket"]

KEY_SESSION_USERNAME = "username"
KEY_SESSION_USEREMAIL = "email"
KEY_SESSION_COMPONENT_LOG = "component_log"
KEY_SESSION_COMPONENT_ACCUEIL = "component_accueil"
KEY_SESSION_COMPONENT_MAIN = "component_main"

KEY_SESSION_SBAR = 'sbar'
KEY_SESSION_BLOC_1 = "bloc_1"
KEY_SESSION_BLOC_2 = "bloc_2"
KEY_SESSION_TRANSIT = 'b_l'
KEY_SESSION_BTN_DECONNECT= 'btn_deconnect'
KEY_SESSION_RADMENU  = 'radmenu'

KEY_SESSION_COL_GRAPH_1 = "col_graph_1"
KEY_SESSION_COL_GRAPH_2 = "col_graph_2"
KEY_SESSION_COL_GRAPH_3 = "col_graph_3"
KEY_SESSION_COL_GRAPH_4 = "col_graph_4"
LIST_COL_PLOT = [KEY_SESSION_COL_GRAPH_1, KEY_SESSION_COL_GRAPH_2, KEY_SESSION_COL_GRAPH_3, KEY_SESSION_COL_GRAPH_4]
KEY_SESSION_CURRENT_FILE_DATA = "current_file_data"
#KEY_SESSION_CURRENT_DF_DATA = "current_df_data"
KEY_SESSION_CURRENT_COL_GRAPH = "col_graph_en_cours"

KEY_SESSION_SONU_DATA_FOUND = "excel_sonu_data"
KEY_SESSION_LEVEL_FILTER = "_level_filter"
KEY_SESSION_DATA_SELECT = "data_select"
CH_TYPE_LOGIN = 'login'
CH_TYPE_SIGNUP = 'signup'
CH_GUEST_NAME = 'Visiteur'
CH_GROUP_BASE = 'g1'

PATH_FOLDER_DATA = "./_data"
PATH_FOLDER_RESSOURCES = "./_ressources"
PATH_FOLDER_CREDENTIALS = "./_data/_credentials"
PATH_FOLDER_MEDIATHEQUE = "./_data/_mediatheque"

PATH_FILE_CONFIG = "conf.json"
PATH_FILE_CREDENTIALS = "credentials.json"
PATH_FILE_MEDIATHEQUE_CONF = "media_conf.json"
PATH_FILE_SONU = "sonu.json"
PATH_FILE_FICHE_EVAL = "Fiche_devaluation_test.xlsx"

PATH_FILE_IMAGE_GRAPH = "head_science.jpg"

CH_STREAMLIT_IMPORT = "streamlit"
CH_STREAMLIT_REPORTTHREAD = "streamlit.report_thread"
CH_STREAMLIT_SERVER = "streamlit.server.server"
CH_MATPLOTLIB = "matplotlib.pyplot"
CH_SEABORN = "seaborn"
CH_PANDAS = "pandas"
CH_NUMPY = "numpy"
CH_PIL = "PIL"
CH_VALIDATE_EMAIL = "validate_email"

CH_TYPE_CREDENTIALS_KEY = "key"
CH_TYPE_CREDENTIALS_BD = "bd"

CH_VIDE = "--"
CH_APP = "Omer--APP"
CH_ON_CONSTRUCTION = "SORRY!! BLOC EN CONSTRUCTION........"
CH_MUST_BE_CONNECT = "SORRY!! VOUS DEVEZ ETRE CONNECTE POUR AVOIR ACCES A CETTE PAGE..... \n\n ............VEUILLEZ ALLER A LA PAGE D'ACCEUIL"
CH_ACCESS_RIGHT = "SORRY!! VOUS NE DISPOSEZ PAS DES DROITS D'ACCES........"

PANDAS_TYPE_DATE = "date"
PANDAS_TYPE_STRING = "str"
PANDAS_TYPE_INT = "int"

SERVER_IMAP_OVH = "ssl0.ovh.net"
PORT_IMAP_ENTRANT_OVH = 993
PORT_MAIL_SSL = 465
SERVER_MAIL_YAHOO = "smtp.mail.yahoo.com"
PORT_YAHOO_MAIL = 587

TYPE_DATA_EXCEL = "xlsx"
TYPE_DATA_CSV = "csv"

CH_USE_TEL = "tel"#use tel to find data
CH_USE_LEVEL = "level"#use group to find data


#TODO: Ajout important. A modifier en fonction des noms de columns
CH_COL_TEL = "Telephone"
CH_COL_REGION = "Region Medicale de :" # the column name of region in excel file
CH_COL_DISTRICT_PATTERN = "District de [Dakar]  :" #pattern of district column in excel file
CH_COL_SONU_PATTERN = "District de [Dakar Centre] :" #pattern of sonu column in excel file
####END AJOUT#####