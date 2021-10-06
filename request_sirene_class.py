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