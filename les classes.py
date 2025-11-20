from datetime import datetime 
# -------------------- Fonctions utilitaires --------------------
def confirmation(question):
    reponse = input(f"{question}  (o/n) : ").strip().lower()
    return reponse in ['o', 'oui', 'y', 'yes']






# -------------------- Class place --------------------
    
class Place():
    les_places=[]
    def __init__(self, etage, zone, numero, type, plaque = None):
        self.__etage = etage
        self.__zone = zone
        self.__numero = numero 
        self.__type = type 
        self._plaque = plaque 
        self._temp = None
        self.tarif = [15, 2, 2, 1.5, 15] # [minutes gratuites, prix première heure, prix deuxième heure, prix de 3 a 10 h, prix max]
    
        # Ajouter l'instance à la liste de classe
        Place.les_places.append(self)
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
            print(f"Étage changé en {value}")
        else:
            print("Rien n'a changé")

    # ---------- ZONE ----------
    @property
    def zone(self):
        return self.__zone

    @zone.setter
    def zone(self, value):
        if confirmation(f"Voulez-vous vraiment changer la zone de {self.__zone} à {value} ?"):
            self.__zone = value
            print(f"Zone changée en {value}")
        else:
            print("Rien n'a changé")

    # ---------- NUMERO ----------
    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, value):
        if confirmation(f"Voulez-vous vraiment changer le numéro de {self.__numero} à {value} ?"):
            self.__numero = value
            print(f"Numéro changé en {value}")
        else:
            print("Rien n'a changé")

    # ---------- TYPE ----------
    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if confirmation(f"Voulez-vous vraiment changer le type de {self.__type} à {value} ?"):
            self.__type = value
            print(f"Type changé en {value}")
        else:
            print("Rien n'a changé")
            
    # ---------- PLAQUE ----------
    @property
    def plaque(self):
        return self._plaque
    
    @plaque.setter
    def plaque(self, value):
        if self._plaque is None:
            self._plaque = value
        else :
            print("Place non libre")
        
    # ---------- TEMP ----------
    @property
    def temp(self):
        return self._temp
    
    @temp.setter
    def temp(self,value):
        self._temp = value
        
    # ---------- OCCUPER UNE PLACE ----------
    def occuper_place(self, nouvelle_plaque):
        if self.plaque != None:
            print(f"Place déja occupée par {self.plaque}")
            return f"Place déja occupée par {self.plaque}"
        self.plaque = nouvelle_plaque
        self.temp = datetime.now()
        
        
    # ---------- libérer la place et calculer le prix ----------
    def liberer_place(self, mtn=None):
        if mtn is None:
            mtn = datetime.now()

    # --- SI Place vide ---
        if self.temp is None:
            return "Étrange, la place était libre !!!!"

    # --- TEST Abonnement ---
        aujourdhui = datetime.today().date()
        abonnement_actif = False
        
        for i in Abonnement.les_abonnés:
            if self.plaque == i.plaque:
                if i.date_fin() >= aujourdhui:
                    abonnement_actif = True
                    break  # on a trouvé un abonnement actif

        if abonnement_actif:
            # Libère la place quand même
            plaque = self.plaque
            self.temp = None
            self.plaque = None
            return f"Le client avec la plaque {plaque} a un abonnement actif jusqu'au {date_fin}"

    # --- SI pas Abonnement ---
    
    # Calcul Durée en minutes
        duree = mtn - self.temp
        minutes = int(duree.total_seconds() / 60)

    # Calcul du prix 
        if minutes < self.tarif[0]:
            prix = 0

        elif minutes <= 60:
            prix = self.tarif[1]

        elif minutes <= 120:
          prix = self.tarif[1] + self.tarif[2]

        elif minutes <= 600:
            extra = minutes - 120
            heures_supp = extra // 60 
            if extra % 60 > 0:  # évite de payer plus si c'est une heure pile 
                heures_supp += 1
            prix = self.tarif[1] + self.tarif[2] + heures_supp * self.tarif[3]

        else:
            prix = self.tarif[4]

        prix = round(prix, 2)

    # On libère la place
        self.temp = None
        self.plaque = None
        
        return f"prix: {prix}"
    
        

    def __str__(self):
        if self.plaque == None:
            return f"Dans le parking la place  {self.etage}{self.zone}:{self.numero} de type {self.type} est libre"
        else:
            return f"Dans le parking la place  {self.etage}{self.zone}:{self.numero} de type {self.type} est occupée par la voiture {self.plaque}"
  
  
    
    @classmethod
    def places_abonnes(cls):
        #Retourne les places réservées par les abonnés.
        abonnements_places = [ab.place for ab in Abonnement.les_abonnés if ab.place is not None]
        return [p for p in cls.les_places if p.id in abonnements_places]

    @classmethod
    def places_occupees(cls):
        #Retourne les places actuellement occupées par une voiture.
        return [p for p in cls.les_places if p.plaque is not None]
    
    @classmethod
    def lister_libres(cls):
        #Retourne les places libres (ni occupées, ni réservées par un abonnement).
        occupees = cls.places_occupees()
        abonnes = cls.places_abonnes()
        return [p for p in cls.les_places if p not in occupees and p not in abonnes]
            
         
# -------------------- les classes pour les abonnés --------------------

class Abonnement:
    les_abonnés = []
    def __init__(self, nom, prenom, plaque, duree, date_debut = None, place_attribuée = None):
        self.id = str(len(Abonnement.les_abonnés)).zfill(5) # ID sur 5 chiffre avec 0 non sigificatifs 
        
        self.nom = nom
        self.prenom = prenom 
        self.plaque = plaque 
        self.duree = duree  # durée en mois
        self.date_debut = date_debut or datetime.today().date()  # date actuelle par défaut
        self.place = place_attribuée
        
        # Ajouter l'instance à la liste de classe
        Abonnement.les_abonnés.append(self)
        

    def date_fin(self):
        # calcul de la date de fin en ajoutant les mois
        month = self.date_debut.month - 1 + self.duree
        year = self.date_debut.year + month // 12
        month = month % 12 + 1
        day = min(self.date_debut.day, [31,
                                        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                                        31,30,31,30,31,31,30,31,30,31][month-1])
        return datetime(year, month, day).date()
    
    
    def __str__(self):
        return f"L'abonnement de {self.nom} {self.prenom} se termine le {self.date_fin()}"


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
        
        
        
ajout_des_donnees_du_client()
       
#---- test----

# for i in Abonnement.les_abonnés:
#     print(i.id, i.nom,i.prenom,i.plaque,i.duree,i.date_debut,i.place)
# for i in Place.les_places:
#     print(i.etage,
#         i.zone,
#         i.numero,
#         i.type,
#         i.plaque,
#         i.temp)

    
for i in Place.places_abonnes() :
    print(i.id)