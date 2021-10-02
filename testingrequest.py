# coding:utf-8

"""On teste le module request et l'API Pappers"""

import requests

api_token = "584e92f6a67ab9972f6be58d9c9d43fa42052d4cf640dae6"

#urlbase = "https://api.pappers.fr/v2/"

siren = "343222386" # DTIF

payload = {'api_token' : api_token, 'siren' : siren}

### replacer /entreprise par /association ou /recherche ... en fonction de ce que l'on veut
r = requests.get("https://api.pappers.fr/v2/document/extrait_pappers", params=payload)
#print(r.json())

"""On doit écrire le résustat dans un fichier. On écrit des bytes"""
with open('dtif.pdf', 'wb') as f:
    f.write(r.content)

# Voir également https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module
