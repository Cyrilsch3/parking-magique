class PlaceOccupeeError(Exception):
    # La place est déjà occupée
    pass

class PlaceInvalideException(Exception):
    # La place entré n'existe pas / n'est pas valide
    pass

#ici tu mets ton exception puis 
# tu remplaces le value error que tu veux dans les classes 
# et apres tu vas dans GUI et tu changes aussi le value error par le nom de ton exception