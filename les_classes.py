from datetime import datetime 
import random #Pour définir un id d'abonnement client


# -------------------- Fonctions utilitaires --------------------
def confirmation(question):
    reponse = input(f"{question}  (o/n) : ").strip().lower()
    return reponse in ['o', 'oui', 'y', 'yes']

class Parking:
    _places = []
    abonnements = []
    
    @property
    def places(cls):
        return cls._places[:]

    @places.setter
    def places(cls, value):
        if not isinstance(value, list):
            raise TypeError("Parking.places doit être une liste.")

        for elem in value:
            if not isinstance(elem, Place):
                raise TypeError("Parking.places ne peut contenir que des objets de type Place.")
            
        cls._places = value

    @classmethod
    def places_occupees(cls):
        return [p for p in cls.places if p.plaque is not None]

    @classmethod
    def places_abonnes(cls):
        result = []
        for ab in cls.abonnements:
            if ab.place is not None:
                # Trouver l'objet Place correspondant à l'ID de l'abonnement
                place_obj = next((p for p in cls.places if p.id == ab.place), None)
                if place_obj:
                    result.append((place_obj, ab.plaque))
        return result
    
    @classmethod
    def places_libres(cls):
        # Récupérer les places occupées et celles réservées aux abonnés
        places_occupees_ids = [p.id for p in cls.places_occupees()]
        places_abonnes_ids = [p.id for p, _ in cls.places_abonnes()]
    
        # Retourner toutes les autres places
        return [p for p in cls.places if p.id not in places_occupees_ids and p.id not in places_abonnes_ids]

    
    @classmethod
    def calcul_prix(cls, place, mtn=None):
        if mtn is None:
            mtn = datetime.now()
        duree = mtn - place.temp
        minutes = int(duree.total_seconds() / 60)
        return Tarif.calcul(minutes)

    @classmethod
    def occuper_place(cls, place, plaque):
        if place.plaque is not None:
            return f"Place déjà occupée par {place.plaque}"
        place.plaque = plaque
        place.temp = datetime.now()
        return f"Place {place.id} occupée par {plaque}"

    @classmethod
    def liberer_place(cls, place):
        if place.temp is None:
            return "La place était déjà libre"
        duree = datetime.now() - place.temp
        minutes = int(duree.total_seconds() / 60)
        prix = Tarif.calcul(minutes)
        place.plaque = None
        place.temp = None
        return f"Place {place.id} libérée — prix : {prix}€"

    
# ---- Classe Tarif ----

class Tarif:
    _gratuit_minutes = 15
    _prix_premiere_heure = 2
    _prix_deuxieme_heure = 2
    _prix_heures_suivantes = 1.5
    _prix_max_10h = 15
    _prix_abonnement_simple = 70
    _prix_abonnement_reserver = 90

    @property   
    def gratuit_minutes(cls):
        return cls._gratuit_minutes
    
    @gratuit_minutes.setter
    def gratuit_minutes(cls, value):
        cls._gratuit_minutes = cls._verif(value)
    @property
    def prix_premiere_heure(cls):
        return cls._prix_premiere_heure
    @property
    def prix_deuxieme_heure(cls):
        return cls._prix_deuxieme_heure

    @prix_deuxieme_heure.setter
    def prix_deuxieme_heure(cls, value):
        cls._prix_deuxieme_heure = cls._verif(value)

    @property
    def prix_heures_suivantes(cls):
        return cls._prix_heures_suivantes

    @prix_heures_suivantes.setter
    def prix_heures_suivantes(cls, value):
        cls._prix_heures_suivantes = cls._verif(value)

    @property
    def prix_max_10h(cls):
        return cls._prix_max_10h

    @prix_max_10h.setter
    def prix_max_10h(cls, value):
        cls._prix_max_10h = cls._verif(value)

    @property
    def prix_abonnement_simple(cls):
        return cls._prix_abonnement_simple
    @prix_abonnement_simple.setter
    def prix_abonnement_simple(cls, value):
        cls._prix_abonnement_simple = cls._verif(value)

    @property
    def prix_abonnement_reserver(cls):
        return cls._prix_abonnement_reserver

    @prix_abonnement_reserver.setter
    def prix_abonnement_reserver(cls, value):
        cls._prix_abonnement_reserver = cls._verif(value)
    

    @classmethod
    def calcul(cls, minutes):
        if minutes < cls.gratuit_minutes:
            return 0
        elif minutes <= 60:
            return cls.prix_premiere_heure
        elif minutes <= 120:
            return cls.prix_premiere_heure + cls.prix_deuxieme_heure
        elif minutes <= 600:
            extra = minutes - 120
            heures = extra // 60
            if extra % 60 > 0:
                heures += 1
            return cls.prix_premiere_heure + cls.prix_deuxieme_heure + heures * cls.prix_heures_suivantes
        else:
            return cls.prix_max_10h

