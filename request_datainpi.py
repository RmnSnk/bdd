# coding:utf-8

"""
Test de l'API de data.inpi
"""

import requests

login = "romain.sonneck-portail-data"
password = "volYjaba2" #-> A modifier

""" Si on utilise pas de session, on doit gérer les cookies et les repasser à chaque requête """

def login_datapinpi():
    urlbase = "https://opendata-rncs.inpi.fr/services/diffusion/login"
    r = requests.post(urlbase, headers={'Login': login, 'Password': password})
    cookie = r.headers['Set-Cookie']
    print(r.text)
    return cookie

def logout_datainpi(cookie):
    urlbase = "https://opendata-rncs.inpi.fr/services/diffusion/logout"
    r = requests.post(urlbase, headers={'cookie': cookie})
    print(r.text)



def get_name_datainpi(cookie, siren=343222386):
    urlbase = 'https://opendata-rncs.inpi.fr/services/diffusion/imrs-saisis/find'
    payload = {'siren': siren}
    r = requests.get(urlbase, params=payload, headers={'cookie': cookie})
    print(r.text)

cookie = login_datapinpi()
get_name_datainpi(cookie, 791835689)
logout_datainpi(cookie)