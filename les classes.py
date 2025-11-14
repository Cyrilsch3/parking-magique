from datetime import datetime 
# -------------------- Fonctions utilitaires --------------------
def confirmation(question):
    reponse = input(f"{question}  (o/n) : ").strip().lower()
    return reponse in ['o', 'oui', 'y', 'yes']





# -------------------- Class place --------------------
    
class Place():
    def __init__(self, etage, zone, numero, type, plaque = None):
        self.__etage = etage
        self.__zone = zone
        self.__numero = numero 
        self.__type = type 
        self._plaque = plaque 
        self._temp = None
        self.tarif = [15, 2, 2, 1.5, 15] # [minutes gratuites, prix première heure, prix deuxième heure, prix de 3 a 10 h, prix max]
        
        
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

    # --- SI Abonnement ---
        if self.plaque in plaque_abonnement:
            plaque = self.plaque
            # On libère quand même la place
            self.temp = None
            self.plaque = None
            return f"Le client avec la plaque {plaque} a un abonnement"

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
  
         
# -------------------- les classes pour les abonnés --------------------

class Abonnement:
    nb = 0 # compteur de tous les abonnements
    def __init__(self, nom, prenom, plaque, duree, date_debut=None):
        self.id = str(Abonnement.nb).zfill(5) # ID sur 5 chiffre avec 0 non sigificatifs 
        Abonnement.nb += 1 #Ajoute un Abonné ()
        
        self.nom = nom
        self.prenom = prenom 
        self.plaque = plaque 
        self.duree = duree  # durée en mois
        self.date_debut = date_debut or datetime.today().date()  # date actuelle par défaut
        

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

