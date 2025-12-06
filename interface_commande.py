from les_classes import Parking
from les_classes import Tarif
from les_classes import Place
from les_classes import Abonnement


mdp = "Bonjour"

def ecran_locked():
    global mdp
    entree_mdp = ""
    while entree_mdp != mdp:
        entree_mdp = input("Veuillez entrer votre mot de passe : ")
        if entree_mdp != mdp:
            print("Mauvais mot de passe, recommencez")
    menu_demarrage()


def menu_demarrage():
    print("\n--------------------- Bienvenue au parking magique ! ------------------------\n")
    print("[0] Eteindre")
    print("[1] Stat parking")
    print("[2] Arrivée véhicule")
    print("[3] Sortie véhicule")
    print("[4] Abonnement")
    print("[5] Paramètres")

    while True:
        try:
            choix = int(input("\nVotre choix : "))

            if choix == 0:
                ecran_locked()
            elif choix == 1:
                stat_parking()
            elif choix == 2:
                arrivee_vehicule()
            elif choix == 3:
                sortie_vehicule()
            elif choix == 4:
                menu_abonnement()
            elif choix == 5:
                menu_parametres()
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def stat_parking():
    print("\nLes stats du parking sont .....\n")
    while True:
        try:
            retour = int(input("[0] Retour\n"))
            if retour == 0:
                menu_demarrage()
                return
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def arrivee_vehicule():
    print("\nArrivée véhicule : faites votre choix\n")
    print("[0] Retour")
    print("[1] Attribuer place")
    print("[2] Abonnement")

    while True:
        try:
            choix = int(input("\nVotre choix : "))
            if choix == 0:
                menu_demarrage()
                return
            elif choix == 1:
                print("\nVotre place se trouve ...")
            elif choix == 2:
                print("Menu abonnement")
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def sortie_vehicule():
    print("\nLe prix à payer est de ....")
    while True:
        try:
            choix = int(input("\n[0] Retour\n"))
            if choix == 0:
                menu_demarrage()
                return
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def menu_abonnement():
    print("\nMenu abonnement")
    while True:
        try:
            choix = int(input("\n[0] Retour\n"))
            if choix == 0:
                menu_demarrage()
                return
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def menu_parametres():
    global mdp

    print("\n------------------ Paramètres -------------------\n")
    print("[0] Retour")
    print("[1] Changer le mot de passe")
    print("[2] Changer les tarifs")

    while True:
        try:
            choix = int(input("\nVotre choix : "))
            if choix == 0:
                menu_demarrage()
                return

            elif choix == 1:
                ancien = input("Ancien mot de passe : ")
                if ancien == mdp:
                    mdp = input("Nouveau mot de passe : ")
                    print("Mot de passe changé.")
                else:
                    print("Mot de passe incorrect.")
                menu_demarrage()
                return

            elif choix == 2:
                print("Liste des tarifs…")
            else:
                print("Choix invalide.")

        except ValueError:
            print("Veuillez entrer un nombre entier.")


# Lancement du programme
ecran_locked()
