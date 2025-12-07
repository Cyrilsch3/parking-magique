from datetime import datetime 
import random #Pour définir un id d'abonnement client
import json
import os
from dateutil.relativedelta import relativedelta

# -------------------- Fonctions utilitaires --------------------
def confirmation(question):
    reponse = input(f"{question}  (o/n) : ").strip().lower()
    return reponse in ['o', 'oui', 'y', 'yes']

class Parking:
    _places = []
    _abonnements = []

    # ----- PLACES -----
    @classmethod
    def places(cls):
        return cls._places[:]

    @classmethod
    def set_places(cls, value):
        if not isinstance(value, list):
            raise TypeError("Parking.places doit être une liste.")
        for elem in value:
            if not isinstance(elem, Place):
                raise TypeError("Parking.places ne peut contenir que des objets de type Place.")
        cls._places = value

    # ----- ABONNEMENTS -----
    @classmethod
    def abonnements(cls):
        return cls._abonnements[:]

    @classmethod
    def set_abonnements(cls, value):
        if not isinstance(value, list):
            raise TypeError("Parking.abonnements doit être une liste.")
        for elem in value:
            if not isinstance(elem, Abonnement):
                raise TypeError("Parking.abonnements ne peut contenir que des objets de type Abonnement.")
        cls._abonnements = value

    # ----- MÉTHODES EXISTANTES -----
    @classmethod
    def places_occupees(cls):
        return [p for p in cls.places() if p.plaque is not None]

    @classmethod

    def places_abonnes(cls):
        #Retourne la liste des places réservées avec plaque, uniquement pour les abonnements encore valides
        result = []
        for ab in cls.abonnements():
            if ab.place is not None and ab.date_fin() > date.today():
                place_obj = next((p for p in cls.places() if p.id.upper() == ab.place.upper()), None)
                if place_obj:
                    result.append((place_obj, ab.plaque))
        return result


    
    @classmethod
    def places_libres(cls):
        places_occupees_ids = [p.id for p in cls.places_occupees()]
        places_abonnes_ids = [p.id for p, _ in cls.places_abonnes()]
        return [p for p in cls.places() if p.id not in places_occupees_ids and p.id not in places_abonnes_ids]
    
    @classmethod
    def liste_place(cls):
        #Retourne la liste complète des places du parking sous forme lisible.
        return [str(place) for place in cls.places()]

    @classmethod
    def lister_plaques_abo(cls):
        return [ab.plaque for ab in cls.abonnements() if ab.date_fin() > date.today()]

    @classmethod
    def retrouver_id(cls, plaque):  
        plaque = plaque.strip().upper()
        abo = next((a for a in cls.abonnements() if a.plaque == plaque), None)
        return abo.id if abo else None

    @classmethod
    def allonger_abonnement(cls, id, nb_mois):
        abo = next((a for a in cls.abonnements() if a.id == id), None)
        if abo is None:
            return [False, f"Aucun abonnement trouvé avec l'ID {id}"]

        if not isinstance(nb_mois, int) or nb_mois <= 0:
            return [False, "La durée à ajouter doit être un entier positif"]
        
        abo.duree += nb_mois
        date_fin = abo.date_fin()  # date de fin après prolongation

        # Calcul du prix mensuel selon si place attribuée ou non
        if abo.place:
            prix_mensuel = Tarif.prix_abonnement_reserver()
        else:
            prix_mensuel = Tarif.prix_abonnement_simple()

        prix = prix_mensuel * nb_mois

        message = f"Abonnement {id} prolongé de {nb_mois} mois. Date de fin : {date_fin}, Prix à payer : {prix:.2f}€"
        return [True, message]
    
    @classmethod
    def calcul_prix(cls, place, mtn=None):
        if mtn is None:
            mtn = datetime.now()
        duree = mtn - place.temp
        minutes = int(duree.total_seconds() / 60)
        return Tarif.calcul(minutes)

    @classmethod
    def occuper_place(cls, place_id, plaque):
        try: 
            place = next((p for p in cls.places() if p.id == place_id.upper()), None)
        except ValueError: 
            return "Place non valide"
        if place is None:
            return "Place inexistante"
        plaque = plaque.strip().upper()

        # Vérifier si cette plaque a déjà une place réservée
        abo_reserve = next((ab for ab in cls.abonnements() if ab.plaque == plaque and ab.place is not None), None)
        if abo_reserve and abo_reserve.place != place.id:
            return f"Vous avez une place réservée : {abo_reserve.place}. Merci d'utiliser votre place."

        # Vérification si la place est déjà occupée physiquement
        if place.plaque is not None:
            return f"Place déjà occupée par {place.plaque}"

        # Vérification des places réservées par un autre abonné
        abo_autre = next((ab for ab in cls.abonnements() if ab.place == place.id), None)
        if abo_autre and abo_autre.plaque != plaque:
            return f"La place {place.id} est réservée pour l'abonné {abo_autre.plaque}"

        # Attribution
        place.plaque = plaque
        place.temp = datetime.now()
        return f"Place {place.id} occupée par {plaque}"


    @classmethod
    def liberer_place(cls, place_id):
        try: 
            place = next((p for p in Parking.places() if p.id == place_id.upper()), None)
        except ValueError: 
            return "place non valide "
        if place.temp is None:
            return [False,"La place était déjà libre"]
        
        if place.plaque in cls.lister_plaques_abo():
            place.plaque = None
            place.temp = None
            return [True, f"Place {place.id} libérée — Abonné : 0€"]
        duree = datetime.now() - place.temp
        minutes = int(duree.total_seconds() / 60)
        prix = Tarif.calcul(minutes)
        place.plaque = None
        place.temp = None
        return [True,f"Place {place.id} libérée — prix : {prix}€"]
    
    @classmethod
    def modifier_abonnement(cls, id, plaque=None, place_id=None):
        abo = next((a for a in cls.abonnements() if a.id == id), None)
        if abo is None:
            return f"Aucun abonnement trouvé avec l'ID {id}"

        # On mémorise la place avant modification
        place_avant = abo.place

        # Met à jour la plaque si fournie
        if plaque:
            abo.plaque = plaque.upper()
            # Ancien comportement : si la place est physiquement attribuée à l'abonné, on met à jour la plaque sur la place
            if abo.place:
                place_obj = next((p for p in cls.places() if p.id == abo.place), None)
                if place_obj and place_obj.plaque == abo.plaque:
                    # Si la place était physiquement occupée par l'ancien abonné, on la met à jour
                    place_obj.plaque = abo.plaque

        # Met à jour la place si fournie
        if place_id:
            nouvelle_place = next((p for p in cls.places() if p.id == place_id.upper()), None)
            if nouvelle_place is None:
                return f"Place {place_id} inexistante"
            # On ne doit pas occuper physiquement la place pour un abonnement (pas de plaque sur la place)
            if nouvelle_place.plaque is not None:
                # Si la place est occupée physiquement, on ne peut pas la réserver
                return f"Place {place_id} déjà occupée par {nouvelle_place.plaque}"
            # Libère l'ancienne place (uniquement si elle n'est pas physiquement occupée)
            if abo.place:
                ancienne_place = next((p for p in cls.places() if p.id == abo.place), None)
                # On ne libère la plaque que si la place était réservée pour l'abo mais pas physiquement occupée
                if ancienne_place and ancienne_place.plaque is None:
                    ancienne_place.plaque = None
            # Attribue la nouvelle place (en tant que réservée, SANS mettre la plaque sur la place)
            abo.place = place_id.upper()
            # Ne pas occuper physiquement la place : on ne met PAS nouvelle_place.plaque = abo.plaque

        # Vérifie si la place est passée de None → non None
        prix_diff = None
        if place_avant is None and abo.place is not None:
            prix_diff = Tarif.prix_abonnement_reserver() - Tarif.prix_abonnement_simple()

        result = f"Abonnement {id} mis à jour : plaque = {abo.plaque}, place = {abo.place}"
        if prix_diff is not None:
            result += f" — Différence de prix pour place réservée : {prix_diff}€"

        return result
    @classmethod
    def save_all(cls):
        now = datetime.now()
        fichier = f"parking_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"

        # Gestion des sauvegardes : ne conserver que les 5 dernières
        # 1. Liste tous les fichiers parking_*.json
        backup_files = [fn for fn in os.listdir('.') if fn.startswith('parking_') and fn.endswith('.json')]
        # 2. Trie par date extraite du nom de fichier
        def extract_date(fn):
            try:
                # Format attendu : parking_YYYY-MM-DD_HH-MM-SS.json
                base = fn.replace('parking_', '').replace('.json', '')
                return datetime.strptime(base, '%Y-%m-%d_%H-%M-%S')
            except Exception:
                return datetime.min
        backup_files.sort(key=extract_date)
        # 3. Supprime les plus anciens pour ne garder que les 5 derniers
        while len(backup_files) >= 5:
            to_remove = backup_files.pop(0)
            try:
                os.remove(to_remove)
            except Exception:
                pass

        data = {
            "places": [
                {
                    "id": p.id,
                    "etage": p.etage,
                    "zone": p.zone,
                    "numero": p.numero,
                    "type_place": p.type_place,
                    "plaque": p.plaque,
                    "temp": p.temp.isoformat() if p.temp else None
                }
                for p in cls.places()
            ],
            "abonnements": [
                {
                    "id": a.id,
                    "nom": a.nom,
                    "prenom": a.prenom,
                    "plaque": a.plaque,
                    "duree": a.duree,
                    "date_debut": a.date_debut.isoformat(),
                    "place": a.place
                }
                for a in cls.abonnements()
            ],
            "tarifs": {
                "gratuit_minutes": Tarif.gratuit_minutes(),
                "prix_premiere_heure": Tarif.prix_premiere_heure(),
                "prix_deuxieme_heure": Tarif.prix_deuxieme_heure(),
                "prix_heures_suivantes": Tarif.prix_heures_suivantes(),
                "prix_max_10h": Tarif.prix_max_10h(),
                "prix_abonnement_simple": Tarif.prix_abonnement_simple(),
                "prix_abonnement_reserver": Tarif.prix_abonnement_reserver()
            }
        }

        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return f"Parking sauvegardé dans {fichier}"
        
