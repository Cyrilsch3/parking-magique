from les_classes import Parking
from les_classes import Tarif
from les_classes import Place
from les_classes import Abonnement
from les_classes import ajout_des_donnees_du_client
from les_classes import DateAbonnementInvalide
from les_classes import PlaceInvalideException
from datetime import datetime, date
import os
import json


def afficher_places_par_etage(places):
    etage_actuel = None
    buffer = []

    for place in places:
        etage = place.id[0]

        if etage != etage_actuel:
            if buffer:
                afficher_buffer(buffer)
                buffer = []
            etage_actuel = etage
            print(f"\nÉtage {etage} :")

        buffer.append(place.id)

    if buffer:
        afficher_buffer(buffer)


def afficher_buffer(buffer, par_ligne=3):
    for i in range(0, len(buffer), par_ligne):
        print("   -   ".join(buffer[i:i + par_ligne]))

def charger_parking_depuis_fichier(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Chargement des places
    Parking.set_places([])  # réinitialiser
    for p in data.get("places", []):
        place = Place(
            etage=p["etage"],
            zone=p["zone"],
            numero=p["numero"],
            type_place=p["type_place"],
            plaque=p.get("plaque")
        )
        # Restaurer la date de temp si présente
        temp_str = p.get("temp")
        if temp_str:
            place.temp = datetime.fromisoformat(temp_str)
        else:
            place.temp = None

    # Chargement des abonnements
    Parking.set_abonnements([])  # réinitialiser
    for a in data.get("abonnements", []):
        date_debut = datetime.fromisoformat(a["date_debut"]).date()
        abonnement = Abonnement(
            nom=a["nom"],
            prenom=a["prenom"],
            plaque=a["plaque"],
            duree=a["duree"],
            date_debut=date_debut,
            place_attribuee=a.get("place")
        )

    # Restaurer les tarifs
    tarifs = data.get("tarifs", {})
    Tarif._gratuit_minutes = tarifs.get("gratuit_minutes", Tarif._gratuit_minutes)
    Tarif._prix_premiere_heure = tarifs.get("prix_premiere_heure", Tarif._prix_premiere_heure)
    Tarif._prix_deuxieme_heure = tarifs.get("prix_deuxieme_heure", Tarif._prix_deuxieme_heure)
    Tarif._prix_heures_suivantes = tarifs.get("prix_heures_suivantes", Tarif._prix_heures_suivantes)
    Tarif._prix_max_10h = tarifs.get("prix_max_10h", Tarif._prix_max_10h)
    Tarif._prix_abonnement_simple = tarifs.get("prix_abonnement_simple", Tarif._prix_abonnement_simple)
    Tarif._prix_abonnement_reserver = tarifs.get("prix_abonnement_reserver", Tarif._prix_abonnement_reserver)

# --- Initialisation du parking ---

# --- Nouvelle logique de chargement du backup le plus récent ---
import glob

def charger_dernier_backup():
    # Cherche tous les fichiers de sauvegarde de type parking_*.json (pas parking.json)
    fichiers = glob.glob("parking_*.json")
    # Si aucun fichier, on initialise avec les données du client
    if not fichiers:
        ajout_des_donnees_du_client()
        return
    # Trie les fichiers par date extraite du nom (format parking_YYYY-MM-DD_HH-MM-SS.json)
    from datetime import datetime
    def extract_date(fn):
        try:
            # Format attendu : parking_YYYY-MM-DD_HH-MM-SS.json
            base = fn.replace('parking_', '').replace('.json', '')
            return datetime.strptime(base, '%Y-%m-%d_%H-%M-%S')
        except Exception:
            return datetime.min
    fichiers.sort(key=extract_date)
    dernier = fichiers[-1]
    charger_parking_depuis_fichier(dernier)

charger_dernier_backup()

    
    
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
    print(f"Sauvegarde auto")
    print(Parking.save_all())
    
    print("\n--------------------- Bienvenue au parking magique ! ------------------------\n")
    print("[0] Sauvegarder")
    print("[1] Statistique parking")
    print("[2] Arrivée véhicule")
    print("[3] Sortie véhicule")
    print("[4] Abonnement")
    print("[5] Paramètres")

    while True:
        
        try:
            choix = int(input("\nVotre choix : "))
            
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
            elif choix == 0:
                print(Parking.save_all())
                menu_demarrage()
            else:
                print("Choix invalide.")
        except ValueError:
            print("Veuillez entrer un nombre entier.")
        except EOFError:
            print("\nEntrée interrompu. Extinction.")
            break


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
    os.system('cls')
    print("\n--- Statistiques du Parking ---")
    print(
    "Etat acuel du parking :\n"
    f"- Places libres : {nbr_place_libre}\n"
    f"- Places occupées : {nbr_place_occupe}\n"
    f"- Places réservées : {nbr_place_reservee}\n"
)
    print(f"Le taux d'occupation du parking est de {taux_occupation } %\n")
   
    while True:
        try:
            retour = int(input("[0] Retour\n"))
            if retour == 0:
                menu_demarrage()
                return
            else:
                print("Choix invalide (Tapez [0]).")
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def arrivee_vehicule():
    historique_choix = [] 

    os.system('cls')
    while True:
        print("\nArrivée véhicule : faites votre choix\n")
        print("[0] Retour")
        print("[1] Attribuer une place")
        print("[2] Prendre un abonnement")

        try:
            choix = int(input("\nVotre choix : "))
            historique_choix.append(choix)  
        except ValueError:
            print("Veuillez entrer un nombre entier.")
            continue

        # ----- RETOUR -----
        if choix == 0:
            print("Historique des choix :", historique_choix)
            menu_demarrage()
            return

        # ----- ATTRIBUTION DE PLACE -----
        elif choix == 1:
            os.system('cls')
            plaque = input("Entrer la plaque du véhicule : ").strip().upper()

            places_libres = sorted(Parking.places_libres(), key=lambda p: p.id)
            if not places_libres:
                os.system('cls')
                print("Aucune place libre disponible.")
                continue

            print("\nVoici les places libres :")
            afficher_places_par_etage(places_libres)

            choix_place = input("\nVotre choix de place : ").strip().upper()
            try:
                message = Parking.occuper_place(choix_place,plaque)
                print(message)
            except PlaceInvalideException as e:
                print(f"erreur : {e}")

            input("\nAppuyez sur Entrée pour revenir au menu...")
            print("Historique des choix :", historique_choix)
            menu_demarrage()
            return

        # ----- ABONNEMENT -----
        elif choix == 2:
            menu_abonnement()
            return

        else:
            print("Choix invalide.")


def sortie_vehicule():
    places_occupees = Parking.places_occupees()

    if not places_occupees:
        os.system('cls')
        print("Aucune place occupée.")
        input("Appuyez sur Entrée pour revenir au menu...")
        menu_demarrage()
        return

    os.system('cls')
    print("\nVoici les places occupées :")
    for place in places_occupees:
        print(f" - {place.id}")

    place_id = input("\nEntrez l'ID de la place à libérer : ").strip().upper()

    success, message = Parking.liberer_place(place_id) # optimisation des interaction du code récupère deucx valeurs en 1 appel 
    print(message)

    input("\nAppuyez sur Entrée pour revenir au menu...")
    menu_demarrage()

def menu_abonnement():
    print("Abonnement existant ? \n[0] Non \n[1] Oui \n[2] Annuler")

    while True:
        try:
            choix_creation_abo = int(input("Votre choix : ").strip())

            # ------------ CREATION ABONNEMENT ------------
            if choix_creation_abo == 0:
                os.system('cls')
                print("\n--- Création abonnement ---\n")
                nom_client = input("Entrez le nom du client : ")
                prenom_client = input("Entrez le prénom du client : ")
                plaque_client = input("Entrez la plaque d'immatriculation du client : ")
                duree_abonnement = int(input("Entrez la durée de l'abonnement (en mois) : "))

                # ---- DATE DEBUT ----
                try:
                    date_debut_abonnement = date.today()

                    while True:
                        try:
                            # On protège l'input contre une interruption brutale (Ctrl+C)
                            choix_date = input("Définir une date de début personnalisée ?\n[0] Non (Aujourd'hui)\n[1] Oui\nVotre choix : ").strip()
                        except (KeyboardInterrupt, EOFError):
                            print("\nAnnulation par l'utilisateur.")
                            break 
                        
                        if choix_date == "0":
                            break 
                        
                        elif choix_date == "1":
                            while True:
                                try:
                                    date_str = input("Entrer une date (format JJ-MM-AA) : ").strip()
                                    date_saisie = datetime.strptime(date_str, "%d-%m-%y").date()

                                    if date_saisie < date.today():
                                        print("Erreur : La date ne peut pas être dans le passé.")
                                    else:
                                        date_debut_abonnement = date_saisie
                                        break 
                                except ValueError:
                                    print("Format invalide. Utilisez le format Jour-Mois-Année (ex: 25-12-24).")
                                except (KeyboardInterrupt, EOFError):
                                    print("\nAnnulation de la saisie.")
                                    break # On sort de la boucle de date
                            break 
                        
                        else:
                            print("Choix invalide. Tapez 0 ou 1.")

                    # Résumé et fin
                    # On ajoute un try ici au cas où les variables (nom_client, etc.) n'auraient pas été définies avant
                    try:
                        print(f"\nSuccès ! Abonnement créé pour {nom_client} {prenom_client}.")
                        print(f"Début : {date_debut_abonnement}")
                        print(f"Plaque : {plaque_client} | Durée : {duree_abonnement} mois.")
                    except NameError as e:
                        print(f"Erreur lors de l'affichage du résumé : variable manquante ({e}).")

                except Exception as e:
                    # Filet de sécurité global pour toute autre erreur imprévue
                    print(f"Une erreur inattendue est survenue : {e}")

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
                    plaque=plaque_client.strip().upper(),
                    duree=duree_abonnement,
                    date_debut=date_debut_abonnement,
                    place_attribuee=place_reserve.strip().upper() if place_reserve else None
                )
                # Calcul et affichage du prix de l'abonnement
                prix_mensuel = Tarif.prix_abonnement_reserver() if nouvel_abo.place else Tarif.prix_abonnement_simple()
                prix_total = nouvel_abo.duree * prix_mensuel
                print(f"Prix à payer pour cet abonnement : {prix_total}€")

                print("\nAbonnement enregistré avec succès !")
                return menu_demarrage()

            # ------------ ABONNEMENT EXISTANT ------------
            elif choix_creation_abo == 1:
                print("--- Liste de tous les abonnements ---")
                print("{:<7} {:<15} {:<15} {:<15} {:<12} {:<12}".format("ID", "Nom", "Prénom", "Plaque", "Place", "Fin"))
                print("-" * 80)
                for abo in Parking.abonnements():
                    print("{:<7} {:<15} {:<15} {:<15} {:<12} {:<12}".format(
                        abo.id,
                        abo.nom,
                        abo.prenom,
                        abo.plaque,
                        abo.place if abo.place else "-",
                        abo.date_fin().strftime("%Y-%m-%d")
                    ))
                print("-" * 80)

                while True:
                    choix_abo_existant = int(input(
                        "Que voulez-vous faire ?\n[0] Prolonger\n[1] Modifier\n[2] Retour\nVotre choix : "
                    ))

                    # --- PROLONGER ---
                    if choix_abo_existant == 0:
                        id_abo = input("ID de l'abonnement à prolonger : ")
                        nb_mois = int(input("Nombre de mois à ajouter : "))

                        success, message = Parking.allonger_abonnement(id=id_abo, nb_mois=nb_mois)
                        print(message)

                        if not success:
                            continue

                        return menu_demarrage()

                    # --- MODIFIER ---
                    elif choix_abo_existant == 1:
                        id_abo = input("ID de l'abonnement à modifier : ")
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
                return menu_demarrage()
            else:
                print("Choix invalide")
        except ValueError:
            print("Veuillez entrer un nombre entier.")




