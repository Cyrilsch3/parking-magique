import unittest
from MVP import Place

class TestPlace(unittest.TestCase):

    def test_occuper_place_libre(self):
        # Arrange
        p = Place(-1, 'A', '01', 'Compacte')

        # Act
        result = p.occuper("ABC-123")

        # Assert
        self.assertTrue(result)
        self.assertTrue(p.est_occupe)
        self.assertEqual(p.voiture, "ABC-123")

    def test_occuper_place_deja_occupee(self):
        p = Place(-1, 'A', '01', 'Compacte')
        p.occuper("ABC-123")

        # Un deuxième véhicule essaie d'occuper
        result = p.occuper("ZZZ-999")

        self.assertFalse(result)
        self.assertEqual(p.voiture, "ABC-123")  # ne change pas
