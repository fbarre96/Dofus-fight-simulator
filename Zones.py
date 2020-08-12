# -*- coding: utf-8 -*
"""@summary: definit les zones d'effets de sorts
"""


def getDistancePoint(point1, point2):
    """@summary: Retourne la distance entre le point 1 et le point 2
        @point1: un tableau de 2 entiers contenant les coordonnées du point 1
        @point2: un tableau de 2 entiers contenant les coordonnées du point 2
        @return: la distance entière séparant ces 2 points"""
    return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])


def getDistanceY(point1, point2):
    """@summary: Retourne la distance en ordonnée entre le point 1 et le point 2
        @point1: un tableau de 2 entiers contenant les coordonnees du point 1
        @point2: un tableau de 2 entiers contenant les coordonnees du point 2
        @return: la distance entière verticale séparant ces 2 points"""
    return abs(point1[1]-point2[1])


def getDistanceX(point1, point2):
    """@summary: Retourne la distance en abcisse entre le point 1 et le point 2
        @point1: un tableau de 2 entiers contenant les coordonnees du point 1
        @point2: un tableau de 2 entiers contenant les coordonnees du point 2
        @return: la distance entière horizontale séparant ces 2 points"""
    return abs(point1[0]-point2[0])


class TypeZone:
    """@summary: Définit une zone d'action pour un effet. Classe de basse héritée"""
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)
    
    @classmethod
    def getZoneList(cls):
        return [str(classe.__name__).replace("TypeZone", "") for classe in cls.subclasses]
    
    @classmethod
    def getZoneFromName(cls,name, zonepo):
        for classe in cls.subclasses:
            if classe.__name__.replace("TypeZone", "").lower() == name.lower():
                return classe(int(zonepo))
    @classmethod
    def factory(cls, zoneStr, desc):
        ret = TypeZoneCercle(0)
        if zoneStr.strip() != "":
            if "jusqu'à la cellule ciblée" in desc:
                zone = "ligne jusque de 0 cases"
                return TypeZoneLigneJusque()
            elif "Tout le monde" in zoneStr:
                return TypeZoneCercle(99)
            else:
                tailleZone = zoneStr.split(" ")[-2].strip()
                typeZone = " ".join(zoneStr.split(" ")[:-3]).strip().lower()
                typeZone = map(lambda x: x[0].upper() + x[1:].lower(), typeZone.split(" "))
                nomZone = "".join(typeZone)
                for classe in cls.subclasses:
                    if nomZone in classe.__name__:
                        return classe(tailleZone)
        return ret
    def __init__(self, zonePO=0):
        # pylint: disable=unused-argument
        """@summary: Constructeur de base d'une zone"""
        self.zonePO = zonePO
    
    def __str__(self):
        return str(self.__class__.__name__).replace("TypeZone", "") + " de "+str(self.zonePO)+" case(s)"

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        # pylint: disable=unused-argument
        """@summary: Fonction qui renvoie si une case donnée est dans la zone"""
        print("zone inconnue")
        return False
        

class TypeZoneCercle(TypeZone):
    """@summary: Définit une zone d'action circulaire pour un effet. Hérite de TypeZone"""

    def __init__(self, zonePO):
        """@summary: Initialise une instance de zone cercle
        @zonePO: le rayon du cercle
        @type: entier"""
        super().__init__()
        self.zonePO = zonePO

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone circulaire
        @departZone: case de depart de la zone (ici le centre du cercle).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort. Hérité de TypeZone
        mais inutile pour la zone Cercle
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        return getDistancePoint(departZone, caseTestee) <= self.zonePO

class TypeZoneDemiCercle(TypeZone):
    """@summary: Définit une zone d'action demi-circulaire pour un effet. Hérite de TypeZone"""

    def __init__(self, zonePO):
        """@summary: Initialise une instance de zone demi-cercle
        @zonePO: le rayon du cercle
        @type: entier"""
        super().__init__()
        self.zonePO = zonePO

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone circulaire
        @departZone: case de depart de la zone (ici le centre du cercle).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone mais inutile pour la zone Cercle
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        distance = getDistancePoint(departZone, caseTestee)
        # La demi-cercle sera horizontale si le joueur lanceur et
        # le depart de la zone sont en verticale
        horizontal = getDistanceX(joueurLanceur, departZone) == 0
        # test présence sur le cercle
        if distance > self.zonePO * 2:
            return False
        if getDistanceX(departZone, caseTestee) != getDistanceY(departZone, caseTestee):
            return False
        if horizontal:
            if getDistanceY(caseTestee, joueurLanceur) <= getDistanceY(departZone, joueurLanceur):
                return True
        else:
            if getDistanceX(caseTestee, joueurLanceur) <= getDistanceX(departZone, joueurLanceur):
                return True
        # Test dans quel demi-cercle la case est
        return False

