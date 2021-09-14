# coding:utf-8

"""
Petit programme pour vérifier si le service postgre est lancé.
Pour mémoire on lance le service postgre par la commande rc-service postgresql-13 start, mais cela va lancer le processus
postgres VIA l'utilisateur postgres.
"""

import psutil
import psycopg2
import logging

logging.basicConfig(level=logging.DEBUG)


class Config:
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
            if proc.name() == Config.nom_proc_pg:
                l.append(proc)

        if len(l) == 0:
            return False
        else:
            return True


    def test_connexion():
        # voir https://pynative.com/python-postgresql-tutorial/#h-install-psycopg2-using-the-pip-command
        # et le scrip en bas pour capturer les erreurs
        try:
            connexion = psycopg2.connect(user=Config.nom_utilisateur_pg, host=Config.host, port=Config.port,
                                         database=Config.nom_bdd_pg)
            cursor = connexion.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")
            cursor.close
            connexion.close
            print("Postgre connection is closed")

        except Exception as error:
            print("Error while connecting to Postgre", error)
        finally:
            print("Tests terminés")

    def running_test():
        CheckPostgre.postgre_isrunning()
        CheckPostgre.test_connexion()



# Script de test

CheckPostgre.running_test()



# TODO : prévoir des logs pour enregistrer les test https://www.youtube.com/watch?v=-ARI4Cz-awo
# TODO : interaction pappers pour récuperer les actes

