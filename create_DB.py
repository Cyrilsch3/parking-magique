import sqlite3
import os
import sys
import traceback

fichier_db = "parking.db"

# on try except pour s'assuer que la base de donnée ce crée bien mais surtout pour attraper d'éventuel erreurs on commence par verifier si la db existe!!
try:
    if os.path.exists(fichier_db):
        print(f"La base '{fichier_db}' existe déjà. Connexion en cour...")
    else:
        print(f"La base de donnée '{fichier_db}' n'existe pas. Création en cour...")
    
    # connexion a la base de donnée (elle sera crée si elle n'existe pas)

    conn = sqlite3.connect(fichier_db)
    cursor = conn.cursor()

    # Creation des tables (On prévoie l'éventualité que ma table existe déjà)

    cursor.execute("""
     

    """)
except ValueError:
    print("Une erreur est survenue!")