class TypeZoneInfini(TypeZone):
    """@summary: Définit une zone d'action circulaire pour un effet. Hérite de TypeZone"""

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone circulaire
        @departZone: case de depart de la zone (ici le centre du cercle).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone mais inutile pour la zone Cercle
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        return True


class TypeZoneCercleSansCentre(TypeZone):
    """@summary: Définit une zone d'action circulaire sans centre pour un effet.
    Hérite de TypeZone"""

    def __init__(self, zonePO):
        """@summary: Initialise une instance de zone cercle sans centre
        @zonePO: le rayon du cercle
        @type: entier"""
        super().__init__()
        self.zonePO = zonePO

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone circulaire sans centre
        @departZone: case de depart de la zone (ici le centre du cercle).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone mais inutile pour la zone Cercle sans centre
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        return getDistancePoint(departZone, caseTestee) <= self.zonePO \
            and getDistancePoint(departZone, caseTestee) != 0


class TypeZoneCroix(TypeZone):
    """@summary: Définit une zone d'action en croix pour un effet. Hérite de TypeZone"""

    def __init__(self, zonePO, zonePOMax=None):
        """@summary: Initialise une instance de zone croix
        @zonePO: la taille de chaque pointe de la croix
        @type: entier"""
        super().__init__()
        self.zonePO = zonePO
        self.zonePOMax = zonePOMax

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone en croix
        @departZone: case de depart de la zone (ici le centre de la croix).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone mais inutile pour la zone croix
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        # Si la case testée n'est pas en ligne, pas dans la zone

        if getDistanceY(departZone, caseTestee) > 0 and getDistanceX(departZone, caseTestee) > 0:
            return False
        distance = getDistancePoint(departZone, caseTestee)
        if self.zonePOMax is not None:
            return distance <= self.zonePOMax and distance >= self.zonePO
        return distance <= self.zonePO


class TypeZoneCroixDiagonale(TypeZone):
    """@summary: Définit une zone d'action en croix diagonale (En X) pour un effet.
    Hérite de TypeZone"""

    def __init__(self, zonePO):
        """@summary: Initialise une instance de zone croix diagonale (en X)
        @zonePO: la taille de chaque pointe de la croix
        @type: entier"""
        # La taille du cercle inscrit est double en prenant les diagonales.
        super().__init__()
        self.zonePO = zonePO*2

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone en croix diagonale
        @departZone: case de depart de la zone (ici le centre de la croix diagonale).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone mais inutile pour la zone croix diagonale
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        # Si la case testée n'est pas en diagonale, pas dans la zone
        if getDistanceY(departZone, caseTestee) != getDistanceX(departZone, caseTestee):
            return False
        return getDistancePoint(departZone, caseTestee) <= self.zonePO


class TypeZoneAnneau(TypeZone):
    """@summary: Définit une zone d'action en anneau pour un effet. Hérite de TypeZone"""

    def __init__(self, zonePO):
        """@summary: Initialise une instance de zone anneau
        @zonePO: la taille du cercle sur lequel l'anneau extérieur sera compté
        @type: entier"""
        super().__init__()
        self.zonePO = zonePO

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone en croix diagonale
        @departZone: case de depart de la zone (ici le centre de la croix diagonale).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone mais inutile pour la zone croix diagonale
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        return getDistancePoint(departZone, caseTestee) == self.zonePO


class TypeZoneLigne(TypeZone):
    """@summary: Définit une zone d'action en ligne pour un effet. Hérite de TypeZone"""

    def __init__(self, zonePO):
        """@summary: Initialise une instance de zone ligne
        @zonePO: la taille de la ligne
        @type: entier"""
        super().__init__()
        self.zonePO = zonePO

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone en ligne
        @departZone: case de depart de la zone (ici le départ de la ligne).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone, définit le sens de la ligne
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        # calcul du sens de la ligne
        horizontal = getDistanceY(joueurLanceur, departZone) == 0
        # si la ligne est horizontal et que la case n'est pas sur la bonne ordonnée
        if horizontal and getDistanceY(departZone, caseTestee) > 0:
            return False
        # si la ligne est verticale et que la case n'est pas sur la même abcisse
        if not horizontal and getDistanceX(departZone, caseTestee) > 0:
            return False
        if horizontal:
            # Si la ligne est horizontale et que la ligne part à droite
            if joueurLanceur[0] <= departZone[0]:
                return (caseTestee[0]-departZone[0] < self.zonePO) \
                    and caseTestee[0]-departZone[0] >= 0
            # Si la ligne est horizontale et que la ligne part à gauche
            else:
                return (abs(caseTestee[0]-departZone[0]) < self.zonePO) \
                    and caseTestee[0]-departZone[0] <= 0
        else:
            # Si la ligne est verticale et que la ligne part en haut
            if joueurLanceur[1] <= departZone[1]:
                return (caseTestee[1]-departZone[1] < self.zonePO) \
                    and caseTestee[1]-departZone[1] >= 0
            # Si la ligne est verticale et que la ligne part en bas
            else:
                return (abs(caseTestee[1]-departZone[1]) < self.zonePO) \
                     and caseTestee[1]-departZone[1] <= 0


