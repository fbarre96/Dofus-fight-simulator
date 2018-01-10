# -*- coding: utf-8 -*
taille_sprite = 30
taille_carte = 15
x_grille = 0
y_grille = 0
width_grille = taille_carte*taille_sprite
height_grille = taille_carte*taille_sprite

x_sorts = 0
y_sorts = y_grille + height_grille
height_sorts = 200
width_sorts = width_grille

width_fenetre = width_sorts
height_fenetre = height_grille+height_sorts

image_vide_1 = "images/vide1.png"
image_vide_2 = "images/vide2.png"
image_team_1 = "images/T1.png"
image_team_2 = "images/T2.png"
image_prevision = "images/prevision.png"
image_zone = "images/zone.png"

def normaliser(chaine):
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