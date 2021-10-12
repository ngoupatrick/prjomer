import importlib as lib

from _config._config import *
from _backend._file_manager import *

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ve = lib.import_module(CH_VALIDATE_EMAIL)

def check_email(adr_email):
    '''
    check if an email is valid
    '''
    _adr_email = adr_email.strip()
    return ve.validate_email(_adr_email)

def get_server_ovh_mail():
    '''
    return (server, port) for ovh server mail connexion
    '''
    return SERVER_IMAP_OVH, PORT_MAIL_SSL

def get_server_yahoo_mail():
    '''
    return (server, port) for yahoo server mail connexion
    '''
    return SERVER_MAIL_YAHOO, PORT_MAIL_SSL

def send_mail_from_admin(recipient, subject, body_text, body_html):
    '''
    Send an email from admin to an other user
    '''
    #admin mail settings
    sender, pass_sender = get_admin_email_credentials()
    #pass_sender = PASS_OVH_ADMIN_EMAIL
    if not sender: return "Bad Admin email" 
    if not check_email(recipient): return "Bad recipient mail"
    #message to send
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient
    if body_text: message.attach(MIMEText(body_text, 'plain'))
    if body_html: message.attach(MIMEText(body_html, 'html'))
    #server mail config
    server, port = get_server_ovh_mail()
    context=ssl.create_default_context()
    # Send Email
    with smtplib.SMTP_SSL(host=server, port=port, context=context) as email_server:
        email_server.login(sender, pass_sender)
        email_server.send_message(message)
        #email_server.send_message(msg=message, from_addr=sender, to_addrs=recipient)
        
    return ""

def send_mail_to_admin(subject, body_text, body_html):
    '''
    The only one use who can send mail from this app is the admin.
    To send a mail to admin, the sender is admin and recipient is also admin.
    '''
    return send_mail_from_admin(recipient=get_admin_email(), subject=subject, body_text=body_text, body_html=body_html)

def send_email_activation(datareturn):
    '''
    Send mail for activation of new user
    '''
    mr_mde = "Monsieur"
    if datareturn["gender"]=="Feminin": mr_mde="Madame"
    subject = f"[{CH_APP}]- Compte activé"
    body_text = None
    body_html = f"""
        <html>
        <body>
            <p>Bonjour, <b>{mr_mde} {datareturn["nom"]}</b>,<br>
            Votre compte [{datareturn["username"]}] viens bel et bien d'être Activé.<br>
            Vous pouvez dès a présent vous connecter sur l'application {CH_APP}.<br><br>
            
            Pour plus d'ample informations, prenez contact avec l'administrateur système</b><br>
            <br><br>
                        
            <a href="http://www.dit.sn">OMER and Open Mind At DIT</a> <br>
            Bien à vous.
            </p>
        </body>
        </html>
        """ 
    return send_mail_from_admin(recipient=datareturn["email"], subject=subject, body_text=body_text, body_html=body_html)
    
def send_confirmation_email(datareturn):
    '''
    Send mail before signup as new user
    '''
    subject = f"[{CH_APP}]- Nouvel utilisateur: Attente d'activation de compte"
    body_text = None
    body_html = f"""
        <html>
        <body>
            <p>Bonjour, <b>Admin</b>,<br>
            Un nouvel utilisater s'enregistré.<br>
            Vous êtes prié de vérifier ses informations et éventuellement activer son compte.<br><br>
            <u>Informations du nouvel utilisateur:</u><br>
            Compte : <b>{datareturn["username"]}</b><br>
            Email : <b>{datareturn["email"]}</b><br>
            Noms & prénoms : <b>{datareturn["nom"]}</b><br>
            Group : <b>{datareturn["group"]}</b><br>
            Sexe : <b>{datareturn["gender"]}</b><br>
            Etablissement : <b>{datareturn["ets"]}</b><br>
            Métier : <b>{datareturn["metier"]}</b><br>
            Tel : <b>{datareturn["tel"]}</b><br><br><br>
                        
            <a href="http://www.dit.sn">OMER and Open Mind At DIT</a> <br>
            Attente de réponse.
            </p>
        </body>
        </html>
        """ 
    return send_mail_to_admin(subject=subject, body_text=body_text, body_html=body_html)    