class TypeZoneLigneJusque(TypeZone):
    """@summary: Définit une zone d'action en ligne allant
    du joueur lanceur a la case de depart zone pour un effet.
    Hérite de TypeZone"""

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans
        la zone en ligne allant du lanceur jusqu'à la case de départ de la zone
        @departZone: case de depart de la zone (ici le bout de la ligne).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone, définit le sens de la ligne et le départ de la zone ici
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        # calcul de la direction de la ligne
        horizontal = getDistanceY(joueurLanceur, departZone) == 0
        # Si la ligne est horizontale et que la case n'est pas sur la même ordonnée
        if horizontal and getDistanceY(departZone, caseTestee) > 0:
            return False
        # Si la ligne est verticale  et que la case n'est pas sur la même abcisse
        if not horizontal and getDistanceX(departZone, caseTestee) > 0:
            return False
        if horizontal:
            # Si la ligne est horizontale et que la ligne part à droite
            if joueurLanceur[0] <= departZone[0]:
                return joueurLanceur[0] < caseTestee[0] and caseTestee[0] <= departZone[0]
             # Si la ligne est horizontale et que la ligne part à gauche
            else:
                return joueurLanceur[0] > caseTestee[0] and caseTestee[0] >= departZone[0]
        else:
            # Si la ligne est verticale et que la ligne part en haut
            if joueurLanceur[1] <= departZone[1]:
                return joueurLanceur[1] < caseTestee[1] and caseTestee[1] <= departZone[1]
            # Si la ligne est verticale et que la ligne part en bas
            else:
                return joueurLanceur[1] > caseTestee[1] and caseTestee[1] >= departZone[1]


class TypeZoneLignePerpendiculaire(TypeZone):
    """@summary: Définit une zone d'action en ligne perpendiculaire (en T) pour un effet.
    Le type de lancer du sort est toujours en ligne. Hérite de TypeZone"""

    def __init__(self, zonePO):
        """@summary: Initialise une instance de zone ligne perpendiculaire.
        @zonePO: la taille de la ligne perpendiculaure
        @type: entier"""
        super().__init__()
        self.zonePO = zonePO

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si un case est dans la zone en ligne perpendiculaire
        @departZone: case de depart de la zone (ici la case visée sur la ligne).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort.
        Hérité de TypeZone, définit le sens de la ligne perpendiculaire
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        # La ligne perpendiculaire sera horizontale si le joueur lanceur
        # et le depart de la zone sont en verticale
        horizontal = getDistanceX(joueurLanceur, departZone) == 0
        # si la ligne est horizontale et que les cases ne sont pas sur la meme ligne.
        if horizontal and getDistanceY(departZone, caseTestee) > 0:
            return False
        # si la ligne est verticale et que les cases ne sont pas sur la meme colonne.
        if not horizontal and getDistanceX(departZone, caseTestee) > 0:
            return False
        return getDistancePoint(departZone, caseTestee) <= self.zonePO


class TypeZoneCarre(TypeZone):
    """@summary: Définit une zone d'action en carré creux pour un effet. Hérite de TypeZone"""

    def __init__(self, zonePO):
        """@summary: Initialise une instance de zone carrée.
        @zonePO: la distance entre le départ de la zone et la zone du carré.
        @type: entier"""
        super().__init__()
        self.zonePO = zonePO

    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        """@summary: Retourne un booléen disant si une case est dans la zone carré creuse
        @departZone: case de depart de la zone (ici le centre du carré).
        Souvent donné par le point d'impact d'un sort.
        @type: tableau de 2 coordonnées entières
        @caseTestee: case dont on testera l'appartenance à la zone
        @type: tableau de 2 coordonnées entières
        @joueurLanceur: le joueur qui lance le sort. Hérité de TypeZone, inutile ici.
        @type: Personnage
        @return: Renvoie vrai si la case testée est dans la zone, faux sinon
        """
        return (getDistanceX(caseTestee, departZone) <= self.zonePO or \
            getDistanceY(caseTestee, departZone) <= self.zonePO) and \
                 getDistanceX(caseTestee, departZone) <= self.zonePO and \
                      getDistanceY(caseTestee, departZone) <= self.zonePO
