import sqlite3
import os
import sys
import traceback

fichier_db = "parking.db"

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
        CREATE TABLE IF NOT EXISTE tb_palces (
        id_place text NOT NULL PRIMARY KEY,
        id_type_place text NOT NULL,
        etage text NOT NULL,
        numero text NOT NULL,
        zone text NOT NULL,
        FOREIGN KEY (id_type_place) REFERENCES tb_typePlaces(id_type_place)
        );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTE tb_typePlaces (
    id_type_place NOT NULL PRIMARY KEY 
    nom_type NULL 
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_reservation (
    id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    plaque_imma TEXT NOT NULL,
    id_place TEXT NOT NULL,
    FOREIGN KEY (plaque_imma) REFERENCES tb_abonne(plaque_imma),
    FOREIGN KEY (id_place) REFERENCES tb_places(id_place) 
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_tarifs (
    id_tarif TEXT PRIMARY KEY AUTOINCREMENT,
    nom_tarif TEXT NULL
    valeur_EURO_Tarif INTEGER NOT NULL
    );
    """)

    conn.commit()  # Sauvegarder les changements (création de table)
    print("Tables vérifiées/créées avec succès.")

except sqlite3.Error as e:
    # Capture toutes les erreurs spécifiques à SQLite
    print(f"Une erreur SQLite est survenue lors de la connexion ou de l'exécution : {e}")

except Exception as e:
    # Capture toutes les autres erreurs imprévues
    print(f"Une erreur inattendue est survenue : {e}")

finally:
    # La connexion est fermée, même en cas d'erreur
    if 'conn' in locals() and conn:
        conn.close()
        print("Connexion à la base de données fermée.")