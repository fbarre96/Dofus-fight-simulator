# -*- coding: utf-8 -*
"""
@summary: Définit les constantes pour le simulateur
"""
# taille d'un des côté du carré d'un sprite sur la grille de jeu
taille_sprite = 30
# Nombre de case sur une ligne et colonne de la carte
taille_carte = 15
# pixels de début de l'affichage de la grille de jeu
x_grille = 0
y_grille = 0
# calculs de la largeur et hauteur de la grille de jeu
width_grille = taille_carte*taille_sprite
height_grille = taille_carte*taille_sprite
# pixels de début de l'affichage de la grille des sorts disponibles
x_sorts = 0
y_sorts = y_grille + height_grille
# calculs de la largeur et hauteur de la grille des sorts disponibles
height_sorts = 200
width_sorts = width_grille

# Calcul de la taille de la fenetre
width_fenetre = width_sorts
height_fenetre = height_grille+height_sorts

image_vide_1 = "images/vide1.png"
image_vide_2 = "images/vide2.png"
image_team_1 = "images/T1.png"
image_team_2 = "images/T2.png"
image_prevision_sort = "images/prevision_sort.jpg"
image_prevision_deplacement = "images/prevision_deplacement.jpg"
image_prevision_ldv = "images/prevision_ldv.jpg"
image_prevision_tacle = "images/prevision_tacle.jpg"
image_prevision_zone = "images/prevision_zone.jpg"


def normaliser(chaine):
    """@summary: enlève les accents d'une chaîne de caractère et la met en minuscule.
        Remplace également les espaces et apostrophes par un underscore.
    @chaine: chaîne de caractère à normaliser
    @type: string
    @return: La chaîne de caractère une fois les remplacements effectués.
    """
    chaine = chaine.lower()
    chaine = chaine.replace(" ", "_")
    chaine = chaine.replace("'", "_")
    chaine = chaine.replace("é", "e")
    chaine = chaine.replace("è", "e")
    chaine = chaine.replace("ê", "e")
    chaine = chaine.replace("à", "a")
    chaine = chaine.replace("ï", "i")
    chaine = chaine.replace("î", "i")
    chaine = chaine.replace("ç", "c")
    chaine = chaine.replace("â", "a")
    return chaine


