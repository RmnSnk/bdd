# coding:utf-8

"""
Test de l'API de data.inpi via l'utilisation d'une class
"""

import requests
import logging

import config # Credential pour data.inpi
import mise_en_forme as mf # Mise en forme

logging.basicConfig(filename='msg.log', level=logging.DEBUG)

class Connexion_datainpi():

    """En utilisant l'objet Session, on n'a plus à gérer les cookies"""

    session = requests.Session()
    login = config.Config_connexion.login
    password = config.Config_connexion.password

    def __init__(self):
        pass

    def login_datapinpi(self):
        urlbase = "https://opendata-rncs.inpi.fr/services/diffusion/login"
        r = Connexion_datainpi.session.post(urlbase, headers={'Login': Connexion_datainpi.login, 'Password': Connexion_datainpi.password})
        logging.debug(r.text)

    def logout_datainpi(self):
        urlbase = "https://opendata-rncs.inpi.fr/services/diffusion/logout"
        r = Connexion_datainpi.session.post(urlbase)
        logging.debug(r.text)

    def get_name_datainpi(self, siren=343222386):
        urlbase = 'https://opendata-rncs.inpi.fr/services/diffusion/imrs-saisis/find'
        payload = {'siren': siren}
        r = Connexion_datainpi.session.get(urlbase, params=payload)
        l = r.json() # r.json() renvoie une liste de 1 élément. Cet élément est un dictionnaire à deux clef : siren et Nom
        if len(l) == 0:
            print(f"le Siren {mf.bleu(str(siren))} est inconnu de data.inpi.fr")
            texte = "(Siren erroné ou entreprise non inscrite au RCS, comme certain auto-entrepreneur libéraux)"
            print(f"{mf.italique(texte)}")
        else:
            print(f"le siren {mf.bleu(str(siren))} est attribué  à : {mf.bleu(l[0].get('denominationSociale'))}")


connexion = Connexion_datainpi()
connexion.login_datapinpi()
connexion.get_name_datainpi(451606651)
connexion.logout_datainpi()
