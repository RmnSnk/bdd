# coding:utf-8

"""
Test de l'API de data.inpi
"""

import requests



class Connexion_datainpi():

    """En utilisant l'objet Session, on n'a plus à gérer les cookies"""

    session = requests.Session()
    login = "romain.sonneck-portail-data"
    password = "volYjaba2"  # -> A modifier

    def __init__(self):
        pass

    def login_datapinpi(self):
        urlbase = "https://opendata-rncs.inpi.fr/services/diffusion/login"
        r = Connexion_datainpi.session.post(urlbase, headers={'Login': Connexion_datainpi.login, 'Password': Connexion_datainpi.password})
        print(r.text)
        return

    def logout_datainpi(self):
        urlbase = "https://opendata-rncs.inpi.fr/services/diffusion/logout"
        r = Connexion_datainpi.session.post(urlbase)
        print(r.text)

    def get_name_datainpi(self, siren=343222386):
        urlbase = 'https://opendata-rncs.inpi.fr/services/diffusion/imrs-saisis/find'
        payload = {'siren': siren}
        r = Connexion_datainpi.session.get(urlbase, params=payload)
        print(r.text)

connexion = Connexion_datainpi()
connexion.login_datapinpi()
connexion.get_name_datainpi()
connexion.logout_datainpi()