from _config._config import *

def cmp_choose_menu(component, title = "Navigation: ", list_menu = LIST_MENU, key_component = "main_menu"):    
    return component.radio(title, list_menu, key = key_component)