# ---- Classe Tarif ----

class Tarif:
    _gratuit_minutes = 15
    _prix_premiere_heure = 2
    _prix_deuxieme_heure = 2
    _prix_heures_suivantes = 1.5
    _prix_max_10h = 15
    _prix_abonnement_simple = 70
    _prix_abonnement_reserver = 90

    # ----- GETTERS ET SETTERS DE CLASSE -----
    @classmethod
    def gratuit_minutes(cls):
        return cls._gratuit_minutes

    @classmethod
    def set_gratuit_minutes(cls, value):
        if not isinstance(value, int) or value < 0:
            return [False, "gratuit_minutes doit être un entier >= 0"]

        cls._gratuit_minutes = value
        return [True, f"Valeur mise à jour : gratuit_minutes = {value}"]
        

    @classmethod
    def prix_premiere_heure(cls):
        return cls._prix_premiere_heure

    @classmethod
    def set_prix_premiere_heure(cls, value):
        if not isinstance(value, (int, float)) or value < 0:
            return [False, "prix_premiere_heure doit être un nombre positif"]
        cls._prix_premiere_heure = value
        return [True, f"Valeur mise à jour : prix_premiere_heure = {value}"]

    @classmethod
    def prix_deuxieme_heure(cls):
        return cls._prix_deuxieme_heure

    @classmethod
    def set_prix_deuxieme_heure(cls, value):
        if not isinstance(value, (int, float)) or value < 0:
            return [False, "prix_deuxieme_heure doit être un nombre positif"]
        cls._prix_deuxieme_heure = value
        return [True, f"Valeur mise à jour : prix_deuxieme_heure = {value}"]

    @classmethod
    def prix_heures_suivantes(cls):
        return cls._prix_heures_suivantes

    @classmethod
    def set_prix_heures_suivantes(cls, value):
        if not isinstance(value, (int, float)) or value < 0:
            return [False, "prix_heures_suivantes doit être un nombre positif"]
        cls._prix_heures_suivantes = value
        return [True, f"Valeur mise à jour : prix_heures_suivantes = {value}"]

    @classmethod
    def prix_max_10h(cls):
        return cls._prix_max_10h

    @classmethod
    def set_prix_max_10h(cls, value):
        if not isinstance(value, (int, float)) or value < 0:
            return [False, "prix_max_10h doit être un nombre positif"]
        cls._prix_max_10h = value
        return [True, f"Valeur mise à jour : prix_max_10h = {value}"]

    @classmethod
    def prix_abonnement_simple(cls):
        return cls._prix_abonnement_simple

    @classmethod
    def set_prix_abonnement_simple(cls, value):
        if not isinstance(value, (int, float)) or value < 0:
            return [False, "prix_abonnement_simple doit être un nombre positif"]
        cls._prix_abonnement_simple = value
        return [True, f"Valeur mise à jour : prix_abonnement_simple = {value}"]

    @classmethod
    def prix_abonnement_reserver(cls):
        return cls._prix_abonnement_reserver

    @classmethod
    def set_prix_abonnement_reserver(cls, value):
        if not isinstance(value, (int, float)) or value < 0:
            return [False, "prix_abonnement_reserver doit être un nombre positif"]
        cls._prix_abonnement_reserver = value
        return [True, f"Valeur mise à jour : prix_abonnement_reserver = {value}"]

    # ----- CALCUL DU PRIX -----
    @classmethod
    def calcul(cls, minutes):
        if minutes < cls.gratuit_minutes():
            return 0
        elif minutes <= 60:
            return cls.prix_premiere_heure()
        elif minutes <= 120:
            return cls.prix_premiere_heure() + cls.prix_deuxieme_heure()
        elif minutes <= 600:  # jusqu'à 10h
            extra = minutes - 120
            heures = extra // 60
            if extra % 60 > 0:
                heures += 1
            return cls.prix_premiere_heure() + cls.prix_deuxieme_heure() + heures * cls.prix_heures_suivantes()
        else:
            return cls.prix_max_10h()
