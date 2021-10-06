# coding:utf-8

"""
Petit programme pour vérifier si le service postgre est lancé.
Pour mémoire on lance le service postgre par la commande rc-service postgresql-13 start, mais cela va lancer le processus
postgres VIA l'utilisateur postgres.
"""

import psutil
import psycopg2
import logging
import re

import sqlalchemy.orm.exc
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, select
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

    def __init__(self, numero_siren, nom_entreprise="tototo"):
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

def siren_check():
    pattern = '[0-9]'
    siren_saisi = input("Saisisser un Siren : ")
    if len(siren_saisi) != 9:
        print("Un Siren comporte exactement 9 chiffres")
        return 0
    else:
        flag = 0
        for c in siren_saisi:
            result = re.match(pattern, c)
            if not result:
                flag += 1
        if flag != 0:
            print("La chaines doit contenir que des chiffres")
            return 0
        else:
            print("Numero siren valide")
            return int(siren_saisi)


flag = True
choix_possible = ("1 2 3 4 5 6 Q")
liste_choix_possible = choix_possible.split()

while flag:
    menu()
    choix = input("Votre choix : ")

    if choix not in liste_choix_possible:
        print("Choix non permis")

    if choix == "Q":
        print("Exiting ...")
        exit()

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
        engine, session = connexion_bdd()
        liste_siren = session.execute(select(Societe).order_by(Societe.siren))
        i = 1
        for user_obj in liste_siren.scalars():
            print(f"{i}.    {user_obj.siren} : {user_obj.nom}")
            i += 1

    if choix == "5":
        siren_saisi_check = int(siren_check())
        while siren_saisi_check == 0:
            siren_saisi_check = int(siren_check())

        engine, session = connexion_bdd()
        try:
            siren_a_ajouter = Societe(siren_saisi_check)
            session.add(siren_a_ajouter)
            session.commit()
            print("Siren ajouté")
        except:
            print("Siren déjà Saisi")

    if choix == "6":
        siren_saisi_check = int(input("Saisisser un Siren : "))  # TODO : Vérifier la forme du siren + confirmation, faire comme le 5
        engine, session = connexion_bdd()
        try:
            siren_to_delete = session.get(Societe, siren_saisi_check)
            session.delete(siren_to_delete)
            session.commit()
            print("Siren effacé")
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            print("Ce Siren n'existe pas")






#
# TODO :        Petit script simple pour enregistrer des informations dans la basse de données (Siren) soit un par un soit via une liste.
# TODO suite :  Utiliser argparse pour ça
# TODO Interaction avec data.inpi et siren pour récuperer le nom de la société
        # TODO : faire si l'entreprise inconnu data.inpi, recherche sur siren.
