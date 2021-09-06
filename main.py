# coding:utf-8

"""
Petit programme pour vérifier si le service postgre est lancé.
Pour mémoire on lance le service postgre par la commande rc-service postgresql-13 start, mais cela va lancer le processus
postgres VIA l'utilisateur postgres.
"""

import psutil


class Config:
    """Classe qui contient la configuration"""

    # Nom du processus postgre recherché
    nom_proc_pg = "postgres"

    # Nom de l'utilisateur postgre et de sa base de donnée
    nom_utilisateur_pg = "python_project"
    nom_bdd_pg = "python_project"


class CheckPostgre:
    """
    Classe pour vérifier le service postgre :
    1 - Le serveur postgre tourne bien
    2 - L'utilisateur et la base de donnée exite.
    Si un de ces tests échoue il faut prévenir le sysadmin pour configurer la bdd
    """


    def postgre_isrunning():

        """Renvoie une liste contenant les différents processus postgre si le service postgre est lancé, sinon renvoie 0"""

        l = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.name() == Config.nom_proc_pg:
                l.append(proc)

        if len(l) == 0:
            return False
        else:
            return True


    def user_isexist():
        pass

    def db_isexist():
        pass



# TODO : prévoir des logs pour enregistrer les test

# Script de test

if CheckPostgre.postgre_isrunning == True:
    print(True)
else:
    print(False)


