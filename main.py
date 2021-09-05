# coding:utf-8

"""
Petit programme pour vérifier si le service postgre est lancé.
Pour mémoire on lance le service postgre par la commande rc-service postgresql-13 start, mais cela va lancer le processus
postgres VIA l'utilisateur postgres.
"""

import psutil

l = []
for proc in psutil.process_iter(['pid', 'name', 'username']):
    if proc.name() == 'postgres':
        l.append(proc)

if len(l) == 0:
    print("Le serveur Postgresql n'est pas lancé")
else:
    print("Le serveur Posgresql est lancé via les processus")
    for proc in l:
        print(f"{proc.pid} | utilisateur : {proc.username()}")

#TODO : maintenant que l'on a compris comment ça marche : faire un classe et un methode qui renvoie True or False
#TODO : prévoir des logs