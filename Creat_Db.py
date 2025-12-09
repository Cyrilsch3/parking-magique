import sqlite3
import os
import sys
import traceback

fichier_db = "parking.db"


if os.path.exists(fichier_db):
    print(f"La base '{fichier_db}' existe déjà. Connexion en cour...")
else:
    print(f"La base de donnée '{fichier_db}' n'existe pas. Création en cour...")
    
    

