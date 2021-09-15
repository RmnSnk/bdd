# coding:utf-8

"""
Petit programme pour vérifier si le service postgre est lancé.
Pour mémoire on lance le service postgre par la commande rc-service postgresql-13 start, mais cela va lancer le processus
postgres VIA l'utilisateur postgres.
"""

import psutil
import psycopg2
import logging

logging.basicConfig(filename='msg.log', level=logging.DEBUG)


class ConfigPostgre:
    """Classe qui contient la configuration"""

    # Nom du processus postgre recherché
    nom_proc_pg = "postgres"

    # Nom de l'utilisateur postgre et de sa base de donnée
    nom_utilisateur_pg = "python_project"
    nom_bdd_pg = "python_project"

    # Paramètre de connexion postgre
    host = "127.0.0.1"
    port = "5432"


class CheckPostgre:
    """
    Classe pour vérifier le service postgre :
    1 - Le serveur postgre tourne bien
    2 - L'utilisateur et la base de donnée existe.
    Si un de ces tests échoue il faut prévenir le sysadmin pour configurer la bdd
    """


    def postgre_isrunning():

        """Renvoie une liste contenant les différents processus postgre si le service postgre est lancé, sinon renvoie 0"""

        l = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.name() == ConfigPostgre.nom_proc_pg:
                l.append(proc)

        if len(l) == 0:
            return False
        else:
            return True


    def connexion_isok():
        # voir https://pynative.com/python-postgresql-tutorial/#h-install-psycopg2-using-the-pip-command
        # et le scrip en bas pour capturer les erreurs
        try:
            connexion = psycopg2.connect(user=ConfigPostgre.nom_utilisateur_pg, host=ConfigPostgre.host, port=ConfigPostgre.port,
                                         database=ConfigPostgre.nom_bdd_pg)
            cursor = connexion.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            logging.debug(record)
            cursor.close
            connexion.close
            print("Test de connexion réussis")

        except Exception as error:
            logging.debug(error)
            print("Erreur lors du connexion : ", error)


    def running_test():
        CheckPostgre.postgre_isrunning()
        CheckPostgre.connexion_isok()



# Script de test

CheckPostgre.running_test()



# TODO : prévoir des logs pour enregistrer les test https://www.youtube.com/watch?v=-ARI4Cz-awo
# TODO :        Petit script simple pour enregistrer des informations dans la basse de données (Siren) soit un par un soit via une liste.
# TODO suite :  Utiliser argparse pour ça
# TODO Interaction avec pappers pour récuperer : Nom, adresse, gérant.
# TODO : interaction pappers pour récuperer les statuts

