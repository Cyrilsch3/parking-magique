import unittest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, date, timedelta
from les_classes import Place, Tarif, Abonnement, Parking, DateAbonnementInvalide


class TestPlace(unittest.TestCase):
    pass

class TestTarif(unittest.TestCase):
    pass

class TestAbonnement(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()