# -------------------- Class place --------------------
class Place:
    TYPES_VALIDES = ["Compacte", "Large", "PMR", "Électrique"]

    def __init__(self, etage, zone, numero, type_place, plaque=None):
        self.__etage = etage
        self.__zone = zone
        self.__numero = numero
        self.__type_place = type_place
        self._plaque = plaque
        self._temp = None
        # Ajouter la place au parking via la liste directe ou via un setter si utilisé
        Parking._places.append(self)

    # ---------- ID ----------
    @property
    def id(self):
        return f"{self.__etage}{self.__zone}{self.__numero}"

    # ---------- ETAGE ----------
    @property
    def etage(self):
        return self.__etage

    @etage.setter
    def etage(self, value):
        if confirmation(f"Voulez-vous vraiment changer l'étage de {self.__etage} à {value} ?"):
            self.__etage = value
        else:
            return False

    # ---------- ZONE ----------
    @property
    def zone(self):
        return self.__zone

    @zone.setter
    def zone(self, value):
        if confirmation(f"Voulez-vous vraiment changer la zone de {self.__zone} à {value} ?"):
            self.__zone = value
        else:
            return False

    # ---------- NUMERO ----------
    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, value):
        if confirmation(f"Voulez-vous vraiment changer le numéro de {self.__numero} à {value} ?"):
            self.__numero = value
        else:
            return False

    # ---------- TYPE PLACE ----------
    @property
    def type_place(self):
        return self.__type_place

    @type_place.setter
    def type_place(self, value):
        if value not in Place.TYPES_VALIDES:
            raise ValueError(f"Type '{value}' invalide. Types autorisés : {Place.TYPES_VALIDES}")
        if confirmation(f"Voulez-vous vraiment changer le type de {self.__type_place} à {value} ?"):
            self.__type_place = value
        else:
            return False

    # ---------- PLAQUE ----------
    @property
    def plaque(self):
        return self._plaque

    @plaque.setter
    def plaque(self, value):
        if value is not None and self._plaque is not None:
            raise ValueError("Place déjà occupée")
        self._plaque = value

    # ---------- TEMP ----------
    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, value):
        self._temp = value

    # ---------- STR ----------
    def __str__(self):
        if self._plaque is None:
            return f"{self.__etage}{self.__zone}:{self.__numero} - {self.__type_place}"
        else:
            return f"{self.__etage}{self.__zone}:{self.__numero} - {self.__type_place} - {self._plaque}"
    
         
