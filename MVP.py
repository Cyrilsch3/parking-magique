from datetime import datetime 
import os
import unittest


# -------------------- Class --------------------
# ---------- class pour le terminale --------------
class Terminal:
    """
    Initalise un terminale sur lequel le stationneur pourra faire toutes ces commandes et interactions

    le terminale pour hardCoder pour par exemple ajouter des palces, des abbonées et annuler ou commencer des abbonements sur base des info qu'il reçoit
    """
    def __init__(self):
        self.__places = []
        self.__abbonnes = []
        self.initalise_donnees()
        self.ajouter_abonne()
        self.lancerTerminal()
    @property
    def abbonnes(self):
        return self.__abbonnes

    @property
    def places(self):
        return self.__places
    
    def initalise_donnees(self):
            """
            Ici on ajoute les abbonées et toutes les palces de parkin qui existait
            """
            self.__places.append(Place(-1, 'A', '01', 'Compacte'))
            self.__places.append(Place(-1, 'A', '02', 'Compacte'))
            self.__places.append(Place(-1, 'A', '03', 'Compacte'))
            self.__places.append(Place(-1, 'A', '04', 'Compacte'))
            self.__places.append(Place(-1, 'B', '01', 'Compacte'))
            self.__places.append(Place(-1, 'B', '02', 'Compacte'))
            self.__places.append(Place(-1, 'B', '03', 'Compacte'))
            self.__places.append(Place(-1, 'B', '04', 'Compacte'))
            self.__places.append(Place(-1, 'C', '01', 'Large'))
            self.__places.append(Place(-1, 'C', '02', 'Large'))
            self.__places.append(Place(-1, 'C', '03', 'Large'))
            self.__places.append(Place(-1, 'C', '04', 'Large'))
            self.__places.append(Place(0, 'A', '01', 'Large'))
            self.__places.append(Place(0, 'A', '02', 'Large'))
            self.__places.append(Place(0, 'A', '03', 'Large'))
            self.__places.append(Place(0, 'A', '04', 'Large'))
            self.__places.append(Place(0, 'A', '05', 'PMR'))
            self.__places.append(Place(0, 'A', '06', 'PMR'))
            self.__places.append(Place(0, 'B', '01', 'Électrique'))
            self.__places.append(Place(0, 'B', '02', 'Électrique'))
            self.__places.append(Place(0, 'B', '03', 'Compacte'))
            self.__places.append(Place(0, 'B', '04', 'Compacte'))
            self.__places.append(Place(0, 'C', '01', 'Large'))
            self.__places.append(Place(0, 'C', '02', 'Large'))
            self.__places.append(Place(0, 'C', '03', 'Large'))
            self.__places.append(Place(0, 'C', '04', 'Large'))
            self.__places.append(Place(1, 'A', '01', 'Compacte'))
            self.__places.append(Place(1, 'A', '02', 'Compacte'))
            self.__places.append(Place(1, 'A', '03', 'Compacte'))
            self.__places.append(Place(1, 'A', '04', 'Compacte'))
            self.__places.append(Place(1, 'A', '05', 'PMR'))
            self.__places.append(Place(1, 'B', '01', 'Compacte'))
            self.__places.append(Place(1, 'B', '02', 'Compacte'))
            self.__places.append(Place(1, 'B', '03', 'Compacte'))
            self.__places.append(Place(1, 'B', '04', 'Compacte'))
            self.__places.append(Place(1, 'B', '12', 'Large'))
            self.__places.append(Place(1, 'C', '01', 'Large'))
            self.__places.append(Place(1, 'C', '02', 'Large'))
            self.__places.append(Place(2, 'A', '01', 'Compacte'))
            self.__places.append(Place(2, 'A', '02', 'Compacte'))
            self.__places.append(Place(2, 'A', '03', 'Compacte'))
            self.__places.append(Place(2, 'A', '04', 'Compacte'))
            self.__places.append(Place(2, 'A', '05', 'Compacte'))
            self.__places.append(Place(2, 'B', '01', 'Compacte'))
            self.__places.append(Place(2, 'B', '02', 'Compacte'))
            self.__places.append(Place(2, 'B', '03', 'Compacte'))
            self.__places.append(Place(2, 'B', '04', 'Compacte'))
            self.__places.append(Place(2, 'C', '01', 'Électrique'))
            self.__places.append(Place(2, 'C', '02', 'Électrique'))
            self.__places.append(Place(2, 'C', '03', 'Large'))
            self.__places.append(Place(2, 'C', '04', 'Large'))
            self.__places.append(Place(3, 'A', '01', 'Compacte'))
            self.__places.append(Place(3, 'A', '02', 'Compacte'))
            self.__places.append(Place(3, 'A', '03', 'Compacte'))
            self.__places.append(Place(3, 'A', '04', 'Compacte'))
            self.__places.append(Place(3, 'B', '01', 'Compacte'))
            self.__places.append(Place(3, 'B', '02', 'Compacte'))
            self.__places.append(Place(3, 'B', '03', 'Large'))
            self.__places.append(Place(3, 'B', '04', 'Large'))
            self.__places.append(Place(3, 'C', '01', 'Large'))
            self.__places.append(Place(3, 'C', '02', 'Large'))
            self.__places.append(Place(3, 'C', '03', 'Large'))
            self.__places.append(Place(3, 'C', '04', 'Large'))

            self.__abbonnes.append(Abonne("Dupuis", "Marie", "AA-452-KM", 12, datetime(2025, 1, 1).date(), "2A05"))
            self.__abbonnes.append(Abonne("Bernard", "Luc", "DB-793-QF", 6, datetime(2025, 3, 15).date(), "1B02"))
            self.__abbonnes.append(Abonne("Leclerc", "Antoine", "FG-219-LR", 12, datetime(2025, 2, 1).date(), "0A02"))
            self.__abbonnes.append(Abonne("Martin", "Céline", "JH-887-PN", 3, datetime(2025, 4, 1).date(), None))
            self.__abbonnes.append(Abonne("Roche", "Damien", "KL-045-TZ", 12, datetime(2025, 1, 10).date(), None))
            self.__abbonnes.append(Abonne("Morel", "Sophie", "BC-338-JC", 6, datetime(2025, 2, 20).date(), None))
            self.__abbonnes.append(Abonne("Gonzalez", "Thierry", "EV-612-NV", 3, datetime(2025, 4, 5).date(), None))
            self.__abbonnes.append(Abonne("Petit", "Hélène", "QW-901-HS", 12, datetime(2025, 3, 1).date(), None))
        

    # pour faire en sorte que les liste dde données fournie sont bien mise a jour en fonction des abbonnées
    # Il faudra néanmoins crée une méthode dans abbonée qui ajoute les abbonnées dynamiquement !! 
    def ajouter_abonne(self):
        """Ajoute un abonné et réserve automatiquement sa place si elle existe"""
        
        for ab in self.__abbonnes:
            if not ab.place_reservee:
                continue
            for place in self.__places:
                code = f"{place.etage}{place.zone}{place.numero}"
                if code == ab.place_reservee:
                    place.reserver(ab.plaque_voiture)
                    
                    break

    def lancerTerminal(self):
        """
        Cette fonction me sert de console ou d'affichage temporaire l'interface grapique la remplacera une fois le MVP fini
        elle pourra être utiliser pour débug

        on voit une serie de print, ça convient a ce que le MVP pourra faire, une fois bien abouti il y aura bcp plus de fonctions
        """

        print(">>> Lancement du menu interactif... <<<")
        choix = input("\nAppuyez sur [Entrée] pour accèder a la liste D'options du terminal")
        while True:
            choix = ""
            if choix == "":
                print("\n" + "="*150)
                print(f"         MENU DE GESTION DU PARKING Bienvenue MR.stattioneur voici la date u jour : {datetime.today().date()} Que voulez vous faire ?...")
                print("="*150)
                print("\n")
                print("Entrer (avec le numéro en console) ce que vous désirer faire !\n")
                print("1.   Enregistrer l'arriver D'un client.")
                print("2.   Enregistrer le départ d'un client.")
                print("3.   Afficher l'état des Places.")
                print("4.   Verifier le status d'une palce spécifque.")
                print("5.   Consulter la liste d'abonnées.")
                print("6.   Informations sur une voiture donnée gâce a la plaque.")
                print("7.   Quitter le Menu interactif.")

            try:
                choix = input("Sélectionnez une option : ").strip()

            except EOFError:
                print("\nEntrée interrompu. Extinction.")
                break

            if  choix == "1":
                os.system('cls')
                nom = input("Veuillez entrer ne nom du client : ")
                prenom = input("veuillez enetrer le prenom du client : ")
                plaque = input("veuillez entrer la plaque d'immatriculation du client : ")

                self.ArrivéeCleint(nom, prenom, plaque)

            elif choix == "2":
                os.system('cls')
                print("Vous avez choisi l'option numéro 2")

            elif choix == "3":
                os.system('cls')
                print("Vous avez choisi l'option numéro 3")

            elif choix == "4":
                os.system('cls')
                print("Vous avez choisi l'option numéro 4")

            elif choix == "5":
                os.system('cls')
                print("Vous avez choisi l'option numéro 5")
            
            elif choix == "6":
                os.system('cls')
                print("vous avez choisi l'option numéro 6")

            elif choix == "7":
                os.system('cls')
                print("Extinction du terminal, AU revoir !!")
                break
            else:
                os.system('cls')
                print(f"Option {choix} non implémentée dans cette version de test.")
                self.attendre_imput()

    def ArrivéeCleint(self, nom, prenom, plaqueImma, abbo = False):
        """
        cette fonction sera une grosse fonction qui va gérer les nouveau clients, ils pouront choisir si ils s'abbonne ou pas
        :param nom : corréspnd au nom du client 
        :parma prénom : corréspond au prénom du client
        :parma plaqueImma : corréspond a la plaque d'immatriculation du client 
        :abbo corrésond a voir si le client est abbonnée, par défaut false
        """
        print("\n" + "="*50)
        print("Bienvenue dans l'interface d'ajout de client !")
        print("="*50)
        os.system('cls')
        print("\n")
        rep = input(f"Le client {nom} {prenom} immatriculé {plaqueImma} souhaite-t-il un abonnement ? (oui/non) : ").strip().lower()

        if rep == "oui":
            duree = int(input("Durée de l'abonnement en mois : "))
            abonne = Abonne(nom, prenom, plaqueImma, duree)
            # Ajouter l'abonné à la liste __abbonnes
            self.__abbonnes.append(abonne)
            self.ajouter_abonne()
        else:
            abonne = None

        # Chercher une place libre et non réservée
        place_trouvee = None
        for place in self.__places:
            if not place.est_occupe and not place.plaque_reservee:
                # On utilise directement la méthode occuper()
                success = place.occuper(plaqueImma)
                if success:
                    place_trouvee = place
                    break

        if place_trouvee:
            print(f"Place attribuée : {place_trouvee.etage}{place_trouvee.zone}{place_trouvee.numero}")

            # Si c'est un abonné, on réserve sa place
            if abonne:
                abonne.place_reservee = f"{place_trouvee.etage}{place_trouvee.zone}{place_trouvee.numero}"
                # On utilise la méthode reserver()
                place_trouvee.reserver(plaqueImma)
        else:
            print("Désolé, aucune place libre et disponible n'a été trouvée !")


    def attendre_imput(self):
        """
        Une fonction utilitaire pour que l'utilisateur press enter pour revnir au menu de base.
        """
        try:
            input("\nAppuyez sur [Entrée] Pour voir le Menu...")
        except EOFError:
            return

