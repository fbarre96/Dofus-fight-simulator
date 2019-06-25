"""@summary: Rassemble les sorts du Pandawa
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetEtat import EffetEtat, EffetEtatSelf, EffetRetireEtat, EffetRafraichirEtats, EffetRetireEtatSelf
from Effets.EffetDegats import EffetDegats, EffetVolDeVie
from Effets.EffetSoin import EffetSoinPerPVMax
from Effets.EffetPousser import EffetPousser, EffetAttire
from Effets.EffetRet import EffetRetPM
from Effets.EffetPorte import EffetPorte, EffetLance
from Effets.EffetInvoque import EffetInvoque
import Zones
from Etats.Etat import Etat
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatBoostBaseDeg import EtatBoostBaseDeg
from Etats.EtatBoostSortCarac import EtatBoostSortCarac
from Etats.EtatModDeg import EtatModDegPer
from Etats.EtatEffet import EtatEffetDebutTour, EtatEffetSiRetraitEtat
import Personnages


def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    sortsDebutCombat.append(
        Sort.Sort("Sobre", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetDebutTour("Sobre si non saoul", 0, -1, EffetEtatSelf(Etat("Sobre", 0, -1), etat_requis_lanceur="!Saoul|!Colère de Zatoïshwan|!Sobre"), "Sobre", "lanceur")), EffetEtatSelf(EtatEffetSiRetraitEtat("Sobre si non saoul", 0, -1, EffetEtatSelf(Etat("Sobre", 0, -1), etat_requis_lanceur="!Saoul|!Colère de Zatoïshwan|!Sobre"), "Saoul", "Sobre", "lanceur"))], [], 0, 99, 99, 0, 0, "cercle", False)
    )
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    sorts = []
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Poing Enflammé", 1, 3, 1, 3, [EffetDegats(16, 21, "Feu", etat_requis_lanceur="Saoul")], [EffetDegats(21, 26, "Feu", etat_requis_lanceur="Saoul")], 5, 99, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Feu.
        L'état Saoul est nécessaire.""", chaine=True),

        Sort.Sort("Poing Enflammé", 25, 3, 1, 3, [EffetDegats(19, 24, "Feu", etat_requis_lanceur="Saoul")], [EffetDegats(24, 29, "Feu", etat_requis_lanceur="Saoul")], 5, 99, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Feu.
        L'état Saoul est nécessaire.""", chaine=True),

        Sort.Sort("Poing Enflammé", 52, 3, 1, 3, [EffetDegats(22, 27, "Feu", etat_requis_lanceur="Saoul")], [EffetDegats(27, 32, "Feu", etat_requis_lanceur="Saoul")], 5, 99, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Feu.
        L'état Saoul est nécessaire.""", chaine=True)
        ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Cercle Brûlant", 105, 4, 2, 5, [EffetDegats(34, 38, "Feu", zone=Zones.TypeZoneCroix(1), etat_requis_lanceur="Sobre", cible_non_requise=True)], [EffetDegats(39, 43, "Feu", zone=Zones.TypeZoneCroix(1), etat_requis_lanceur="Sobre", cible_non_requise=True)], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu en zone.
        Nécessite l'état Sobre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Ribote", 1, 3, 1, 3, [EffetDegats(16, 20, "Terre")], [EffetDegats(19, 23, "Terre")], 5, 3, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Ribote", 30, 3, 1, 3, [EffetDegats(19, 23, "Terre")], [EffetDegats(22, 26, "Terre")], 5, 3, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Ribote", 60, 3, 1, 3, [EffetDegats(22, 26, "Terre")], [EffetDegats(25, 29, "Terre")], 5, 3, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Gueule de Bois", 110, 3, 1, 1, [EffetDegats(24, 28, "Terre", etat_requis_lanceur="Saoul"), EffetEtatSelf(EtatBoostBaseDeg("Gueule de Bois", 0, 3, "Gueule de Bois", 5))], [EffetDegats(29, 33, "Terre", etat_requis_lanceur="Sobre"), EffetEtatSelf(EtatBoostBaseDeg("Gueule de Bois", 0, 3, "Gueule de Bois", 5))], 5, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Terre.
    Les dommages du sort augmentent aux lancers suivants.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Bombance", 1, 2, 0, 0, [EffetEtat(Etat('Saoul', 0, 2), etat_requis_lanceur="Sobre"), EffetEtat(EtatBoostCaracFixe("Bombance", 0, 2, "tacle", 10))], [], 0, 1, 1, 2, 0, "cercle", False, description="""Applique l'état Saoul et donne du tacle. Ne bloque pas le lancer des sorts Sobre.""", chaine=True),

        Sort.Sort("Bombance", 20, 2, 0, 0, [EffetEtat(Etat('Saoul', 0, 2), etat_requis_lanceur="Sobre"), EffetEtat(EtatBoostCaracFixe("Bombance", 0, 2, "tacle", 20))], [], 0, 1, 1, 2, 0, "cercle", False, description="""Applique l'état Saoul et donne du tacle. Ne bloque pas le lancer des sorts Sobre.""", chaine=True),

        Sort.Sort("Bombance", 40, 2, 0, 0, [EffetEtat(Etat('Saoul', 0, 2), etat_requis_lanceur="Sobre"), EffetEtat(EtatBoostCaracFixe("Bombance", 0, 2, "tacle", 30))], [], 0, 1, 1, 2, 0, "cercle", False, description="""Applique l'état Saoul et donne du tacle. Ne bloque pas le lancer des sorts Sobre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Picole", 101, 1, 0, 0,
                  [
                      EffetEtat(Etat('Saoul', 0, 4), etat_requis_lanceur="Sobre|Sobre|!Picole"),
                      EffetEtat(EtatBoostCaracFixe("Picole", 0, 4, "PM", -1), etat_requis_lanceur="Sobre|Sobre|!Picole"),
                      EffetEtat(EtatModDegPer("Picole", 0, 4, 75), etat_requis_lanceur="Sobre|Sobre|!Picole"),
                      EffetRetireEtat("Sobre", etat_requis_lanceur="Sobre|Sobre|!Picole"),
                      EffetRetireEtat("Colère de Zatoïshwan", etat_requis_lanceur="Picole"),
                      EffetRafraichirEtats(4, etat_requis_lanceur="Picole"),
                  ], [], 0, 99, 99, 0, 0, "cercle", True, description="""Applique l'état Saoul et retire 1 PM.
    Réduit les dommages reçus.
    Relancer Picole permet d'annuler ses effets et de désenvoûter le lanceur.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Epouvante", 3, 2, 1, 3, [EffetEtat(EtatBoostCaracFixe("Epouvante", 0, 2, "cc", -5)), EffetPousser(1)], [EffetEtat(EtatBoostCaracFixe("Epouvante", 0, 2, "cc", -10)), EffetPousser(1)], 15, 3, 1, 0, 1, "ligne", True, description="""Repousse la cible et réduit la probabilité d'occasionner des critiques aux ennemis.""", chaine=True),

        Sort.Sort("Epouvante", 35, 2, 1, 5, [EffetEtat(EtatBoostCaracFixe("Epouvante", 0, 2, "cc", -10)), EffetPousser(1)], [EffetEtat(EtatBoostCaracFixe("Epouvante", 0, 2, "cc", -15)), EffetPousser(1)], 15, 3, 1, 0, 1, "ligne", True, description="""Repousse la cible et réduit la probabilité d'occasionner des critiques aux ennemis.""", chaine=True),

        Sort.Sort("Epouvante", 67, 2, 1, 7, [EffetEtat(EtatBoostCaracFixe("Epouvante", 0, 3, "cc", -15)), EffetPousser(1)], [EffetEtat(EtatBoostCaracFixe("Epouvante", 0, 3, "cc", -20)), EffetPousser(1)], 15, 3, 1, 0, 1, "ligne", True, description="""Repousse la cible et réduit la probabilité d'occasionner des critiques aux ennemis.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Consolation", 115, 3, 1, 6, [EffetAttire(4, etat_requis_lanceur="Sobre"), EffetSoinPerPVMax(7, etat_requis_lanceur="Sobre")], [], 0, 1, 99, 0, 0, "ligne", True, description="""Attire la cible alliée vers le lanceur et la soigne.
    Nécessite l'état Sobre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Souffle Alcoolisé", 6, 3, 1, 4, [EffetDegats(16, 17, "Air", etat_requis_lanceur="Saoul"), EffetPousser(1)], [EffetDegats(20, 21, "Air", etat_requis_lanceur="Saoul"), EffetPousser(1)], 5, 99, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air et pousse la cible.
    L'état Saoul est nécessaire.""", chaine=True),

        Sort.Sort("Souffle Alcoolisé", 42, 3, 1, 6, [EffetDegats(20, 21, "Air", etat_requis_lanceur="Saoul"), EffetPousser(1)], [EffetDegats(24, 25, "Air", etat_requis_lanceur="Saoul"), EffetPousser(1)], 5, 99, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air et pousse la cible.
    L'état Saoul est nécessaire.""", chaine=True),

        Sort.Sort("Souffle Alcoolisé", 74, 3, 1, 8, [EffetDegats(24, 25, "Air", etat_requis_lanceur="Saoul"), EffetPousser(1)], [EffetDegats(28, 29, "Air", etat_requis_lanceur="Saoul"), EffetPousser(1)], 5, 99, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air et pousse la cible.
    L'état Saoul est nécessaire.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Engourdissement", 120, 5, 1, 7, [EffetDegats(38, 42, "Air", etat_requis_lanceur="Sobre", zone=Zones.TypeZoneCroixDiagonale(1)), EffetRetPM(3, zone=Zones.TypeZoneCroixDiagonale(1))], [EffetDegats(42, 46, "Air", etat_requis_lanceur="Sobre", zone=Zones.TypeZoneCroixDiagonale(1)), EffetRetPM(3, zone=Zones.TypeZoneCroixDiagonale(1))], 25, 1, 99, 0, 1, "cercle", True, description="""Occasionne des dommages Air et retire des PM en zone.
    Nécessite l'état Sobre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Karcham", 9, 1, 1, 1, [
            # Indique qu'on doit lancer
            EffetEtatSelf(Etat("Doit Lancer", 0, 1), etat_requis_lanceur="Karcham|Sobre", cible_non_requise=True),
            # Retire Karcham au lanceur
            EffetRetireEtatSelf("Karcham", etat_requis_lanceur="Karcham|Sobre", cible_non_requise=True),
            # Lance et consomme etat Doit Lancer au Lanceur.
            EffetLance(etat_requis_lanceur="Doit Lancer", consomme_etat=True, cible_non_requise=True),
            # Si on n'a pas lancer, on porte
            EffetEtatSelf(EtatBoostSortCarac("Karcham", 0, -1, "Karcham", "POMax", 5), etat_requis="!Karcham", etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetEtat(EtatBoostCaracFixe("Karcham", 0, -1, "checkLdv", False), etat_requis="!Karcham", etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetPorte(etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetRetireEtatSelf("Doit Lancer", cible_non_requise=True)], [], 0, 6, 1, 0, 0, "ligne", True, description="""Porte la cible. Au second lancer, jette la cible à 6 cellules maximum.
    Désactive les lignes de vue des sorts de la cible portée.""", chaine=False),
        Sort.Sort("Karcham", 9, 1, 1, 1, [
            # Indique qu'on doit lancer
            EffetEtatSelf(Etat("Doit Lancer", 0, 1), etat_requis_lanceur="Karcham|Sobre", cible_non_requise=True),
            # Retire Karcham au lanceur
            EffetRetireEtatSelf("Karcham", etat_requis_lanceur="Karcham|Sobre", cible_non_requise=True),
            # Lance et consomme etat Doit Lancer au Lanceur.
            EffetLance(etat_requis_lanceur="Doit Lancer", consomme_etat=True, cible_non_requise=True),
            # Si on n'a pas lancer, on porte
            EffetEtatSelf(EtatBoostSortCarac("Karcham", 0, -1, "Karcham", "POMax", 5), etat_requis="!Karcham", etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetEtat(EtatBoostCaracFixe("Karcham", 0, -1, "checkLdv", False), etat_requis="!Karcham", etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetPorte(etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetRetireEtatSelf("Doit Lancer", cible_non_requise=True)], [], 0, 6, 1, 0, 0, "ligne", True, description="""Porte la cible. Au second lancer, jette la cible à 6 cellules maximum.
    Désactive les lignes de vue des sorts de la cible portée.""", chaine=False),
        Sort.Sort("Karcham", 9, 1, 1, 1, [
            # Indique qu'on doit lancer
            EffetEtatSelf(Etat("Doit Lancer", 0, 1), etat_requis_lanceur="Karcham|Sobre", cible_non_requise=True),
            # Retire Karcham au lanceur
            EffetRetireEtatSelf("Karcham", etat_requis_lanceur="Karcham|Sobre", cible_non_requise=True),
            # Lance et consomme etat Doit Lancer au Lanceur.
            EffetLance(etat_requis_lanceur="Doit Lancer", consomme_etat=True, cible_non_requise=True),
            # Si on n'a pas lancer, on porte
            EffetEtatSelf(EtatBoostSortCarac("Karcham", 0, -1, "Karcham", "POMax", 5), etat_requis="!Karcham", etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetEtat(EtatBoostCaracFixe("Karcham", 0, -1, "checkLdv", False), etat_requis="!Karcham", etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetPorte(etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetRetireEtatSelf("Doit Lancer", cible_non_requise=True)], [], 0, 6, 1, 0, 0, "ligne", True, description="""Porte la cible. Au second lancer, jette la cible à 6 cellules maximum.
    Désactive les lignes de vue des sorts de la cible portée.""", chaine=False),
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Chamrak", 125, 1, 1, 1, [EffetLance(etat_requis_lanceur="Chamrak|Sobre", consomme_etat=True, cible_non_requise=True), EffetEtatSelf(EtatBoostSortCarac("Chamrak", 0, -1, "Chamrak", "POMax", 3), etat_requis="!Chamrak", etat_requis_lanceur="!Chamrak|Sobre"), EffetEtat(EtatBoostCaracFixe("Chamrak", 0, -1, "checkLdv", False), etat_requis="!Chamrak", etat_requis_lanceur="Chamrak|Sobre"), EffetPorte(etat_requis_lanceur="Chamrak|Sobre")], [], 0, 6, 1, 0, 0, "ligne", False, description="""Porte la cible. Au second lancer, jette la cible à 4 cellules maximum sans ligne de vue.
    Désactive les lignes de vue des sorts de la cible portée.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Schnaps", 13, 4, 2, 5, [EffetDegats(23, 25, "Air", zone=Zones.TypeZoneCroix(1), cible_non_requise=True, etat_requis_lanceur="Sobre")], [EffetDegats(27, 29, "Air", zone=Zones.TypeZoneCroix(1), cible_non_requise=True, etat_requis_lanceur="Sobre")], 15, 2, 99, 0, 0, "diagonale", True, description="""Occasionne des dommages Air en zone.""", chaine=True),

        Sort.Sort("Schnaps", 54, 4, 2, 6, [EffetDegats(29, 31, "Air", zone=Zones.TypeZoneCroix(1), cible_non_requise=True, etat_requis_lanceur="Sobre")], [EffetDegats(33, 35, "Air", zone=Zones.TypeZoneCroix(1), cible_non_requise=True, etat_requis_lanceur="Sobre")], 15, 2, 99, 0, 0, "diagonale", True, description="""Occasionne des dommages Air en zone.""", chaine=True),

        Sort.Sort("Schnaps", 94, 4, 2, 7, [EffetDegats(35, 37, "Air", zone=Zones.TypeZoneCroix(1), cible_non_requise=True, etat_requis_lanceur="Sobre")], [EffetDegats(39, 41, "Air", zone=Zones.TypeZoneCroix(1), cible_non_requise=True, etat_requis_lanceur="Sobre")], 15, 2, 99, 0, 0, "diagonale", True, description="""Occasionne des dommages Air en zone.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Liqueur", 130, 3, 2, 8, [EffetVolDeVie(19, 23, "Air", etat_requis_lanceur="Saoul")], [EffetVolDeVie(23, 27, "Air", etat_requis_lanceur="Saoul")], 5, 3, 2, 0, 1, "cercle", True, description="""Vole de la vie dans l'élément Air.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Propulsion", 17, 3, 1, 3, [EffetLance(cible_non_requise=True), EffetDegats(27, 33, "Feu", zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis", cible_non_requise=True), EffetPousser(1, "CaseCible", cibles_possibles="Ennemis", cible_non_requise=True, zone=Zones.TypeZoneCroix(1))], [EffetLance(cible_non_requise=True), EffetDegats(32, 38, "Feu", zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis", cible_non_requise=True), EffetPousser(1, "CaseCible", cibles_possibles="Ennemis", zone=Zones.TypeZoneCroix(1), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Lance l'entité portée.
    Occasionne des dommages Feu aux ennemis et repousse autour de la cellule ciblée.""", chaine=True),
        Sort.Sort("Propulsion", 58, 3, 1, 4, [EffetLance(cible_non_requise=True), EffetDegats(37, 43, "Feu", zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis", cible_non_requise=True), EffetPousser(1, "CaseCible", cibles_possibles="Ennemis", cible_non_requise=True, zone=Zones.TypeZoneCroix(1))], [EffetLance(cible_non_requise=True), EffetDegats(42, 48, "Feu", zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis", cible_non_requise=True), EffetPousser(1, "CaseCible", cibles_possibles="Ennemis", zone=Zones.TypeZoneCroix(1), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Lance l'entité portée.
    Occasionne des dommages Feu aux ennemis et repousse autour de la cellule ciblée.""", chaine=True),
        Sort.Sort("Propulsion", 102, 3, 1, 5, [EffetLance(cible_non_requise=True), EffetDegats(47, 53, "Feu", zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis", cible_non_requise=True), EffetPousser(1, "CaseCible", cibles_possibles="Ennemis", cible_non_requise=True, zone=Zones.TypeZoneCroix(1))], [EffetLance(cible_non_requise=True), EffetDegats(52, 58, "Feu", zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis", cible_non_requise=True), EffetPousser(1, "CaseCible", cibles_possibles="Ennemis", zone=Zones.TypeZoneCroix(1), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Lance l'entité portée.
    Occasionne des dommages Feu aux ennemis et repousse autour de la cellule ciblée.""", chaine=True)
    ]))
    # Attire de 8 cases max, porté de 15, pas de ldv. Soigne 53,81quand porté à 1 case autour
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Ivresse", 22, 4, 1, 1, [EffetInvoque("Tonneau Attractif", True, etat_requis_lanceur="Sobre", cibles_possibles="", cible_non_requise=True)], [], 0, 1, 1, 5, 0, "ligne", True, description="""Invoque un tonneau qui attire les ennemis. Il attire également les alliés s'ils sont dans l'état Saoul.
    S'il est porté ou jeté : soigne autour de lui.""", chaine=True),

        Sort.Sort("Ivresse", 65, 4, 1, 1, [EffetInvoque("Tonneau Attractif", True, etat_requis_lanceur="Sobre", cibles_possibles="", cible_non_requise=True)], [], 0, 1, 1, 5, 0, "ligne", True, description="""Invoque un tonneau qui attire les ennemis. Il attire également les alliés s'ils sont dans l'état Saoul.
    S'il est porté ou jeté : soigne autour de lui.""", chaine=True),

        Sort.Sort("Ivresse", 108, 4, 1, 1, [EffetInvoque("Tonneau Attractif", True, etat_requis_lanceur="Sobre", cibles_possibles="", cible_non_requise=True)], [], 0, 1, 1, 5, 0, "ligne", True, description="""Invoque un tonneau qui attire les ennemis. Il attire également les alliés s'ils sont dans l'état Saoul.
    S'il est porté ou jeté : soigne autour de lui.""", chaine=True)
    ]))
    return sorts
    