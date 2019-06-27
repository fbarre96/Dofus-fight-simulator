"""@summary: Rassemble les sorts du Pandawa
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetEtat import EffetEtat, EffetEtatSelf, EffetRetireEtat, EffetRafraichirEtats, EffetRetireEtatSelf
from Effets.EffetDegats import EffetDegats, EffetVolDeVie, EffetDegatsSelonPMUtilises
from Effets.EffetSoin import EffetSoinPerPVMax
from Effets.EffetPousser import EffetPousser, EffetAttire
from Effets.EffetRet import EffetRetPM
from Effets.EffetPorte import EffetPorte, EffetLance
from Effets.EffetInvoque import EffetInvoque
from Effets.EffetTp import EffetTpSymSelf
import Zones
from Etats.Etat import Etat
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatBoostBaseDeg import EtatBoostBaseDeg
from Etats.EtatBoostSortCarac import EtatBoostSortCarac
from Etats.EtatModDeg import EtatModDegPer
from Etats.EtatModSoin import EtatModSoinPer
from Etats.EtatBouclier import EtatBouclierPerLvl
from Etats.EtatEffet import EtatEffetDebutTour, EtatEffetSiRetraitEtat, EtatEffetSiSubit
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
                      EffetEtat(Etat('Saoul', 0, 4), etat_requis_lanceur="Sobre|!Picole"),
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
        Sort.Sort("Chamrak", 125, 1, 1, 1, [
            # Indique qu'on doit lancer
            EffetEtatSelf(Etat("Doit Lancer", 0, 1), etat_requis_lanceur="Chamrak|Sobre", cible_non_requise=True),
            # Retire Chamrak au lanceur
            EffetRetireEtatSelf("Chamrak", etat_requis_lanceur="Chamrak|Sobre", cible_non_requise=True),
            # Lance et consomme etat Doit Lancer au Lanceur.
            EffetLance(etat_requis_lanceur="Doit Lancer", consomme_etat=True, cible_non_requise=True),
            # Si on n'a pas lancer, on porte
            EffetEtatSelf(EtatBoostSortCarac("Chamrak", 0, -1, "Chamrak", "POMax", 3), etat_requis="!Chamrak", etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetEtat(EtatBoostCaracFixe("Chamrak", 0, -1, "checkLdv", False), etat_requis="!Chamrak", etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetPorte(etat_requis_lanceur="!Doit Lancer|Sobre"),
            EffetRetireEtatSelf("Doit Lancer", cible_non_requise=True)], [], 0, 6, 1, 0, 0, "ligne", False, description="""Porte la cible. Au second lancer, jette la cible à 4 cellules maximum sans ligne de vue.
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
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Eau-de-vie", 135, 4, 1, 3, [EffetLance(cible_non_requise=True, etat_requis_lanceur="Sobre"), EffetSoinPerPVMax(15, zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis", cible_non_requise=True, etat_requis_lanceur="Sobre")], [], 15, 2, 99, 0, 0, "ligne", True, description="""Lance l'entité portée.
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
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Ebriété", 140, 3, 1, 1, [EffetInvoque("Tonneau Incapacitant", True, etat_requis_lanceur="Sobre", cibles_possibles="", cible_non_requise=True)], [], 0, 1, 1, 4, 0, "cercle", False, description="""Invoque un Tonneau qui augmente la Puissance en zone autour de lui.
    Quand il est jeté, il retire des PM en zone aux ennemis autour du point d'impact.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Stabilisation", 27, 1, 0, 2, [EffetEtat(Etat('Enraciné', 0, 1), etat_requis_lanceur="Sobre"), EffetEtat(EtatBoostCaracFixe("Enraciné", 0, 1, "esqPM", 20), etat_requis_lanceur="Sobre")], [], 0, 1, 1, 4, 1, "ligne", False, description="""Empéche la cible d'étre déplacée.
    Augmente les résistances aux pertes de PM.""", chaine=True),

        Sort.Sort("Stabilisation", 72, 1, 0, 4, [EffetEtat(Etat('Enraciné', 0, 1), etat_requis_lanceur="Sobre"), EffetEtat(EtatBoostCaracFixe("Enraciné", 0, 1, "esqPM", 30), etat_requis_lanceur="Sobre")], [], 0, 1, 1, 3, 1, "ligne", False, description="""Empéche la cible d'étre déplacée.
    Augmente les résistances aux pertes de PM.""", chaine=True),

        Sort.Sort("Stabilisation", 118, 1, 0, 6, [EffetEtat(Etat('Enraciné', 0, 1), etat_requis_lanceur="Sobre"), EffetEtat(EtatBoostCaracFixe("Enraciné", 0, 1, "esqPM", 40), etat_requis_lanceur="Sobre")], [], 0, 1, 1, 2, 1, "ligne", False, description="""Empéche la cible d'étre déplacée.
    Augmente les résistances aux pertes de PM.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Varappe", 145, 2, 0, 0, [EffetEtat(EtatBoostCaracFixe("Varappe", 0, 1, "tacle", 50), etat_requis_lanceur="Sobre"), EffetEtat(EtatEffetSiSubit("Varappe", 0, 1, EffetPorte(), "Varappe", "lanceur", "attaquant", "melee"))], [], 0, 1, 1, 2, 0, "cercle", False, description="""Donne du tacle et si le lanceur subit une attaque de mélée, il porte son attaquant.
    Nécessite l'état Sobre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Eviction", 32, 2, 1, 1, [EffetDegats(12, 16, "Terre", etat_requis_lanceur="Saoul"), EffetTpSymSelf(etat_requis_lanceur="Saoul")], [EffetDegats(15, 19, "Terre", etat_requis_lanceur="Saoul"), EffetTpSymSelf(etat_requis_lanceur="Saoul")], 25, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Terre aux ennemis.
    La cible est téléportée derrière le lanceur.""", chaine=True),

        Sort.Sort("Eviction", 81, 2, 1, 1, [EffetDegats(15, 19, "Terre", etat_requis_lanceur="Saoul"), EffetTpSymSelf(etat_requis_lanceur="Saoul")], [EffetDegats(18, 22, "Terre", etat_requis_lanceur="Saoul"), EffetTpSymSelf(etat_requis_lanceur="Saoul")], 25, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Terre aux ennemis.
    La cible est téléportée derrière le lanceur.""", chaine=True),

        Sort.Sort("Eviction", 124, 2, 1, 1, [EffetDegats(18, 22, "Terre", etat_requis_lanceur="Saoul"), EffetTpSymSelf(etat_requis_lanceur="Saoul")], [EffetDegats(21, 25, "Terre", etat_requis_lanceur="Saoul"), EffetTpSymSelf(etat_requis_lanceur="Saoul")], 25, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Terre aux ennemis.
    La cible est téléportée derrière le lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Nausée", 150, 2, 2, 6, [EffetDegats(7, 9, "Air", etat_requis_lanceur="Saoul"), EffetPousser(2, source="CaseCible", cible="Lanceur", etat_requis_lanceur="Saoul")], [EffetDegats(9, 11, "Air", etat_requis_lanceur="Saoul"), EffetPousser(2, source="CaseCible", cible="Lanceur", etat_requis_lanceur="Saoul")], 5, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air et repousse le lanceur de la cible.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Ethylo", 38, 3, 2, 5, [EffetDegats(16, 20, "Eau", etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Ethylo", 0, 2, "retPA", -10), etat_requis_lanceur="Saoul")], [EffetDegats(20, 24, "Eau", etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Ethylo", 0, 2, "retPA", -15), etat_requis_lanceur="Saoul")], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.
    Applique un malus au retrait de PA.""", chaine=True),

        Sort.Sort("Ethylo", 90, 3, 2, 5, [EffetDegats(19, 23, "Eau", etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Ethylo", 0, 2, "retPA", -20), etat_requis_lanceur="Saoul")], [EffetDegats(23, 27, "Eau", etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Ethylo", 0, 2, "retPA", -25), etat_requis_lanceur="Saoul")], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.
    Applique un malus au retrait de PA.""", chaine=True),

        Sort.Sort("Ethylo", 132, 3, 2, 6, [EffetDegats(22, 26, "Eau", etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Ethylo", 0, 2, "retPA", -30), etat_requis_lanceur="Saoul")], [EffetDegats(26, 30, "Eau", etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Ethylo", 0, 2, "retPA", -35), etat_requis_lanceur="Saoul")], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.
    Applique un malus au retrait de PA.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Distillation", 155, 5, 3, 6, [EffetDegats(38, 42, "Eau", zone=Zones.TypeZoneCarre(1), etat_requis_lanceur="Sobre", cible_non_requise=True), EffetEtat(EtatBoostCaracFixe("Distillation", 0, 1, "PO", -5), etat_requis_lanceur="Sobre", zone=Zones.TypeZoneCarre(1), cible_non_requise=True)], [EffetDegats(42, 46, "Eau", cible_non_requise=True, zone=Zones.TypeZoneCarre(1), etat_requis_lanceur="Sobre"), EffetEtat(EtatBoostCaracFixe("Distillation", 0, 1, "PO", -5), etat_requis_lanceur="Sobre", cible_non_requise=True, zone=Zones.TypeZoneCarre(1))], 25, 1, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Eau en zone et retire de la portée.
    Nécessite l'état Sobre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Souillure", 44, 2, 1, 2, [EffetRafraichirEtats(1, etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Souillure", 0, 1, "pui", -70), etat_requis_lanceur="Saoul")], [EffetRafraichirEtats(1, etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Souillure", 0, 1, "pui", -100), etat_requis_lanceur="Saoul")], 15, 1, 1, 2, 0, "ligne", True, description="""Réduit la durée des effets sur la cible de 1 tour.
    Applique un malus de Puissance.
    L'état Saoul est nécessaire.""", chaine=True),

        Sort.Sort("Souillure", 97, 2, 1, 2, [EffetRafraichirEtats(1, etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Souillure", 0, 1, "pui", -110), etat_requis_lanceur="Saoul")], [EffetRafraichirEtats(1, etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Souillure", 0, 1, "pui", -140), etat_requis_lanceur="Saoul")], 15, 1, 1, 1, 0, "ligne", True, description="""Réduit la durée des effets sur la cible de 1 tour.
    Applique un malus de Puissance.
    L'état Saoul est nécessaire.""", chaine=True),

        Sort.Sort("Souillure", 137, 2, 1, 2, [EffetRafraichirEtats(1, etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Souillure", 0, 1, "pui", -150), etat_requis_lanceur="Saoul")], [EffetRafraichirEtats(1, etat_requis_lanceur="Saoul"), EffetEtat(EtatBoostCaracFixe("Souillure", 0, 1, "pui", -180), etat_requis_lanceur="Saoul")], 15, 2, 1, 0, 0, "ligne", True, description="""Réduit la durée des effets sur la cible de 1 tour.
    Applique un malus de Puissance.
    L'état Saoul est nécessaire.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Brassage", 160, 2, 0, 3, [EffetEtat(Etat("Pesanteur", 0, 1), etat_requis_lanceur="Saoul")], [], 0, 1, 1, 2, 0, "cercle", True, description="""Applique l'état Pesanteur.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Vulnérabilité", 50, 3, 1, 3, [EffetEtat(EtatModDegPer("Vulnérabilité", 0, 2, 115), etat_requis_lanceur="Saoul")], [EffetEtat(EtatModDegPer("Vulnérabilité", 0, 2, 117), etat_requis_lanceur="Saoul")], 5, 4, 2, 0, 1, "ligne", True, description="""Augmente les dommages reçus par la cible pendant 2 tours.
    L'état Saoul est nécessaire.""", chaine=True),

        Sort.Sort("Vulnérabilité", 103, 3, 1, 5, [EffetEtat(EtatModDegPer("Vulnérabilité", 0, 2, 115), etat_requis_lanceur="Saoul")], [EffetEtat(EtatModDegPer("Vulnérabilité", 0, 2, 117), etat_requis_lanceur="Saoul")], 5, 4, 2, 0, 1, "ligne", True, description="""Augmente les dommages reçus par la cible pendant 2 tours.
    L'état Saoul est nécessaire.""", chaine=True),

        Sort.Sort("Vulnérabilité", 143, 3, 1, 7, [EffetEtat(EtatModDegPer("Vulnérabilité", 0, 2, 115), etat_requis_lanceur="Saoul")], [EffetEtat(EtatModDegPer("Vulnérabilité", 0, 2, 117), etat_requis_lanceur="Saoul")], 5, 4, 2, 0, 1, "ligne", True, description="""Augmente les dommages reçus par la cible pendant 2 tours.
    L'état Saoul est nécessaire.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Prohibition", 165, 2, 0, 5, [EffetEtat(EtatModSoinPer('Insoignable', 0, 1, 0), etat_requis_lanceur="Saoul"), EffetEtat(EtatModDegPer("Prohibition", 0, 1, 0, "melee"))], [], 0, 1, 1, 3, 0, "ligne", True, description="""Applique l'état Insoignable sur la cible et la rend invulnérable aux dommages de mélée.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Vague à Lame", 56, 4, 1, 3, [EffetDegats(31, 33, "Eau", zone=Zones.TypeZoneLignePerpendiculaire(1), etat_requis_lanceur="Sobre", cible_non_requise=True)], [EffetDegats(37, 39, "Eau", zone=Zones.TypeZoneLignePerpendiculaire(1), etat_requis_lanceur="Sobre", cible_non_requise=True)], 25, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Eau.""", chaine=True),

        Sort.Sort("Vague à Lame", 112, 4, 1, 4, [EffetDegats(36, 38, "Eau", zone=Zones.TypeZoneLignePerpendiculaire(1), etat_requis_lanceur="Sobre", cible_non_requise=True)], [EffetDegats(42, 44, "Eau", zone=Zones.TypeZoneLignePerpendiculaire(1), etat_requis_lanceur="Sobre", cible_non_requise=True)], 25, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Eau.""", chaine=True),

        Sort.Sort("Vague à Lame", 147, 4, 1, 5, [EffetDegats(41, 43, "Eau", zone=Zones.TypeZoneLignePerpendiculaire(1), etat_requis_lanceur="Sobre", cible_non_requise=True)], [EffetDegats(47, 49, "Eau", zone=Zones.TypeZoneLignePerpendiculaire(1), etat_requis_lanceur="Sobre", cible_non_requise=True)], 25, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Eau.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Gnôle", 170, 4, 1, 5, [EffetDegatsSelonPMUtilises(53, 57, "Eau")], [EffetDegatsSelonPMUtilises(61, 65, "Eau")], 15, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Eau.
    Moins le lanceur a utilisé de PM pendant son tour de jeu, plus les dommages occasionnés sont importants.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Colère de Zatoïshwan", 62, 3, 0, 0, [EffetEtatSelf(Etat("Saoul", 0, 2), etat_requis="!Saoul|!Karcham|!Chamrak"), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "pui", 100)), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "do", 5)), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "PA", 2))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Applique l'état Saoul.
    Augmente les dommages et les PA du lanceur.""", chaine=True),

        Sort.Sort("Colère de Zatoïshwan", 116, 3, 0, 0, [EffetEtatSelf(Etat("Saoul", 0, 2), etat_requis="!Saoul|!Karcham|!Chamrak"), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "pui", 150)), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "do", 10)), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "PA", 2))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Applique l'état Saoul.
    Augmente les dommages et les PA du lanceur.""", chaine=True),

        Sort.Sort("Colère de Zatoïshwan", 153, 3, 0, 0, [EffetEtatSelf(Etat("Saoul", 0, 2), etat_requis="!Saoul|!Karcham|!Chamrak"), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "pui", 200)), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "do", 15)), EffetEtat(EtatBoostCaracFixe("Colère de Zatoïshwan", 0, 2, "PA", 2))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Applique l'état Saoul.
    Augmente les dommages et les PA du lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Fermentation", 175, 3, 0, 0, [EffetEtat(EtatBouclierPerLvl("Fermentation", 0, 1, 240), etat_requis_lanceur="Saoul"), EffetEtat(EtatBouclierPerLvl("Fermentation", 1, 1, 240), etat_requis_lanceur="Saoul")], [], 0, 1, 1, 2, 0, "cercle", False, description="""Applique un bouclier pour le tour en cours et un second au tour suivant.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Flasque Explosive", 69, 2, 2, 4, [EffetDegats(24, 28, "Feu", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, etat_requis_lanceur="Sobre")], [EffetDegats(29, 33, "Feu", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, etat_requis_lanceur="Sobre")], 25, 1, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu en zone.""", chaine=True),

        Sort.Sort("Flasque Explosive", 122, 2, 2, 4, [EffetDegats(29, 33, "Feu", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, etat_requis_lanceur="Sobre")], [EffetDegats(34, 38, "Feu", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, etat_requis_lanceur="Sobre")], 25, 1, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu en zone.""", chaine=True),

        Sort.Sort("Flasque Explosive", 162, 2, 2, 5, [EffetDegats(34, 38, "Feu", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, etat_requis_lanceur="Sobre")], [EffetDegats(39, 43, "Feu", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, etat_requis_lanceur="Sobre")], 25, 1, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu en zone.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Absinthe", 180, 3, 1, 6, [EffetDegats(25, 29, "Feu", etat_requis_lanceur="Saoul")], [EffetDegats(30, 34, "Feu", etat_requis_lanceur="Saoul")], 5, 3, 2, 0, 0, "ligne", False, description="""Occasionne des dommages Feu sans ligne de vue.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Vertige", 77, 2, 1, 4, [EffetLance(cible_non_requise=True, cibles_possibles=""), EffetAttire(2, source="CaseCible", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetEtat(EtatBoostCaracFixe("Vertige", 0, 1, "tacle", 30), cible_non_requise=True)], [], 0, 2, 99, 0, 0, "ligne", True, description="""Lance l'entité portée et augmente son tacle.
    Attire les entités alignées avec la cellule ciblée.""", chaine=True),

        Sort.Sort("Vertige", 128, 2, 1, 5, [EffetLance(cible_non_requise=True, cibles_possibles=""), EffetAttire(3, source="CaseCible", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetEtat(EtatBoostCaracFixe("Vertige", 0, 1, "tacle", 40), cible_non_requise=True)], [], 0, 2, 99, 0, 0, "ligne", True, description="""Lance l'entité portée et augmente son tacle.
    Attire les entités alignées avec la cellule ciblée.""", chaine=True),

        Sort.Sort("Vertige", 172, 2, 1, 6, [EffetLance(cible_non_requise=True, cibles_possibles=""), EffetAttire(3, source="CaseCible", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetEtat(EtatBoostCaracFixe("Vertige", 0, 1, "tacle", 50), cible_non_requise=True)], [], 0, 2, 99, 0, 0, "ligne", True, description="""Lance l'entité portée et augmente son tacle.
    Attire les entités alignées avec la cellule ciblée.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Cascade", 185, 2, 1, 5, [EffetLance(cible_non_requise=True, cibles_possibles="", etat_requis_lanceur="Sobre"), EffetAttire(2, source="CaseCible", cible="Lanceur", etat_requis_lanceur="Sobre")], [], 0, 2, 99, 0, 0, "ligne", True, description="""Le lanceur jette la cible et s'en rapproche.
    Nécessite l'état Sobre.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Pandatak", 84, 4, 1, 6, [EffetDegats(36, 40, "Terre", zone=Zones.TypeZoneLigne(3), etat_requis_lanceur="Sobre", cible_non_requise=True)], [EffetDegats(43, 47, "Terre", zone=Zones.TypeZoneLigne(3), etat_requis_lanceur="Sobre", cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Terre sur plusieurs cases en ligne.""", chaine=True),

        Sort.Sort("Pandatak", 134, 4, 1, 6, [EffetDegats(42, 46, "Terre", zone=Zones.TypeZoneLigne(3), etat_requis_lanceur="Sobre", cible_non_requise=True)], [EffetDegats(49, 53, "Terre", zone=Zones.TypeZoneLigne(3), etat_requis_lanceur="Sobre", cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Terre sur plusieurs cases en ligne.""", chaine=True),

        Sort.Sort("Pandatak", 178, 4, 1, 6, [EffetDegats(48, 52, "Terre", zone=Zones.TypeZoneLigne(3), etat_requis_lanceur="Sobre", cible_non_requise=True)], [EffetDegats(55, 59, "Terre", zone=Zones.TypeZoneLigne(3), etat_requis_lanceur="Sobre", cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Terre sur plusieurs cases en ligne.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Bistouille", 190, 4, 0, 0, [EffetVolDeVie(38, 42, "Terre", zone=Zones.TypeZoneCroix(1, 1), etat_requis_lanceur="Saoul")], [EffetVolDeVie(42, 46, "Terre", zone=Zones.TypeZoneCroix(1, 1), etat_requis_lanceur="Saoul")], 25, 2, 99, 0, 0, "cercle", False, description="""Vole de la vie dans l'élément Terre en zone autour du lanceur.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Pandanlku", 92, 2, 0, 2, [EffetEtat(EtatBoostCaracFixe("Pandanlku", 0, 2, "PM", 3), etat_requis_lanceur="Saoul")], [], 0, 1, 1, 6, 1, "cercle", True, description="""Augmente les PM de la cible.
    Nécessite l'état Saoul.""", chaine=True),

        Sort.Sort("Pandanlku", 141, 2, 0, 4, [EffetEtat(EtatBoostCaracFixe("Pandanlku", 0, 2, "PM", 3), etat_requis_lanceur="Saoul")], [], 0, 1, 1, 5, 1, "cercle", True, description="""Augmente les PM de la cible.
    Nécessite l'état Saoul.""", chaine=True),

        Sort.Sort("Pandanlku", 187, 2, 0, 6, [EffetEtat(EtatBoostCaracFixe("Pandanlku", 0, 2, "PM", 4), etat_requis_lanceur="Saoul")], [], 0, 1, 1, 4, 1, "cercle", True, description="""Augmente les PM de la cible.
    Nécessite l'état Saoul.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Brancard", 195, 2, 1, 4, [EffetEtat(EtatEffetSiRetraitEtat("Brancard", 0, 1, EffetSoinPerPVMax(10), "Brancard", "Brancard", "porteur"), zone=Zones.TypeZoneLigneJusque(), cibles_possibles="Allies|Ennemis", cible_non_requise=True, etat_requis_lanceur="Sobre"), EffetRetireEtat("Brancard", zone=Zones.TypeZoneInfini(), cible_non_requise=True, etat_requis_lanceur="Sobre"), EffetLance(cible_non_requise=True, cibles_possibles="", etat_requis_lanceur="Sobre")], [], 0, 2, 99, 0, 0, "ligne", False, description="""Jette la cible jusqu'à la cellule ciblée. La cible est soignée en fonction du nombre d'entités survolées.
    Nécessite l'état Sobre.""", chaine=False)
    ]))
    return sorts
    