# -------------------- les classes pour les abonnés --------------------
from datetime import datetime, date

class Abonnement:
    def __init__(self, nom, prenom, plaque, duree, date_debut=None, place_attribuee=None):
        # ID unique basé sur le nombre d'abonnements existants
        self._id = str(len(Parking.abonnements())).zfill(5)
        
        # Attribution des autres propriétés
        self._nom = nom
        self._prenom = prenom
        self._plaque = plaque
        self._duree = duree  # durée en mois
        self._date_debut = date_debut or datetime.today().date()
        self._place = place_attribuee
        
        # Ajouter l'abonnement à la liste du parking
        Parking._abonnements.append(self)
    
    # ---------- ID ----------
    @property
    def id(self):
        return self._id

    # ---------- NOM ----------
    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Nom invalide")
        self._nom = value.strip().title()

    # ---------- PRENOM ----------
    @property
    def prenom(self):
        return self._prenom
    
    @prenom.setter
    def prenom(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Prénom invalide")
        self._prenom = value.strip().title()

    # ---------- PLAQUE ----------
    @property
    def plaque(self):
        return self._plaque
    
    @plaque.setter
    def plaque(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Plaque invalide")
        self._plaque = value.strip().upper()

    # ---------- DUREE ----------
    @property
    def duree(self):
        return self._duree
    
    @duree.setter
    def duree(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Durée doit être un entier positif (mois)")
        self._duree = value

    # ---------- DATE DEBUT ----------
    @property
    def date_debut(self):
        return self._date_debut
    
    @date_debut.setter
    def date_debut(self, value):
        if isinstance(value, datetime):
            value = value.date()
        if not isinstance(value, date):
            raise TypeError("date_debut doit être une date")
        self._date_debut = value
    # ---------- PLACE ATTRIBUEE ----------
    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value):
        self._place = value  # peut être None ou un ID de place

    # ---------- CALCUL DATE FIN ----------
    def date_fin(self):
        return self._date_debut + relativedelta(months=self._duree)

    # ---------- STR ----------
    def __str__(self):
        return str(self.date_fin())
    


def ajout_des_donnees_du_client():
    # --------- Liste des places du parking donnée par le client ---------
    places_tableau = [
        [-1, 'A', '01', 'Compacte'],
        [-1, 'A', '02', 'Compacte'],
        [-1, 'A', '03', 'Compacte'],
        [-1, 'A', '04', 'Compacte'],
        [-1, 'B', '01', 'Compacte'],
        [-1, 'B', '02', 'Compacte'],
        [-1, 'B', '03', 'Compacte'],
        [-1, 'B', '04', 'Compacte'],
        [-1, 'C', '01', 'Large'],
        [-1, 'C', '02', 'Large'],
        [-1, 'C', '03', 'Large'],
        [-1, 'C', '04', 'Large'],
        
        [0, 'A', '01', 'Large'],
        [0, 'A', '02', 'Large'],
        [0, 'A', '03', 'Large'],
        [0, 'A', '04', 'Large'],
        [0, 'A', '05', 'PMR'],
        [0, 'A', '06', 'PMR'],
        [0, 'B', '01', 'Électrique'],
        [0, 'B', '02', 'Électrique'],
        [0, 'B', '03', 'Compacte'],
        [0, 'B', '04', 'Compacte'],
        [0, 'C', '01', 'Large'],
        [0, 'C', '02', 'Large'],
        [0, 'C', '03', 'Large'],
        [0, 'C', '04', 'Large'],

        [1, 'A', '01', 'Compacte'],
        [1, 'A', '02', 'Compacte'],
        [1, 'A', '03', 'Compacte'],
        [1, 'A', '04', 'Compacte'],
        [1, 'A', '05', 'PMR'],
        [1, 'B', '01', 'Compacte'],
        [1, 'B', '02', 'Compacte'],
        [1, 'B', '03', 'Compacte'],
        [1, 'B', '04', 'Compacte'],
        [1, 'B', '12', 'Large'],
        [1, 'C', '01', 'Large'],
        [1, 'C', '02', 'Large'],

        [2, 'A', '01', 'Compacte'],
        [2, 'A', '02', 'Compacte'],
        [2, 'A', '03', 'Compacte'],
        [2, 'A', '04', 'Compacte'],
        [2, 'A', '05', 'Compacte'],
        [2, 'B', '01', 'Compacte'],
        [2, 'B', '02', 'Compacte'],
        [2, 'B', '03', 'Compacte'],
        [2, 'B', '04', 'Compacte'],
        [2, 'C', '01', 'Électrique'],
        [2, 'C', '02', 'Électrique'],
        [2, 'C', '03', 'Large'],
        [2, 'C', '04', 'Large'],

        [3, 'A', '01', 'Compacte'],
        [3, 'A', '02', 'Compacte'],
        [3, 'A', '03', 'Compacte'],
        [3, 'A', '04', 'Compacte'],
        [3, 'B', '01', 'Compacte'],
        [3, 'B', '02', 'Compacte'],
        [3, 'B', '03', 'Large'],
        [3, 'B', '04', 'Large'],
        [3, 'C', '01', 'Large'],
        [3, 'C', '02', 'Large'],
        [3, 'C', '03', 'Large'],
        [3, 'C', '04', 'Large']
    ]
    #-------- création des places ------
    for i in places_tableau:
        temp = Place(etage= i[0],
                     zone = i[1],
                     numero = i[2],
                     type_place = i[3],
                     plaque = None)
        
    #----- liste des abonné actuels----
    tb_abonnés = [
        ["Dupuis", "Marie", "AA-452-KM", 12, datetime(2025, 1, 1).date(), "2A05"],   
        ["Bernard", "Luc", "DB-793-QF", 6, datetime(2025, 3, 15).date(), "1B12"],  
        ["Leclerc", "Antoine", "FG-219-LR", 12, datetime(2025, 2, 1).date(), "0A02"],
        ["Martin", "Céline", "JH-887-PN", 3, datetime(2025, 4, 1).date(), None],
        ["Roche", "Damien", "KL-045-TZ", 12, datetime(2025, 1, 10).date(), None],
        ["Morel", "Sophie", "BC-338-JC", 6, datetime(2025, 2, 20).date(), None],
        ["Gonzalez", "Thierry", "EV-612-NV", 3, datetime(2025, 4, 5).date(), None],
        ["Petit", "Hélène", "QW-901-HS", 12, datetime(2025, 3, 1).date(), None]
    ]

    #création des abonnés
    for i in tb_abonnés:
        temp = Abonnement(
            nom = i[0],
            prenom = i[1],
            plaque = i[2],
            duree = i[3],
            date_debut = i[4],
            place_attribuee = i[5]
        )
