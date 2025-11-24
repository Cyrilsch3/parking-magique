# -------------------- Class --------------------

# ---------- class pour les places --------------
class Place:
    def __init__(self,etage, numero):
        self.etage = etage
        self.numero = numero
        self.est_occupe = False
        self.voiture = None
        self.plaque_reservee = None
        
    def occuper(self, voiture):
        if self.plaque_reservee and voiture != self.plaque_reservee:
            print(f"l'étage {self.etage}, Place {self.numero} est reservée pour {self.plaque_reservee} !")
        if not self.est_occupe:
            self.voiture = voiture
            self.est_occupe = True
            print(f"voiture {voiture} garée a l'étage {self.etage}, place {self.numero}")
            return True
        else:
            print(f"L'étage {self.etage}, place {self.numero} est déjà occupée.")

class Abonne:
    list_abonne = []

    def __init__(self, nom, plaque_voiture , place_reservee=None):
        self.nom = nom
        self.plaque_voiture = plaque_voiture
        self.place_reservee = place_reservee
        if place_reservee:
            place_reservee.plaque_reservee = plaque_voiture
        Abonne.list_abonne.append(self)
    