# ---------- class pour les places --------------
class Place:
    """
    Initialise une place dans le parking avec toutes ces infos

    une place est définit cette place ce trouve a un étage reçoit un numéro de place et nous dis si elle est occupé ou pas
    Si occupé la plaue de la voiture est spacifié (bonus : on peux savoir si la place est réservé si le perma self.plaque_reservee n'est pas sur "none")
    """
    def __init__(self,etage,zone,numero,type):
        """
        Initialise une nouvelle place 
        perma : etage : nous donne l'étage de la place 
        perma : numero : nous donne le numéro de la place ainsi que ça zone
        """
        self.etage = etage
        self.zone = zone
        self.numero = numero
        self.type = type
        #--- Attribut d'état interne 
        """
        la place est par défaut libre, il n'y a pas de voiture dessus, elle n'est pas réservée par une voiture
        """
        self.est_occupe = False
        self.voiture = None
        self.plaque_reservee = None
        self.dateArrivee = None

        # Tarifs ponctuels (non abonnés)
        self.tarifs_horaire = [
            ("0-30 min", 0.0),
            ("30 min - 1 h", 2.5),
            ("Par heure supplémentaire", 1.8),
            ("Plafond 24h", 18.0)
        ]

        
    def occuper(self, voiture):
        """
        attribue cette place a une plaque de voiture donnée
        :parma voiture: la plaque d'imatriculation de l'abbonée qui l'occupe
        """
        if self.plaque_reservee and voiture != self.plaque_reservee:
            print(f"l'étage {self.etage}, Place {self.zone + self.numero} est reservée pour {self.plaque_reservee} !")
            print(f"Veuillez introduire une autre place pour vous garer !!")
        if not self.est_occupe:
            self.voiture = voiture
            self.est_occupe = True
            self.dateArrivee = datetime.today()
            print(f"voiture {voiture} garée a l'étage {self.etage}, place {self.numero}")
            return True
        else:
            print(f"L'étage {self.etage}, place {self.numero} est déjà occupée.")
            return False
        
    def parti(self, voiture):
        """
        cette fonction va en gros calculer sur base de la variable tarifs combien le client doit payer quand il veux sortir du parkin
        :parma tarfis: contient tout les tarfis que le client nous a fourni pour calculer combien un client dois payer
        """
        try:
            if self.plaque_reservee:
                print("OUf rien a payer le client garer ici a réserver ça place donc est au tarifs abonnées")
                self.voiture = None
                self.est_occupe = False
                self.dateArrivee = None
            else:
                Temps_du_client = datetime.today() - self.dateArrivee
                Temps_du_client = round(Temps_du_client.total_seconds() / 3600, 2)
        
                if Temps_du_client <= 0.30:
                    print(f"Le client doit payer un motant totale de {self.tarifs_horaire[0][1]}")
                elif Temps_du_client <= 1.00 and Temps_du_client > 0.30:
                    print(f"Le client doit payer un motant totale de {self.tarifs_horaire[1][1]}")
                elif Temps_du_client >= 24.00:
                    print(f"Le cient a atteint le plafond de 24h il payera donc {self.tarifs_horaire[3][1]}")
                else:
                    print(f"Le client doit payer un motant totale de {Temps_du_client * self.tarifs_horaire[2][1]}")
        
            self.voiture = None
            self.est_occupe = False
            self.dateArrivee = None
        except:
            print("Une erreur d'origine inconnue est survenue suite au calcule des tarifs, veuillez contacter le support si l'erreur pérsiste")



    def reserver(self, voiture):
        """
        reserve cette place pour un abbonée l'ors de la création de l'abonée 
        et verifie si celle-ci nest pas déjà reserver, on peux réserver une place si une voiture est déjà garer dessus mais il faudra attrendre que 
        la voiture parte pour pouvoire récuperer ou ce garer sur la place 
        """
        if self.plaque_reservee and self.plaque_reservee != self.voiture:
            print(f"l'étage {self.etage}, Place {self.numero} est reservée pour {self.plaque_reservee} il est donc impossible de vous donner cette place !!")
            return False
        else:
            self.plaque_reservee = voiture
            return True
    