# -------------------- Class place --------------------

    
class Place():
    
    def __init__(self, etage, zone, numero, type, plaque = None):
        self.__etage = etage
        self.__zone = zone
        self.__numero = numero 
        self.__type = type 
        self._plaque = plaque 
        self._temp = None
        Parking.places.append(self)
    # ---------- ID ----------
    @property
    def id(self):
        #ID calculé dynamiquement à partir de l'étage, la zone et le numéro
        return f"{self.__etage}{self.__zone}{self.__numero}"
        
    # ---------- ETAGE ----------
    @property
    def etage(self):
        return self.__etage

    @etage.setter
    def etage(self, value):
        if confirmation(f"Voulez-vous vraiment changer l'étage de {self.__etage} à {value} ?"):
            self.__etage = value
            #print(f"Étage changé en {value}")
            return value
        else:
            #print("Rien n'a changé")
            return False

    # ---------- ZONE ----------
    @property
    def zone(self):
        return self.__zone

    @zone.setter
    def zone(self, value):
        if confirmation(f"Voulez-vous vraiment changer la zone de {self.__zone} à {value} ?"):
            self.__zone = value
            #print(f"Zone changée en {value}")
            return value #Renvoie la nouvelle zone 
        else:
            #print("Rien n'a changé")
            return False

    # ---------- NUMERO ----------
    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, value):
        if confirmation(f"Voulez-vous vraiment changer le numéro de {self.__numero} à {value} ?"):
            self.__numero = value
            #print(f"Numéro changé en {value}")
            return value #renvoiela nouvelle value
        else:
            False

    # ---------- TYPE ----------
    TYPES_VALIDES = ["Compacte", "Large", "PMR", "Électrique"]

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if value not in Place.TYPES_VALIDES:
            raise ValueError(f"Type '{value}' invalide. Types autorisés : {Place.TYPES_VALIDES}")
        
        if confirmation(f"Voulez-vous vraiment changer le type de {self.__type} à {value} ?"):
            self.__type = value  
            #print(f"Type changé en {value}")
            return value #type changer en value
        else:
            #print("Rien n'a changé")
            return False

    # ---------- PLAQUE ----------
    @property
    def plaque(self):
        return self._plaque
    
    @plaque.setter
    def plaque(self, value):
        if self._plaque is None:
            self._plaque = value
        else :
            False #Place non libre
        
    # ---------- TEMP ----------
    @property
    def temp(self):
        return self._temp
    
    @temp.setter
    def temp(self,value):
        self._temp = value
        
        

    def __str__(self):
        if self.plaque == None:
            return f"{self.etage}{self.zone}:{self.numero} - {self.type}" #Ne return pas de plaque si libre
        else:
            return f"{self.etage}{self.zone}:{self.numero} - {self.type} - {self.plaque}"#Return une plaque si pas libre
  
  
        
         
# -------------------- les classes pour les abonnés --------------------

class Abonnement:
    def __init__(self, nom, prenom, plaque, duree, date_debut = None, place_attribuée = None):
        self.id = str(len(Parking.abonnements)).zfill(5) # ID sur 5 chiffre avec 0 non sigificatifs 
        
        self.nom = nom
        self.prenom = prenom 
        self.plaque = plaque 
        self.duree = duree  # durée en mois
        self.date_debut = date_debut or datetime.today().date()  # date actuelle par défaut
        self.place = place_attribuée
        
        # Ajouter l'instance à la liste de classe
        Parking.abonnements.append(self)
            # --- propriétés en lecture (id immuable) ---
    @property
    def id(self):
        return self._id
    
    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("nom invalide")
        self._nom = value.strip().title()

    @property
    def prenom(self):
        return self._prenom


    @prenom.setter
    def prenom(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("prenom invalide")
        self._prenom = value.strip().title()

    @property
    def plaque(self):
        return self._plaque

    @plaque.setter
    def plaque(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("plaque invalide")
        self._plaque = value.strip().upper()

    @property
    def duree(self):
        return self._duree

    @duree.setter
    def duree(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("duree doit être un entier positif (mois)")
        self._duree = value


    @property
    def date_debut(self):
        return self._date_debut


    @date_debut.setter
    def date_debut(self, value):
        if isinstance(value, datetime):
            value = value.date()
        if not isinstance(value, datetime):
            raise TypeError("date_debut doit être une date")
        self._date_debut = value

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        self._place = value
        
    def date_fin(self):
        month = self._date_debut.month - 1 + self._duree
        year = self._date_debut.year + month // 12
        month = month % 12 + 1
        day = min(self._date_debut.day, [31,
                                        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                                        31,30,31,30,31,31,30,31,30,31][month-1])
        return datetime(year, month, day).date()

    def __str__(self):
        return self.date_fin()


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
                     type = i[3],
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
            place_attribuée = i[5]
        )
        
          
#ajout_des_donnees_du_client()
       
#---- test----

#sofiane
    
#for i in Parking.places_libres() :
#    print(i.id)

# for place, plaque in Parking.places_abonnes():
#     print(f"Place : {place.id} — Réservée pour la plaque : {plaque}")

