# coding:utf-8

"""
Test de l'API de data.inpi
"""

import requests

login = "romain.sonneck-portail-data"
password = "volYjaba2"
urlbase = "https://opendata-rncs.inpi.fr/services/diffusion/login"

#api_token = "584e92f6a67ab9972f6be58d9c9d43fa42052d4cf640dae6"

#urlbase = "https://api.pappers.fr/v2/"

#siren = "343222386" # DTIF



r = requests.post(urlbase, headers={'Login': login, 'Password': password})

## Voir la doc mais le "cookie" est dans le header de la réponse : 'Set-Cookie': 'JSESSIONID=81BA2DAB1ABB65E6C1A1BF7A36334CBC

print(r.headers)
print(r.headers['Set-Cookie'])
cookie = r.headers['Set-Cookie']
print(r.text)

"""Voir pour réutiliser le cookie"""
# TODO : https://fr.python-requests.org/en/latest/user/advanced.html

#https://opendata-rncs.inpi.fr/services/diffusion/imrs-saisis/find?siren=343222386

r2 = requests.get('https://opendata-rncs.inpi.fr/services/diffusion/imrs-saisis/find?siren=343222386', headers={'cookie': cookie})
print(r2.text)