# ---------- class pour les abbonnées  --------------
class Abonne:
    """
    Initialise un abonné qui créera et ajoutera un abonné à une liste d'abonnés
    """
    def __init__(self, nom, prenom, plaque_voiture, duree, date_debut=None, place_reservee=None):
        self.__nom = nom
        self.__prenom = prenom
        self.plaque_voiture = plaque_voiture
        self.__duree = duree
        self.__date_debut = date_debut or datetime.today()
        self.__place_reservee = place_reservee

    # --- Propriétés pour accéder aux attributs privés ---
    @property
    def nom(self):
        return self.__nom

    @property
    def prenom(self):
        return self.__prenom

    @property
    def duree(self):
        return self.__duree

    @property
    def date_debut(self):
        return self.__date_debut

    @property
    def place_reservee(self):
        return self.__place_reservee

    # Optionnel : permettre de modifier la place réservée
    @place_reservee.setter
    def place_reservee(self, nouvelle_place):
        self.__place_reservee = nouvelle_place


# --- Section de Tests --- 
terminal = Terminal()

"""
print("\n--- Liste des abonnés ---")
for ab in terminal.abbonnes:
    print(f"{ab.nom} {ab.prenom} | Plaque: {ab.plaque_voiture} | Place réservée: {ab.place_reservee}")

print("\n--- Liste des places ---")
for pl in terminal.places:
    print(f"{pl.etage}{pl.zone}{pl.numero} | Type: {pl.type} | Réservée pour: {pl.plaque_reservee} | Occupée: {pl.est_occupe}")
"""
