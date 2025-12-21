import sqlite3
import os
import sys
import traceback
from Erreur_perso.ERREURS import ErreurDansLaDB

fichier_db = "parking.db"

def creeTables():
    """
    Docstring for creeTables : 
    cette fonction sera lancer des l'ctivation du programme et son initalisation, elle va vérifier l'exsitance du fichier de la db
    si non exsistante elle va la créé dans le bon fichier. 
    """
    try:
        if os.path.exists(fichier_db):
            print(f"La base '{fichier_db}' existe déjà. Connexion en cours...")
        else:
            print(f"La base de donnée '{fichier_db}' n'existe pas. Création en cours...")

        # Connexion à la base de donnée (elle sera créée si elle n'existe pas)
        # L'exception de connexion peut être capturée par sqlite3.Error

        conn = sqlite3.connect(fichier_db)
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON;")

        # Création des tables
        # Note : ICI les tables sont crée une fois si elle existe déjà elle ne seront pas crée ni instencier a nouveau 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_abonne (
            id_abbo text NOT NULL,
            plaque_imma text NOT NULL PRIMARY KEY,
            nom text NOT NULL,
            prenom text NOT NULL,
            place_res text NULL,
            duree INTEGER NOT NULL,
            date_debut DATE NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_places (
            id_place text NOT NULL PRIMARY KEY,
            id_type_place text NOT NULL,
            etage text NOT NULL,
            numero text NOT NULL,
            zone text NOT NULL,
            FOREIGN KEY (id_type_place) REFERENCES tb_typePlaces(id_type_place)
            );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_typePlaces (
        id_type_place TEXT NOT NULL PRIMARY KEY,
        nom_type TEXT NULL 
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_reservation (
        id_reservation  INTEGER PRIMARY KEY AUTOINCREMENT,
        plaque_imma TEXT NOT NULL,
        id_place TEXT NOT NULL,
        FOREIGN KEY (plaque_imma) REFERENCES tb_abonne(plaque_imma),
        FOREIGN KEY (id_place) REFERENCES tb_places(id_place) 
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_tarifs (
        id_tarif INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_tarif TEXT NULL,
        valeur_EURO_Tarif INTEGER NOT NULL
        );
        """)

        conn.commit()  # Sauvegarder les changements (création de table)
        print("Tables vérifiées/créées avec succès.")
        get_tables()

    except sqlite3.Error as e:
        # Capture toutes les erreurs spécifiques à SQLite
        raise ErreurDansLaDB(f"Une erreur SQLite est survenue lors de la connexion ou de l'exécution : {e}") from e

    except Exception as e:
        # Capture toutes les autres erreurs imprévues
        raise ErreurDansLaDB(f"Une erreur inattendue est survenue : {e}") from e

    finally:
        # La connexion est fermée, même en cas d'erreur
        if 'conn' in locals() and conn:
            conn.close()
            print("Connexion à la base de données fermée.")

def get_tables():
    """ Crée un Tuple qui contient la liste de tables dans la base de données"""
    try:
        conn = sqlite3.connect(fichier_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()] # tuple -> string
        return tables

    except sqlite3.Error as a:
        raise ErreurDansLaDB(f"une erreur est survenue lors de la connection a la base de données!! {a}") from a


def verifierTables(table):
    try:
        conn = sqlite3.connect(fichier_db)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from {table}")
        column_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        return rows, column_names



    except sqlite3.Error as e:
       raise ErreurDansLaDB(f"une erreur est survenue lors de la connection a la base de données!! {e}") from e


def afficher_tables(rows, column_names, tables):
    """
    Docstring for afficher_tables
    Affiche la base de donnée en console pour pouvoir visualiser les données
    et aussi avoir plus de contrôle sur les données. 
    """
    print(f"Table : {tables}")

    if not column_names:
        print("(la table est vide ou inaccesible.)")
        return False
    
    tete = " | ".join(column_names)
    print("-" * 10)
    print(f"COLONNES : {tete}")
    print(f"-" * 10)

    if not rows:
        print("-> Aucune données trouver dans cette table.")
    else:
        for row in rows:
            message = " | ".join(map(str, row))
            print(f"Données : {message}")

    print("-" * 20)

creeTables()
for t in get_tables():
    rows, cols = verifierTables(t)
    afficher_tables(rows, cols, t)