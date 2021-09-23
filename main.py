# coding:utf-8

"""
Petit programme pour vérifier si le service postgre est lancé.
Pour mémoire on lance le service postgre par la commande rc-service postgresql-13 start, mais cela va lancer le processus
postgres VIA l'utilisateur postgres.
"""

import psutil
import psycopg2
import logging

from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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

        """Renvoi False si aucun processus postgre n'est trouvé. Renvoi True et log la liste des processus sinon"""

        l = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.name() == ConfigPostgre.nom_proc_pg:
                l.append(proc)

        if len(l) == 0:
            logging.critical("Pas de processus postgre trouvé")
            return False
        else:
            logging.debug(f"Service postgre: {l}")
            return True

    def connexion_isok():
        try:
            connexion = psycopg2.connect(user=ConfigPostgre.nom_utilisateur_pg, host=ConfigPostgre.host,
                                         port=ConfigPostgre.port,
                                         database=ConfigPostgre.nom_bdd_pg)
            cursor = connexion.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            logging.debug(record)
            cursor.close
            connexion.close
            print("Test de connexion réussi")

        except Exception as error:
            logging.critical(error)
            print("Erreur lors du connexion : ", error)

    def running_test():
        CheckPostgre.postgre_isrunning()
        CheckPostgre.connexion_isok()


"""
On passe au table de la base de donnée
"""

Base = declarative_base()


class Societe(Base):
    __tablename__ = "societe"
    siren = Column(Integer, primary_key=True)
    nom = Column(Text)

    def __init__(self, numero_siren, nom_entreprise):
        self.siren = numero_siren
        self.nom = nom_entreprise

    def ___str__(self):
        return self.nom + ":" + self.siren


def connexion_bdd():
    """Renvoi les objets engine session pour la connexion future"""

    engine_config = str(
        'postgresql+psycopg2://' + ConfigPostgre.nom_utilisateur_pg + '@' + ConfigPostgre.host + ':' + ConfigPostgre.port + '/' + ConfigPostgre.nom_bdd_pg)
    engine = create_engine(engine_config, echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session


### Scritp pour tester le connexion ###
"""


google = Societe(890765453, "Google")
session.add(google)
session.commit()
"""


### Code du GUI ###

def menu():
    print()
    print(f"*** PYTHON POSTGRESQL API ***")
    print()
    print("1. Tester la connexion au serveur postgre")
    print("2. Créer la table société")
    print("3. Effacer la table société")
    print("4. Lister les Siren")
    print("5. Ajouter un Siren")
    print("6. Effacer un Siren")
    print("Q : Pour quitter")
    print()


flag = True
choix_possible = ("1 2 3 4 5 6 Q")
liste_choix_possible = choix_possible.split()

while flag:
    menu()
    choix = input("Votre choix : ")

    if choix not in liste_choix_possible:
        print("Choix non permis")
    if choix == "1":
        CheckPostgre.running_test()

    if choix == "2":
        engine, session = connexion_bdd()
        Base.metadata.create_all(bind=engine,
                                 tables=[Base.metadata.tables["societe"]])  # Creation de la table société uniquement
        print("Table créée")

    if choix == "3":
        engine, session = connexion_bdd()
        Base.metadata.drop_all(bind=engine,
                               tables=[Base.metadata.tables["societe"]])
        print("Table effacée")

    if choix == "4":
        pass
        # TODO : A coder

    # TODO : Dans l'immediat : créer une table et permettre d'inserer des siren
# TODO : prévoir des logs pour enregistrer les test https://www.youtube.com/watch?v=-ARI4Cz-awo
# TODO :        Petit script simple pour enregistrer des informations dans la basse de données (Siren) soit un par un soit via une liste.
# TODO suite :  Utiliser argparse pour ça
# TODO Interaction avec pappers pour récuperer le nom de la société