def menu_parametres():

    print("\n------------------ Paramètres -------------------\n")
    print("[0] Retour")
    print("[1] Changer les tarifs")

    while True:
        try:
            choix = int(input("\nVotre choix : "))
            if choix == 0:
                menu_demarrage()
                return

            elif choix == 1:
                print(f"Que voulez vous modifier ? ")
                print(f"[0] Rien, retour au menu")
                print(f"[1] Période gratuite, actuellement : {Tarif.gratuit_minutes()} minutes")
                print(f"[2] Prix première heure, actuellement : {Tarif.prix_premiere_heure()}€")
                print(f"[3] Prix deuxième heure, actuellement : {Tarif.prix_deuxieme_heure()}€")
                print(f"[4] Prix heures suivantes, actuellement : {Tarif.prix_heures_suivantes()}€")
                print(f"[5] Prix pour +10h, actuellement : {Tarif.prix_max_10h()}€")
                print(f"[6] Prix abonnement simple, actuellement : {Tarif.prix_abonnement_simple()}€")
                print(f"[7] Prix abonnement place réservée, actuellement : {Tarif.prix_abonnement_reserver()}€")
                while True:
                    try:
                        choix = int(input(f"Votre choix : "))
                        if choix == 0 :
                            menu_demarrage()
                        elif choix == 1 :
                            try:
                                new_value = int(input("Nouvelle période gratuite en minute : "))
                            except ValueError:
                                print("Veuillez entrer un nombre entier.")
                                continue
                            success, message = Tarif.set_gratuit_minutes(new_value)
                            print(message)
                            if not success:
                                continue
                            menu_parametres()
                        elif choix == 2 :
                            try:
                                new_value = float(input("Nouveau tarif première heure : "))
                            except ValueError:
                                print("Veuillez entrer un nombre.")
                                continue
                            success, message = Tarif.set_prix_premiere_heure(new_value)
                            print(message)
                            if not success:
                                continue
                            menu_parametres()
                        elif choix == 3 :
                            try:
                                new_value = float(input("Nouveau tarif deuxième heure : "))
                            except ValueError:
                                print("Veuillez entrer un nombre.")
                                continue
                            success, message = Tarif.set_prix_deuxieme_heure(new_value)
                            print(message)
                            if not success:
                                continue
                            menu_parametres()
                        elif choix == 4 :
                            try:
                                new_value = float(input("Nouveau tarif heures suivantes : "))
                            except ValueError:
                                print("Veuillez entrer un nombre.")
                                continue
                            success, message = Tarif.set_prix_heures_suivantes(new_value)
                            print(message)
                            if not success:
                                continue
                            menu_parametres()
                        elif choix == 5 :
                            try:
                                new_value = float(input("Nouveau prix pour +10h : "))
                            except ValueError:
                                print("Veuillez entrer un nombre.")
                                continue
                            success, message = Tarif.set_prix_max_10h(new_value)
                            print(message)
                            if not success:
                                continue
                            menu_parametres()
                        elif choix == 6 :
                            try:
                                new_value = float(input("Nouveau tarif abonnement simple : "))
                            except ValueError:
                                print("Veuillez entrer un nombre.")
                                continue
                            success, message = Tarif.set_prix_abonnement_simple(new_value)
                            print(message)
                            if not success:
                                continue
                            menu_parametres()
                        elif choix == 7 :
                            try:
                                new_value = float(input("Nouveau tarif abonnement place réservée : "))
                            except ValueError:
                                print("Veuillez entrer un nombre.")
                                continue
                            success, message = Tarif.set_prix_abonnement_reserver(new_value)
                            print(message)
                            if not success:
                                continue
                            menu_parametres()
                        else:
                            print("Choix invalide")
                    except ValueError:
                        print("Veuillez entrer un nombre entier.")
                
                
                
            else:
                print("Choix invalide.")

        except ValueError:
            print("Veuillez entrer un nombre entier.")


# Lancement du programme
menu_demarrage()
