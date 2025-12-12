import unittest
from datetime import datetime, date
from les_classes import Parking, Place, Tarif

class TestParkingSpec(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Parking.set_places([])  # Vide le parking
        Parking.set_abonnements([])  # Vide les abonnements
    
        cls.place1 = Place(0, "A", "01", "Compacte")
        cls.place2 = Place(0, "A", "02", "Compacte")

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

if __name__ == "__main__":
    unittest.main()