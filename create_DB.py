import sqlite3
import os
import re
from Erreur_perso.ERREURS import ErreurDansLaDB
from functools import wraps
from les_classes import Place, Abonnement
from datetime import date

fichier_db = "parking.db"

# ---------------- Décorateur pour sécuriser l'accès aux tables ----------------
def securiser_table(fonction):
    @wraps(fonction)
    def wrapper(table, *args, **kwargs):
        # Vérification du nom de table (lettres, chiffres, underscore)
        if not re.match(r"^[A-Za-z0-9_]+$", table):
            raise ErreurDansLaDB(f"Nom de table invalide : {table}")
        try:
            return fonction(table, *args, **kwargs)
        except sqlite3.Error as e:
            raise ErreurDansLaDB(f"Erreur SQLite lors de l'opération sur la table '{table}': {e}") from e
        except Exception as e:
            raise ErreurDansLaDB(f"Erreur inattendue lors de l'opération sur la table '{table}': {e}") from e
    return wrapper

# ---------------- Fonction pour créer les tables ----------------
def creeTables():
    try:
        if os.path.exists(fichier_db):
            print(f"La base '{fichier_db}' existe déjà. Connexion en cours...")
        else:
            print(f"La base '{fichier_db}' n'existe pas. Création en cours...")

        conn = sqlite3.connect(fichier_db)
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON;")

        # Création des tables
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
            CREATE TABLE IF NOT EXISTS tb_typePlaces (
                id_type_place TEXT NOT NULL PRIMARY KEY,
                nom_type TEXT NULL 
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

        conn.commit()
        print("Tables vérifiées/créées avec succès.")
        get_tables()

    except sqlite3.Error as e:
        raise ErreurDansLaDB(f"Une erreur SQLite est survenue lors de la création des tables : {e}") from e
    except Exception as e:
        raise ErreurDansLaDB(f"Une erreur inattendue est survenue : {e}") from e
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Connexion à la base de données fermée.")

# ---------------- Fonction pour récupérer la liste des tables ----------------
def get_tables():
    try:
        conn = sqlite3.connect(fichier_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        conn.close()
        return tables
    except sqlite3.Error as a:
        raise ErreurDansLaDB(f"Erreur lors de la récupération des tables : {a}") from a

# ---------------- Fonction pour vérifier les tables ----------------
@securiser_table
def verifierTables(table):
    conn = sqlite3.connect(fichier_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    column_names = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return rows, column_names

# ---------------- Fonction pour afficher les tables ----------------
def afficher_tables(rows, column_names, tables):
    print(f"Table : {tables}")

    if not column_names:
        print("(la table est vide ou inaccessible.)")
        return False
    
    tete = " | ".join(column_names)
    print("-" * 10)
    print(f"COLONNES : {tete}")
    print("-" * 10)

    if not rows:
        print("-> Aucune donnée trouvée dans cette table.")
    else:
        for row in rows:
            message = " | ".join(map(str, row))
            print(f"Données : {message}")

    print("-" * 20)


def charger_places():
    conn = sqlite3.connect(fichier_db)
    cur = conn.cursor()

    cur.execute("""
        SELECT id_place, etage, zone, numero, id_type_place
        FROM tb_places
    """)

    places = []
    for id_place, etage, zone, numero, type_place in cur.fetchall():
        p = Place(
            etage=etage,
            zone=zone,
            numero=numero,
            type_place=type_place,
            plaque=None
        )
        places.append(p)

    conn.close()
    return places

def charger_abonnements():
    conn = sqlite3.connect(fichier_db)
    cur = conn.cursor()

    cur.execute("""
        SELECT id_abbo, nom, prenom, plaque_imma, duree, date_debut, place_res
        FROM tb_abonne
    """)

    abos = []
    for id_, nom, prenom, plaque, duree, date_debut, place in cur.fetchall():
        a = Abonnement(
            nom=nom,
            prenom=prenom,
            plaque=plaque,
            duree=duree,
            date_debut=date.fromisoformat(date_debut),
            place_attribuee=place
        )
        a._id = id_ 
        abos.append(a)

    conn.close()
    return abos

for t in get_tables():
    rows, cols = verifierTables(t)
    afficher_tables(rows, cols, t)