from les_classes import Parking
from les_classes import Tarif
from les_classes import Place
from les_classes import Abonnement
from les_classes import ajout_des_donnees_du_client
from datetime import datetime, date


ajout_des_donnees_du_client()
def confirmation(question):
    reponse = input(f"{question}  (o/n) : ").strip().lower()
    return reponse in ['o', 'oui', 'y', 'yes']



# mdp = "Bonjour"

# def ecran_locked():
#     global mdp
#     entree_mdp = ""
#     while entree_mdp != mdp:
#        entree_mdp = input("Veuillez entrer votre mot de passe : ")
#        if entree_mdp != mdp:
#            print("Mauvais mot de passe, recommencez")
#    menu_demarrage()


def menu_demarrage():
    print("\n--------------------- Bienvenue au parking magique ! ------------------------\n")
    #print("[0] Eteindre")
    print("[1] Statistique parking")
    print("[2] Arrivée véhicule")
    print("[3] Sortie véhicule")
    print("[4] Abonnement")
    print("[5] Paramètres")

    while True:
        try:
            choix = int(input("\nVotre choix : "))

            # if choix == 0:
            #     ecran_locked()
            if choix == 1:
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
    liste_place = Parking.liste_place()
    nbr_places = len(liste_place)
    #print(nbr_places)
    
    liste_place_libre = Parking.places_libres()
    nbr_place_libre = len(liste_place_libre)
    #print(nbr_place_libre)
    
    liste_place_occupe = Parking.places_occupees()
    nbr_place_occupe = len(liste_place_occupe)
    #print(nbr_place_occupe)
    
    liste_place_reservee = Parking.places_abonnes()
    nbr_place_reservee = len(liste_place_reservee)
    
    pourcentage_places_libres = round((nbr_place_libre / nbr_places) * 100, 2) if nbr_places else 0
    taux_occupation = round(100 - pourcentage_places_libres,1)
    print("\n--- Statistiques du Parking ---")
    print(
    "Il y'a actuellement :\n"
    f"- {nbr_place_libre} places libres\n"
    f"- {nbr_place_occupe} places occupées\n"
    f"- {nbr_place_reservee} places réservées\n"
)
    print(f"Le taux d'occupation du parking est de {taux_occupation } %\n")
   
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
    print("[2] prendre un Abonnement")

    while True:
        try:
            choix = int(input("\nVotre choix : "))
            if choix == 0:
                menu_demarrage()
                return
            elif choix == 1:
                print("Entrer la plaque de votre véhicule")
                plaque = input("\nVotre plaque : ")
                print(f"Voici les places Libres :")
                for i in Parking.places_libres():
                    print(i.id)
                choix_place = input("\nVotre choix de place: ")
                print(Parking.occuper_place(choix_place,plaque))
                menu_demarrage()
            elif choix == 2:
                menu_abonnement()
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def sortie_vehicule():
    liste_place_occupe = Parking.places_occupees()
    tab =[]
    print(f"Voici les places occupées :")
    for i in liste_place_occupe:
        print(i.id)
        
    prix = 0
    place = input("Entrez l'id de la place a liberer ")
    retour = Parking.liberer_place(place)
    if retour[0] == True: 
        print(retour[1])
    else:
        print(retour[1])
    
    menu_demarrage()
    while True:
        try:
            choix = int(input("\n[0] Retour\n"))
            if choix == 0:
                menu_demarrage()
                
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def menu_abonnement():

    print("Abonnement existant ? \n[0] Non \n[1] Oui \n[2] Annuler")
    
    while True:
        try: 
            choix_creation_abo = int(input("Votre choix : ").strip())

            # ------------ CREATION ABONNEMENT ------------
            if choix_creation_abo == 0:
                print("\n--- Création abonnement ---\n")
                nom_client = input("Entrez le nom du client : ")
                prenom_client = input("Entrez le prénom du client : ")
                plaque_client = input("Entrez la plaque d'immatriculation du client : ")
                duree_abonnement = int(input("Entrez la durée de l'abonnement (en mois) : "))

                # ---- DATE DEBUT ----
                while True:
                    choix_date_debut = int(input("Voulez vous une date de début ?\n[0] Non\n[1] Oui : "))

                    if choix_date_debut == 0:
                        date_debut_abonnement = date.today()
                        print(f"Votre abonnement commence le {date_debut_abonnement}")
                        break

                    elif choix_date_debut == 1:
                        while True:
                            date_str = input("Entrer une date (dd-mm-yy) : ")
                            try:
                                date_debut_abonnement = datetime.strptime(date_str, "%d-%m-%y").date()
                                break
                            except ValueError:
                                print("Format invalide, réessayez.")
                        break

                    else:
                        print("Mauvaise entrée.")

                # ---- PLACE RÉSERVÉE ----
                while True:
                    choix_place_reserve = int(input("Souhaitez-vous une place réservée ?\n[0] Oui\n[1] Non\n[2] Retour\nVotre choix : "))

                    if choix_place_reserve == 0:
                        place_reserve = input("Quelle place souhaitez-vous réserver ? : ")
                        break
                    elif choix_place_reserve == 1:
                        place_reserve = None
                        break
                    elif choix_place_reserve == 2:
                        return menu_demarrage()
                    else:
                        print("Choix non valide.")

                nouvel_abo = Abonnement(
                    nom=nom_client,
                    prenom=prenom_client,
                    plaque=plaque_client,
                    duree=duree_abonnement,
                    date_debut=date_debut_abonnement,
                    place_attribuee=place_reserve
                )
                #Parking.ajouter(nouvel_abo)

                print("\nAbonnement enregistré avec succès !")
                return menu_demarrage()


            # ------------ ABONNEMENT EXISTANT ------------
            elif choix_creation_abo == 1:
                print("--- Abonnement existant ---")

                while True:
                    choix_abo_existant = int(input(
                        "Que voulez-vous faire ?\n[0] Prolonger\n[1] Modifier\n[2] Retour\nVotre choix : "
                    ))

                    # --- PROLONGER ---
                    if choix_abo_existant == 0:
                        id_abo = input("ID de l'abonnement : ")
                        nb_mois = int(input("Nombre de mois à ajouter : "))

                        success, message = Parking.allonger_abonnement(id=id_abo, nb_mois=nb_mois)
                        print(message)

                        if not success:
                            continue

                        return menu_demarrage()

                    # --- MODIFIER ---
                    elif choix_abo_existant == 1:
                        id_abo = input("ID de l'abonnement : ")
                        modif = int(input("Modifier :\n[0] Plaque\n[1] Place\n[2] Retour : "))

                        if modif == 0:
                            nouvelle_plaque = input("Nouvelle plaque : ")

                            result = Parking.modifier_abonnement(id=id_abo, plaque=nouvelle_plaque)
                            print(result)

                        elif modif == 1:
                            nouvelle_place = input("Nouvelle place : ")

                            result = Parking.modifier_abonnement(id=id_abo, place_id=nouvelle_place)
                            print(result)

                        elif modif == 2:
                            return menu_demarrage()
                        else:
                            print("Choix invalide")

                    # --- RETOUR ---
                    elif choix_abo_existant == 2:
                        return menu_demarrage()
                    else:
                        print("Choix invalide")
            elif choix_creation_abo == 2:
                return menu_demarrage
            else:
                print("Choix invalide")
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
menu_demarrage()
