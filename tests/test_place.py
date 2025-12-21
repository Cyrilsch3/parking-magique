import unittest
from unittest.mock import patch
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MVP import Place, Abonne

class TestPlace(unittest.TestCase):

    @patch("builtins.input", return_value="ABC-123")
    def test_occuper_place_libre_simule_input(self, mock_input):
        """
        Pré :
            - La place est libre (est_occupe = False)
        Post :
            - La place est occupée par la plaque entrée via l'input
            - est_occupe passe à True
        """
        # Arrange : créer une place libre
        p = Place(-1, 'A', '01', 'Compacte')

        # Pré : la place doit être libre
        self.assertFalse(p.est_occupe)
        self.assertIsNone(p.voiture)

        # Act : simuler l’input de la plaque pour occuper la place
        plaque = input("Entrer la plaque de la voiture : ").strip().upper()
        res = p.occuper(plaque)

        # Post : vérifications
        self.assertTrue(res)                     # La méthode retourne True
        self.assertTrue(p.est_occupe)            # La place est maintenant occupée
        self.assertEqual(p.voiture, "ABC-123")  # La voiture est bien celle entrée

if __name__ == "__main__":
    unittest.main()
