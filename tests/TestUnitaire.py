import unittest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, date, timedelta
from les_classes import Place, Tarif, Abonnement, Parking

class TestParkingSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Parking.set_places([])  # Vide le parking
        Parking.set_abonnements([])  # Vide les abonnements
    
        cls.place1 = Place(0, "A", "01", "Compacte")
        cls.place2 = Place(0, "A", "02", "Compacte")
        cls.place3 = Place(0, "A", "03", "Compacte")
        cls.place4 = Place(0, "A", "04", "Compacte")

        
        cls.abo1 = Abonnement( #création abonnement sans place attribuée
            "cyril", "Schweicher", "BE-468-CU",
            duree=6,
            date_debut=date.today(),
            place_attribuee=None
        )
        cls.abo2 = Abonnement( #création abonnement avec place attribuée
            "Edouard", "Paul", "BE-676-GE",
            duree=12,
            date_debut=date.today(),
            place_attribuee=cls.place3.id
        )

    def test_occuper_place_libre(self):
        # Pré :
        #     - La place self.place2 est libre (plaque = None, temp = None)
        # Post :
        #     - La place est occupée (plaque = "AA-123-BB")
        #     - Une date est enregistrée dans temp
        Parking.occuper_place(self.place2.id, "AA-123-BB")  # appel la fonction à tester
        self.assertEqual(self.place2.plaque, "AA-123-BB")   # vérifie que la plaque est entrée
        self.assertIsInstance(self.place2.temp, datetime)    # vérifie qu'une datetime est entrée 

    def test_liberer_place(self):
        # Pré :
        #     - La place self.place1 est occupée (plaque non None, temp non None)
        # Post :
        #     - La place est libérée (plaque = None, temp = None)
        #     - Le message retourné indique que la place a été libérée
        self.place1.plaque = "ZZ-999-YY"  # rempli la plaque 
        self.place1.temp = datetime.now()  # rempli le temps
        res = Parking.liberer_place(self.place1.id)  # appel la fonction à tester 
        self.assertTrue(res[0])  # vérifie que le changement est fait avec True
        self.assertIsNone(self.place1.plaque)  # vérifie que la plaque est None
        self.assertIsNone(self.place1.temp)    # vérifie que le temps est None
    
    def test_allonger_abonnement_valide(self):
        # Pré :
        #     - L’abonnement self.abo1 existe
        #     - Durée initiale = 6 mois (ligne 17)
        # Post :
        #     - La durée est augmentée de 3 mois
        #     - Le message indique une prolongation
        res = Parking.allonger_abonnement(self.abo1.id, 3)
        self.assertTrue(res[0])
        self.assertEqual(self.abo1.duree, 9)
        self.assertIn("prolongé", res[1])

    
    def test_modifier_abonnement_plaque(self):
        # Pré :
        #     - L’abonnement self.abo1 a une plaque AA-111-AA
        # Post :
        #     - La plaque est modifiée
        res = Parking.modifier_abonnement(self.abo1.id, plaque="NV-212-PL")
        self.assertIn("NV-212-PL", res)
        self.assertEqual(self.abo1.plaque, "NV-212-PL") #vérifie la maj de la nouvelle plaque

    def test_modifier_abonnement_place(self):
        # Pré :
        #     - L'abonnement abo1 existe
        #     - L’abonnement self.abo1 n’a pas de place réservée
        # Post :
        #     - Une place est attribuée
        #     - Un message indique une différence de prix
        res = Parking.modifier_abonnement(self.abo1.id, place_id=self.place4.id) #on ajoute une place dans l'abonnement
        self.assertEqual(self.abo1.place, self.place4.id) #On vérif que la place qu'on a attribué à l'abo lui est bien réservé
        self.assertIn("Différence de prix", res)
    
    def test_modifier_abonnement_inexistant(self):
        # Pré :
        #     - Aucun abonnement avec cet ID
        # Post :
        #     - Un message d’erreur est retourné
        res = Parking.modifier_abonnement("99999", plaque="YU-868-MM")
        self.assertIn("Aucun abonnement trouvé", res)

class TestPlace(unittest.TestCase):
    def setUp(self):
        Parking.set_places([])
    
    def test_creation_place_id(self):
        # Pré :
        #     - Création d'une place avec étage, zone et numéro
        # Post :
        #     - L'ID est correctement généré (etage + zone + numero)
        place = Place(1, "B", "04", "Large")
        self.assertEqual(place.id, "1B04")
    
    def test_place_occupee_interdite(self):
        # Pré :
        #     - Une place est déjà occupée par une plaque
        # Post :
        #     - Une erreur est levée si on tente de changer la plaque
        place = Place(0, "A", "01", "Compacte")
        place.plaque = "AA-123-BB"
        with self.assertRaises(ValueError):
            place.plaque = "CC-456-DD"
    
    def test_type_place_invalide(self):
        # Pré :
        #     - Une place existe avec un type valide
        # Post :
        #     - Une erreur est levée si le type est invalide
        place = Place(0, "A", "02", "Compacte")
        with self.assertRaises(ValueError):
            place.type_place = "Volante"

class TestTarif(unittest.TestCase):
    def test_gratuit(self):
        # Pré :
        #     - Une durée inférieure au temps gratuit
        # Post :
        #     - Le prix retourné est 0€
        self.assertEqual(Tarif.calcul(10), 0)

    def test_premiere_heure(self):
        # Pré :
        #     - Une durée de 60 minutes
        # Post :
        #     - Le prix correspond à la première heure
        self.assertEqual(Tarif.calcul(60), Tarif.prix_premiere_heure())
    
    def test_deux_heures(self):
        # Pré :
        #     - Une durée de 120 minutes
        # Post :
        #     - Le prix est la somme des deux premières heures
        expected = Tarif.prix_premiere_heure() + Tarif.prix_deuxieme_heure()
        self.assertEqual(Tarif.calcul(120), expected)

    def test_heures_supplementaires(self):
        # Pré :
        #     - Une durée supérieure à 2 heures
        # Post :
        #     - Le prix augmente avec les heures supplémentaires
        prix = Tarif.calcul(180) #car 3h
        self.assertGreater(prix, Tarif.prix_premiere_heure())

    def test_prix_max(self):
        # Pré :
        #     - Une durée supérieure à 10 heures
        # Post :
        #     - Le prix maximal est appliqué
        self.assertEqual(Tarif.calcul(700), Tarif.prix_max_10h())

class TestAbonnement(unittest.TestCase):
    def setUp(self):
        Parking.set_abonnements([])
    
    def test_creation_abonnement(self):
        # Pré :
        #     - Création d'un abonnement valide
        # Post :
        #     - Les attributs sont correctement initialisés
        abo = Abonnement(
            "Dupont", "Alice", "AB-123-CD",
            duree=6,
            date_debut=date.today(),
            place_attribuee=None
        )
        self.assertEqual(abo.nom, "Dupont")
        self.assertEqual(abo.duree, 6)
    
    def test_date_fin(self):
        # Pré :
        #     - Abonnement avec une durée définie
        # Post :
        #     - La date de fin est postérieure à la date de début
        abo = Abonnement(
            "Martin", "Paul", "ZZ-999-ZZ",
            duree=3,
            date_debut=date.today(),
            place_attribuee=None
        )
        self.assertGreater(abo.date_fin(), abo.date_debut)

if __name__ == "__main__":
    unittest.main()