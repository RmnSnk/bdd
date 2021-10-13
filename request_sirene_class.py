# coding:utf-8

"""
Test de l'API de siren via l'utilisation d'une class
"""

import requests
import logging

import config # Credential pour data.inpi
import mise_en_forme as mf # Mise en forme

logging.basicConfig(filename='msg.log', level=logging.DEBUG)

"""
https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee
"""

"""
Tuto : https://www.sebastien-lhuillier.com/index.php/item/495-explointons-les-api-de-l-insee
Sur les Jetons : https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/help.jag#jeton
"""

"""
Url de base : https://api.insee.fr/entreprises/sirene/V3/siren/{siren}
"""

r = requests.get("https://api.insee.fr/entreprises/sirene/V3/siren/833216781", headers={'Accept': 'application/json', 'Authorization': 'Bearer 593f2777-5f10-363e-8140-bd8f3e1ddfc3'})
t = r.json() # t contient un dictionnaire qui contient 2 dictionnaires : header et uniteLegale. unitelegale contient nos informations contenues dans des listes
             # et autres dictionnaires ...
print(t)
print(t['uniteLegale']['periodesUniteLegale'][0]['denominationUniteLegale']) # Différent si personne physique lire la documentation
# TODO : coder une simple requête
# TODO : renouveler / gerer le Token
