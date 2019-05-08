# -*- coding: utf-8 -*
#taille d'un des côté du carré d'un sprite sur la grille de jeu
taille_sprite = 30
#Nombre de case sur une ligne et colonne de la carte
taille_carte = 15
#pixels de début de l'affichage de la grille de jeu
x_grille = 0
y_grille = 0
#calculs de la largeur et hauteur de la grille de jeu
width_grille = taille_carte*taille_sprite
height_grille = taille_carte*taille_sprite
#pixels de début de l'affichage de la grille des sorts disponibles
x_sorts = 0
y_sorts = y_grille + height_grille
#calculs de la largeur et hauteur de la grille des sorts disponibles
height_sorts = 200
width_sorts = width_grille

#Calcul de la taille de la fenetre
width_fenetre = width_sorts
height_fenetre = height_grille+height_sorts

image_vide_1 = "images/vide1.png"
image_vide_2 = "images/vide2.png"
image_team_1 = "images/T1.png"
image_team_2 = "images/T2.png"
image_prevision = "images/prevision.png"
image_zone = "images/zone.png"

def normaliser(chaine):
	"""@summary: enlève les accents d'une chaîne de caractère et la met en minuscule. Remplace également les espaces et apostrophes par un underscore.
	@chaine: chaîne de caractère à normaliser
	@type: string
	@return: La chaîne de caractère une fois les remplacements effectués.
	"""
	chaine = chaine.lower()
	chaine = chaine.replace(u" ",u"_")
	chaine = chaine.replace(u"'",u"_")
	chaine = chaine.replace(u"é",u"e")
	chaine = chaine.replace(u"è",u"e")
	chaine = chaine.replace(u"ê",u"e")
	chaine = chaine.replace(u"à",u"a")
	chaine = chaine.replace(u"ï",u"i")
	chaine = chaine.replace(u"î",u"i")
	chaine = chaine.replace(u"ç",u"c")
	chaine = chaine.replace(u"â",u"a")
	return chaine