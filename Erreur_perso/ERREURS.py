class PlaceOccupeeError(Exception):
    # La place est déjà occupée
    pass

class PlaceInvalideException(Exception):
    # La place entré n'existe pas / n'est pas valide
    pass

class ErreurDansLaDB(Exception):
    # toutes les erreurs qui sont propre a la db remonteront ici
    pass

class DateAbonnementInvalide(Exception):
    # La date entrée n'est pas valide
    pass

class erreurMvp(Exception):
    # toutes les erreurs qui sont propre a la db remonteront ici
    pass