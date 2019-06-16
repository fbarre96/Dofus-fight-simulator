"""@summary: Rassemble les sorts du Sram
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetEtat import EffetEtat, EffetEtatSelf, EffetRetireEtat, EffetSetDureeEtat
from Effets.EffetDegats import EffetDegats, EffetVolDeVie
from Effets.EffetTue import EffetTue
from Effets.EffetSoin import EffetSoinSelonSubit
from Effets.EffetPousser import EffetAttire, EffetPousser, EffetPousserJusque
from Effets.EffetRet import EffetRetPM
from Effets.EffetGlyphe import EffetGlyphe
from Effets.EffetPiege import EffetPiege
from Effets.EffetEntiteLanceSort import EffetEntiteLanceSort
from Effets.EffetTp import EffetEchangePlace
from Effets.EffetInvoque import EffetInvoque, EffetDouble
import Zones
from Etats.EtatEffet import EtatEffetSiPiegeDeclenche, EtatEffetSiSubit, EtatEffetDebutTour, EtatEffetFinTour
from Etats.EtatBoostBaseDeg import EtatBoostBaseDeg
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatBoostSortCarac import EtatBoostSortCarac
from Etats.Etat import Etat
from Etats.EtatActiveSort import EtatActiveSort
import Personnages


def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    sortsDebutCombat.append(
        Sort.Sort("Chausse-Trappe Boost", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiPiegeDeclenche("Chausse-Trappe Boost", 0, -1, EffetEtatSelf(EtatBoostBaseDeg(
            "Chausse-Trappe", 0, -1, "Chausse-Trappe", 8), cumulMax=5), "Chausse-Trappe Boost", "porteur", "porteur"))], [], 0, 99, 99, 0, 0, "cercle", False, description="""""", chaine=False),
    )
    sortsDebutCombat.append(
        Sort.Sort("Traquenard Boost", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiPiegeDeclenche("Traquenard Boost", 0, -1, EffetEtatSelf(EtatBoostSortCarac(
            "Traquenard", 0, -1, "Traquenard", "POMax", 1), cumulMax=5), "Traquenard Boost", "porteur", "porteur"))], [], 0, 99, 99, 0, 0, "cercle", False, description="""""", chaine=False),
    )
    sortsDebutCombat.append(
        Sort.Sort("Injection Toxique Boost", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiPiegeDeclenche("Injection Toxique Boost", 0, -1, EffetEtatSelf(EtatBoostSortCarac("Injection Toxique", 0, -1,
                                                                                                                                                                     "Injection Toxique", "nbTourEntreDeux", -1), cumulMax=5), "Injection Toxique Boost", "porteur", "porteur"))], [], 0, 99, 99, 0, 0, "cercle", False, description="""""", chaine=False),
    )
    sortsDebutCombat.append(
        Sort.Sort("Perfidie Boost", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiPiegeDeclenche("Perfidie Boost", 0, -1, EffetEtatSelf(EtatBoostSortCarac(
            "Perfidie", 0, -1, "Perfidie", "coutPA", -1), cumulMax=5), "Perfidie Boost", "porteur", "porteur"))], [], 0, 99, 99, 0, 0, "cercle", False, description="""""", chaine=False),
    )
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    sorts = []
    activationPiegeSournois = [EffetDegats(26, 28, "feu", zone=Zones.TypeZoneCercle(
        1), cible_non_requise=True, piege=True), EffetAttire(1, "CaseCible", zone=Zones.TypeZoneCercle(1), cible_non_requise=True)]
    activationPiegePerfide = [EffetAttire(
        3, "CaseCible", zone=Zones.TypeZoneCroix(3), cible_non_requise=True, piege=True)]
    activationPiegeFangeux = [EffetEtat(EtatEffetSiSubit('Etat temporaire', 0, 1, EffetSoinSelonSubit(50, zone=Zones.TypeZoneCercle(
        2), cibles_possibles="Allies"), "Piège Fangeux", "lanceur", "cible")), EffetDegats(33, 37, "Eau", piege=True, cible_non_requise=True), EffetRetireEtat('Etat temporaire')]
    activationPiegeDeMasse = [EffetDegats(
        34, 38, "Terre", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, piege=True)]
    activationPiegeEmpoisonne = [EffetEtat(EtatEffetDebutTour("Piège Empoisonné", 0, 3, EffetDegats(
        10, 10, "Air"), "Piège Empoisonné", "lanceur"), zone=Zones.TypeZoneCroix(1), cible_non_requise=True, piege=True)]
    activationPiegeAFragmentation = [EffetDegats(18, 22, "feu", zone=Zones.TypeZoneCercle(0), cible_non_requise=True, piege=True), EffetDegats(33, 37, "feu", zone=Zones.TypeZoneAnneau(
        1), cible_non_requise=True, piege=True), EffetDegats(43, 47, "feu", zone=Zones.TypeZoneAnneau(2), cible_non_requise=True, piege=True), EffetDegats(58, 62, "feu", zone=Zones.TypeZoneAnneau(3), cible_non_requise=True, piege=True)]
    activationPiegeDimmobilisation = [EffetRetPM(
        4, 3, zone=Zones.TypeZoneCercle(3), cible_non_requise=True, piege=True)]
    activationPiegeDeDerive = [EffetPousser(
        2, "CaseCible", zone=Zones.TypeZoneCroixDiagonale(1), cible_non_requise=True, piege=True)]
    activationGlypheInsidieuse = Sort.Sort("Piège insidieux : poison fin de tour", 0, 0, 0, 3, [EffetEtat(EtatEffetFinTour("Piège insidieux : poison fin de tour", 0, 1, EffetDegats(
        34, 38, "Air"), "Piège insidieux : poison fin de tour", "lanceur"), cumulMax=1, cibles_possibles="Ennemis")], [], 0, 99, 99, 0, 0, "cercle", False)
    sortieGlypheInsidieuse = Sort.Sort("Piège insidieux: Sortie", 0, 0, 0, 99, [EffetRetireEtat(
        "Piège insidieux : poison fin de tour", cibles_possibles="Ennemis", cible_non_requise=True)], [], 0, 99, 99, 0, 0, "cercle", False)
    activationPiegeInsidieux = [EffetGlyphe(activationGlypheInsidieuse, activationGlypheInsidieuse, sortieGlypheInsidieuse,
                                            1, "Piège insidieux", (0, 200, 0), zone=Zones.TypeZoneCercle(2), cible_non_requise=True, piege=True)]
    activationPiegeRepulsif = [EffetDegats(12, 12, "air", zone=Zones.TypeZoneCercle(
        1), cible_non_requise=True, piege=True), EffetPousser(2, "CaseCible", zone=Zones.TypeZoneCercle(1), cible_non_requise=True)]
    activationPiegeRepoussant = [EffetPousser(
        2, "CaseCible", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, piege=True)]
    activationPiegeDeProximite = [EffetDegats(
        43, 47, "Air", zone=Zones.TypeZoneCercle(2), cible_non_requise=True, piege=True)]
    activationCalamite = [EffetVolDeVie(38, 42, "Eau", zone=Zones.TypeZoneCarre(1), cible_non_requise=True, piege=True), EffetEtat(
        EtatBoostCaracFixe("Calamité", 0, 1, "fuite", -30), zone=Zones.TypeZoneCarre(1), cible_non_requise=True, piege=True)]
    activationPiegeFuneste = [EffetEtatSelf(EtatBoostBaseDeg("Etat temporaire piège funeste", 0, 1, "Piège Funeste", 30), zone=Zones.TypeZoneCercle(
        2), cibles_possibles="Ennemis"), EffetDegats(28, 32, "Terre"), EffetRetireEtat("Etat temporaire piège funeste", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")]
    activationPiegeMortel = [EffetDegats(53, 57, "Terre")]
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Sournoiserie", 1, 3, 1, 4, [EffetDegats(14, 16, "Terre")], [EffetDegats(
            18, 20, "Terre")], 5, 99, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Sournoiserie", 25, 3, 1, 4, [EffetDegats(17, 19, "Terre")], [EffetDegats(
            21, 23, "Terre")], 5, 99, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Sournoiserie", 52, 3, 1, 5, [EffetDegats(20, 22, "Terre")], [EffetDegats(
            24, 26, "Terre")], 5, 99, 3, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Chausse-Trappe", 110, 4, 1, 4, [EffetDegats(30, 34, "Terre"), EffetRetireEtat("Chausse-Trappe", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], [EffetDegats(34, 38, "Terre"), EffetRetireEtat("Chausse-Trappe", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre. Chaque piège déclenché augmente les dommages de Chausse-Trape.
    Le bonus de dommages disparaît quand le sort est lancé.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège Sournois", 1, 3, 1, 4, [EffetPiege(Zones.TypeZoneCroix(1), activationPiegeSournois, "Piège sournois", (255, 0, 0), cible_non_requise=True)], [
        ], 0, 1, 99, 0, 1, "cercle", False, description="""Occasionne des dommages Feu et attire.""", chaine=True),

        Sort.Sort("Piège Sournois", 30, 3, 1, 6, [EffetPiege(Zones.TypeZoneCroix(1), activationPiegeSournois, "Piège sournois", (255, 0, 0), cible_non_requise=True)], [
        ], 0, 1, 99, 0, 1, "cercle", False, description="""Occasionne des dommages Feu et attire.""", chaine=True),

        Sort.Sort("Piège Sournois", 60, 3, 1, 8, [EffetPiege(Zones.TypeZoneCroix(1), activationPiegeSournois, "Piège sournois", (255, 0, 0), cible_non_requise=True)], [
        ], 0, 1, 99, 0, 1, "cercle", False, description="""Occasionne des dommages Feu et attire.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège Perfide", 105, 2, 1, 7, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegePerfide, "Piège Perfide", (240, 0, 0), cible_non_requise=True)], [
        ], 0, 1, 99, 0, 1, "cercle", False, description="""Pose un piège mono-cellule qui attire en zone.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Invisibilité", 1, 2, 0, 0, [EffetEtat(Etat("Invisible", 0, 3)), EffetEtat(EtatBoostCaracFixe(
            "Invibilité_PM", 0, 4, "PM", 1))], [], 0, 1, 1, 7, 0, "cercle", False, description="""Rend invisible.""", chaine=True),

        Sort.Sort("Invisibilité", 20, 2, 0, 0, [EffetEtat(Etat("Invisible", 0, 3)), EffetEtat(EtatBoostCaracFixe(
            "Invibilité_PM", 0, 4, "PM", 1))], [], 0, 1, 1, 6, 0, "cercle", False, description="""Rend invisible.""", chaine=True),

        Sort.Sort("Invisibilité", 40, 2, 0, 0, [EffetEtat(Etat("Invisible", 0, 3)), EffetEtat(EtatBoostCaracFixe(
            "Invibilité_PM", 0, 4, "PM", 2))], [], 0, 1, 1, 6, 0, "cercle", False, description="""Rend invisible.""", chaine=True)
    ]))
    activationBrume = Sort.Sort("Activation Brume", 0, 0, 0, 3, [EffetEtat(Etat(
        "Invisible", 0, 2), cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    sortieBrume = Sort.Sort("Brume: Sortie", 0, 0, 0, 99, [EffetRetireEtat(
        "Invisible", cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Brume", 101, 3, 1, 3, [EffetGlyphe(activationBrume, activationBrume, sortieBrume, 2, "Brume", (255, 0, 255), zone=Zones.TypeZoneCercle(
            3), cible_non_requise=True)], [], 0, 1, 1, 4, 0, "cercle", True, description="""Pose un glyphe-aura qui rend invisible les alliés présents dans la zone.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Poison insidieux", 3, 3, 1, 4, [EffetEtat(EtatEffetDebutTour("Poison insidieux", 0, 2, EffetDegats(6, 7, "Air"), "Poison insidieux", "lanceur"))], [EffetEtat(EtatEffetDebutTour(
            "Poison insidieux", 0, 2, EffetDegats(8, 9, "Air"), "Poison insidieux", "lanceur"))], 15, 99, 1, 0, 1, "ligne", False, description="""Empoisonne la cible pendant 2 tours en occasionnant des dommages Air.""", chaine=True),

        Sort.Sort("Poison insidieux", 35, 3, 1, 4, [EffetEtat(EtatEffetDebutTour("Poison insidieux", 0, 2, EffetDegats(8, 9, "Air"), "Poison insidieux", "lanceur"))], [EffetEtat(EtatEffetDebutTour(
            "Poison insidieux", 0, 2, EffetDegats(10, 11, "Air"), "Poison insidieux", "lanceur"))], 15, 99, 1, 0, 1, "ligne", False, description="""Empoisonne la cible pendant 2 tours en occasionnant des dommages Air.""", chaine=True),

        Sort.Sort("Poison insidieux", 67, 3, 1, 4, [EffetEtat(EtatEffetDebutTour("Poison insidieux", 0, 2, EffetDegats(10, 11, "Air"), "Poison insidieux", "lanceur"))], [EffetEtat(EtatEffetDebutTour(
            "Poison insidieux", 0, 2, EffetDegats(12, 13, "Air"), "Poison insidieux", "lanceur"))], 15, 99, 1, 0, 1, "ligne", False, description="""Empoisonne la cible pendant 2 tours en occasionnant des dommages Air.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Toxines", 115, 3, 1, 7, [
            EffetRetireEtat("Toxines", zone=Zones.TypeZoneInfini()),
            EffetEtat(EtatEffetDebutTour("Toxines", 0, 2, EffetDegats(
                10, 11, "Air"), "Toxines", "lanceur")),
            EffetEtatSelf(EtatEffetSiPiegeDeclenche("Toxines", 0, 2, EffetEtatSelf(EtatBoostBaseDeg(
                "Toxines", 0, -1, "Toxines", 10)), "Toxines", "lanceur", "lanceur"), etat_requis_cibles="Toxines"),
            EffetEtatSelf(EtatEffetSiPiegeDeclenche("Toxines", 0, 2, EffetSetDureeEtat(
                "Toxines", 0, 2, zone=Zones.TypeZoneInfini()), "Toxines", "lanceur", "declencheur"), etat_requis_cibles="Toxines")
        ], [], 0, 1, 1, 2, 1, "cercle", True, description="""L'ennemi ciblé subit un poison Air pendant 2 tours.
    Si la cible subit un piège alors qu'elle est sous les effets de Toxines, les dommages du poison sont augmentés et sa durée est réinitialisée.
    Il ne peut y avoir qu'un seul ennemi sous l'effet de Toxines.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Fourvoiement", 6, 4, 0, 0, [
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "erosion", 10),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", -30),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", 30)),
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", -30),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", 30)),
            EffetDegats(11, 14, "Air", cibles_exclues="Lanceur",
                        zone=Zones.TypeZoneCroix(1)),
            EffetDegats(11, 14, "Terre", cibles_exclues="Lanceur",
                        zone=Zones.TypeZoneCroix(1))
        ],
                  [
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "erosion", 10),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", -40),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", 40)),
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", -40),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", 40)),
                      EffetDegats(15, 18, "Air", cibles_exclues="Lanceur",
                                  zone=Zones.TypeZoneCroix(1)),
                      EffetDegats(15, 18, "Terre", cibles_exclues="Lanceur",
                                  zone=Zones.TypeZoneCroix(1))],
                  5, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Air et Terre.
    Vole de l'Agilité et de la Force.
    Applique de l'érosion.""", chaine=True),

        Sort.Sort("Fourvoiement", 42, 4, 0, 0, [
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "erosion", 10),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", -40),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", 40)),
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", -40),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", 40)),
            EffetDegats(14, 17, "Air", zone=Zones.TypeZoneCroix(1),
                        cibles_exclues="Lanceur"),
            EffetDegats(14, 17, "Terre", zone=Zones.TypeZoneCroix(
                1), cibles_exclues="Lanceur")
        ],
                  [
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "erosion", 10),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", -50),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", 50)),
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", -50),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", 50)),
                      EffetDegats(18, 21, "Air", zone=Zones.TypeZoneCroix(1),
                                  cibles_exclues="Lanceur"),
                      EffetDegats(18, 21, "Terre", zone=Zones.TypeZoneCroix(1),
                                  cibles_exclues="Lanceur")],
                  5, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Air et Terre.
    Vole de l'Agilité et de la Force.
    Applique de l'érosion.""", chaine=True),

        Sort.Sort("Fourvoiement", 74, 4, 0, 0, [
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "erosion", 10),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", -50),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", 50)),
            EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", -50),
                      cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
            EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", 50)),
            EffetDegats(17, 20, "Air", zone=Zones.TypeZoneCroix(1),
                        cibles_exclues="Lanceur"),
            EffetDegats(17, 20, "Terre", zone=Zones.TypeZoneCroix(
                1), cibles_exclues="Lanceur")
        ],
                  [
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "erosion", 10),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", -60),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "agi", 60)),
                      EffetEtat(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", -60),
                                cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                      EffetEtatSelf(EtatBoostCaracFixe("Fourvoiement", 0, 3, "fo", 60)),
                      EffetDegats(21, 24, "Air", zone=Zones.TypeZoneCroix(1),
                                  cibles_exclues="Lanceur"),
                      EffetDegats(21, 24, "Terre", zone=Zones.TypeZoneCroix(1),
                                  cibles_exclues="Lanceur")],
                  5, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Air et Terre.
    Vole de l'Agilité et de la Force.
    Applique de l'érosion.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Pillage", 120, 3, 1, 1, [EffetEtat(EtatEffetSiSubit('Etat temporaire', 0, 1, EffetSoinSelonSubit(50, zone=Zones.TypeZoneCercle(3), cibles_possibles="Allies"), "Pillage", "lanceur", "cible")), EffetDegats(34, 38, "Eau"), EffetRetireEtat('Etat temporaire')], [EffetEtat(EtatEffetSiSubit('Etat temporaire', 0, 1, EffetSoinSelonSubit(50, zone=Zones.TypeZoneCercle(3)), "Pillage", "lanceur", "cible")), EffetDegats(40, 44, "Eau"), EffetRetireEtat('Etat temporaire')], 15, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Eau.
        50% des dommages sont distribués sous forme de soin aux alliés à 3 cellules ou moins de la cible.
        N'affecte pas le lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Coup Sournois", 9, 3, 1, 3, [EffetDegats(18, 21, "Feu"), EffetPousser(2)], [EffetDegats(22, 25, "Feu"), EffetPousser(2)], 15, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Feu sur les ennemis.
    Pousse la cible.""", chaine=True),

        Sort.Sort("Coup Sournois", 47, 3, 1, 3, [EffetDegats(22, 25, "Feu"), EffetPousser(2)], [EffetDegats(26, 29, "Feu"), EffetPousser(2)], 15, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Feu sur les ennemis.
    Pousse la cible.""", chaine=True),

        Sort.Sort("Coup Sournois", 87, 3, 1, 4, [EffetDegats(26, 29, "Feu"), EffetPousser(3)], [EffetDegats(31, 34, "Feu"), EffetPousser(3)], 15, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Feu sur les ennemis.
    Pousse la cible.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Coupe-gorge", 125, 4, 1, 7, [EffetDegats(34, 38, "Feu"), EffetEtatSelf(EtatBoostCaracFixe("Coupe-gorge", 0, 2, "doPiegesPui", 250))], [EffetDegats(40, 44, "Feu"), EffetEtatSelf(
            EtatBoostCaracFixe("Coupe-gorge", 0, 2, "doPiegesPui", 250))], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Feu et augmente la puissance des pièges.""", chaine=True)
    ]))
    activationDoubleComplot2 = Sort.Sort("Complot", 0, 0, 0, 99, [EffetEchangePlace(zone=Zones.TypeZoneInfini(), cibles_possibles="Invocateur"), EffetTue(
        zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], [], 0, 1, 1, 0, 0, "cercle", False, description="Echange de place avec son invocateur, tue l'invocation")
    activationDoubleComplot = Sort.Sort("Complot", 0, 0, 0, 99, [EffetEtatSelf(EtatEffetFinTour("Explosion Double", 0, 2, EffetEntiteLanceSort(
        "Double", activationDoubleComplot2), "Explosion Double", "lanceur"))], [], 0, 1, 1, 0, 0, "cercle", False, description="Echange de place avec son invocateur, tue l'invocation")
    activationComploteurComplot2 = Sort.Sort("Complot", 0, 0, 0, 99, [EffetDegats(39, 41, "Neutre", zone=Zones.TypeZoneCercleSansCentre(1)), EffetTue(
        zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], [], 0, 1, 1, 0, 0, "cercle", False, description="Echange de place avec son invocateur, tue l'invocation", chaine=False)
    activationComploteurComplot = Sort.Sort("Complot", 0, 0, 0, 99, [EffetEtatSelf(EtatEffetFinTour("Explosion Comploteur", 0, 2, EffetEntiteLanceSort(
        "Comploteur", activationComploteurComplot2), "Explosion Comploteur", "lanceur"))], [], 0, 1, 1, 0, 0, "cercle", False, description="Echange de place avec son invocateur, tue l'invocation")
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Double", 13, 3, 1, 2, [EffetInvoque("Double", True, cibles_possibles="", cible_non_requise=True), EffetDouble()], [], 0, 1, 1, 6, 0, "ligne", True, description="""Invoque un double contrôlable qui possède les mêmes caractéristiques que l'invocateur.
    N'attaque pas et meurt au bout de 2 tours en échangeant de place avec son invocateur.""", chaine=True),

        Sort.Sort("Double", 54, 3, 1, 2, [EffetInvoque("Double", True, cibles_possibles="", cible_non_requise=True), EffetDouble()], [], 0, 1, 1, 5, 0, "ligne", True, description="""Invoque un double contrôlable qui possède les mêmes caractéristiques que l'invocateur.
    N'attaque pas et meurt au bout de 2 tours en échangeant de place avec son invocateur.""", chaine=True),

        Sort.Sort("Double", 94, 3, 1, 2, [EffetInvoque("Double", True, cibles_possibles="", cible_non_requise=True), EffetDouble(), EffetEtat(EtatActiveSort("Complot", 2, 1, activationDoubleComplot))], [], 0, 1, 1, 4, 0, "ligne", True, description="""Invoque un double contrôlable qui possède les mêmes caractéristiques que l'invocateur.
    N'attaque pas et meurt au bout de 2 tours en échangeant de place avec son invocateur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Comploteur", 130, 3, 1, 2, [EffetInvoque("Comploteur", True, cibles_possibles="", cible_non_requise=True), EffetDouble(), EffetEtat(EtatActiveSort("Complot", 2, 1, activationComploteurComplot)), EffetEtat(EtatEffetSiPiegeDeclenche("Comploteur", 0, -1, EffetEtatSelf(EtatBoostBaseDeg("ComplotBoost", 0, -1, "Complot", 14), cumulMax=4), "Complot", "porteur", "porteur"))], [], 0, 1, 1, 4, 0, "cercle", True, description="""Invoque un Double contrôlable.
    Chaque piège déclenché augmente la Puissance du Double.
    Il meurt après 2 tours.
    Il occasionne des dommages Neutre en zone autour de lui lorsqu'il meurt.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège Fangeux", 17, 3, 1, 4, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeFangeux, "Piège Fangeux", (0, 0, 255), cible_non_requise=True)], [], 0, 1, 99, 0, 1, "cercle", True, description="""Pose un piège qui occasionne des dommages Eau.
    Les alliés à proximité de la cible sont soignés à hauteur de 50% des dommages occasionnés.""", chaine=True),

        Sort.Sort("Piège Fangeux", 58, 3, 1, 6, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeFangeux, "Piège Fangeux", (0, 0, 255), cible_non_requise=True)], [], 0, 1, 99, 0, 1, "cercle", True, description="""Pose un piège qui occasionne des dommages Eau.
    Les alliés à proximité de la cible sont soignés à hauteur de 50% des dommages occasionnés.""", chaine=True),

        Sort.Sort("Piège Fangeux", 102, 3, 1, 8, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeFangeux, "Piège Fangeux", (0, 0, 255), cible_non_requise=True)], [], 0, 2, 99, 0, 1, "cercle", True, description="""Pose un piège qui occasionne des dommages Eau.
    Les alliés à proximité de la cible sont soignés à hauteur de 50% des dommages occasionnés.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Larcin", 135, 4, 0, 0, [EffetEtat(EtatBoostCaracFixe("Larcin", 0, 2, "cha", -80), cibles_exclues="Lanceur", zone=Zones.TypeZoneCroixDiagonale(1)), EffetEtatSelf(EtatBoostCaracFixe("Larcin", 0, 2, "cha", 80), cibles_exclues="Lanceur", zone=Zones.TypeZoneCroixDiagonale(1)), EffetDegats(40, 44, "Eau", cibles_exclues="Lanceur", zone=Zones.TypeZoneCroixDiagonale(1))], [EffetEtat(EtatBoostCaracFixe(
            "Larcin", 0, 2, "cha", -100), cibles_exclues="Lanceur", zone=Zones.TypeZoneCroixDiagonale(1)), EffetEtatSelf(EtatBoostCaracFixe("Larcin", 0, 2, "cha", 100), cibles_exclues="Lanceur", zone=Zones.TypeZoneCroixDiagonale(1)), EffetDegats(44, 48, "Eau", cibles_exclues="Lanceur", zone=Zones.TypeZoneCroixDiagonale(1))], 25, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Eau et vole de la Chance.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège de Masse", 22, 4, 1, 3, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeDeMasse, "Piège de Masse", (50, 50, 30), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 1, "cercle", False, description="""Pose un piège mono-cellule qui occasionne des dommages Terre en zone.""", chaine=True),

        Sort.Sort("Piège de Masse", 65, 4, 1, 4, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeDeMasse, "Piège de Masse", (50, 50, 30), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 1, "cercle", False, description="""Pose un piège mono-cellule qui occasionne des dommages Terre en zone.""", chaine=True),

        Sort.Sort("Piège de Masse", 108, 4, 1, 5, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeDeMasse, "Piège de Masse", (50, 50, 30), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 1, "cercle", False, description="""Pose un piège mono-cellule qui occasionne des dommages Terre en zone.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Traquenard", 140, 3, 1, 1, [EffetDegats(30, 34, "Terre"), EffetRetireEtat("Traquenard")], [EffetDegats(33, 37, "Terre"), EffetRetireEtat("Traquenard")], 5, 3, 2, 0, 0, "ligne", False, description="""Occasionne des dommages Terre. Chaque piège déclenché augmente la portée de Traquenard.
    Le bonus de portée disparaît quand le sort est lancé.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Cruauté", 27, 3, 1, 5, [EffetDegats(12, 14, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Cruauté", 0, 1, "PM", 1))], [EffetDegats(16, 18, "Eau"), EffetEtatSelf(
            EtatBoostCaracFixe("Cruauté", 0, 1, "PM", 1))], 5, 2, 99, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et augmente les PM du lanceur.""", chaine=True),

        Sort.Sort("Cruauté", 72, 3, 1, 6, [EffetDegats(15, 17, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Cruauté", 0, 1, "PM", 1))], [EffetDegats(19, 21, "Eau"), EffetEtatSelf(
            EtatBoostCaracFixe("Cruauté", 0, 1, "PM", 1))], 5, 2, 99, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et augmente les PM du lanceur.""", chaine=True),

        Sort.Sort("Cruauté", 118, 3, 1, 7, [EffetDegats(18, 20, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Cruauté", 0, 1, "PM", 1))], [EffetDegats(22, 24, "Eau"), EffetEtatSelf(
            EtatBoostCaracFixe("Cruauté", 0, 1, "PM", 1))], 5, 2, 99, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et augmente les PM du lanceur.""", chaine=True)
    ]))
    activationGuetApens = Sort.Sort("Activation Guet-apens", 145, 0, 0, 99, [EffetAttire(2, "Lanceur", "JoueurCaseEffet", zone=Zones.TypeZoneInfini(
    ), etat_requis_cibles="Guet-Apens", consomme_etat=True)], [], 0, 99, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Feu et attire la cible vers le Double.""", chaine=True)
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Guet-apens", 145, 3, 1, 5, [EffetDegats(30, 34, "Feu"), EffetEtat(Etat("Guet-Apens", 0, -1)), EffetEntiteLanceSort("Double|Comploteur", activationGuetApens)], [EffetDegats(34, 38, "Feu"), EffetAttire(
            2, "JoueurCaseEffet", "Lanceur", zone=Zones.TypeZoneInfini(), cibles_possibles="Double|Comploteur")], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Feu et attire la cible vers le Double.""", chaine=True)
    ]))

    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège Empoisonné", 32, 3, 1, 3, [EffetPiege(Zones.TypeZoneCroix(1), activationPiegeEmpoisonne, "Piège Empoisonné", (120, 120, 120), cible_non_requise=True)], [
        ], 0, 1, 1, 3, 1, "cercle", False, description="""Empoisonne la cible en occasionnant des dommages Air pendant 3 tours.""", chaine=True),

        Sort.Sort("Piège Empoisonné", 81, 3, 1, 3, [EffetPiege(Zones.TypeZoneCroix(1), activationPiegeEmpoisonne, "Piège Empoisonné", (120, 120, 120), cible_non_requise=True)], [
        ], 0, 1, 1, 3, 1, "cercle", False, description="""Empoisonne la cible en occasionnant des dommages Air pendant 3 tours.""", chaine=True),

        Sort.Sort("Piège Empoisonné", 124, 3, 1, 4, [EffetPiege(Zones.TypeZoneCroix(1), activationPiegeEmpoisonne, "Piège Empoisonné", (120, 120, 120), cible_non_requise=True)], [
        ], 0, 1, 1, 2, 1, "cercle", False, description="""Empoisonne la cible en occasionnant des dommages Air pendant 3 tours.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Injection Toxique", 150, 5, 1, 5, [
            EffetRetireEtat("Injection Toxique", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur"), EffetEtat(EtatEffetDebutTour("Injection Toxique", 0, 3, EffetDegats(28, 32, "Air"), "Injection Toxique", "lanceur"))],
                  [EffetRetireEtat("Injection Toxique", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur"), EffetEtat(EtatEffetDebutTour("Injection Toxique", 0, 3, EffetDegats(34, 38, "Air"), "Injection Toxique", "lanceur"))], 5, 1, 1, 5, 0, "cercle", True, description="""Applique un poison Air sur la cible. Chaque piège déclenché réduit le temps de relance d'Injection Toxique.
    La réduction du temps de relance disparaît quand le sort est lancé.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Concentration de Chakra", 38, 2, 1, 4, [EffetEtat(EtatEffetSiPiegeDeclenche('Concentration de Chakra', 0, 1, EffetVolDeVie(15, 15, "Feu"), "Concentration de Chakra", "lanceur", "porteur"))], [
        ], 0, 1, 1, 4, 0, "ligne", True, description="""Vole de la vie dans l'élément Feu lorsque la cible déclenche un piège.""", chaine=True),

        Sort.Sort("Concentration de Chakra", 90, 2, 1, 5, [EffetEtat(EtatEffetSiPiegeDeclenche('Concentration de Chakra', 0, 1, EffetVolDeVie(15, 15, "Feu"), "Concentration de Chakra", "lanceur", "porteur"))], [
        ], 0, 1, 1, 3, 0, "ligne", True, description="""Vole de la vie dans l'élément Feu lorsque la cible déclenche un piège.""", chaine=True),

        Sort.Sort("Concentration de Chakra", 132, 2, 1, 6, [EffetEtat(EtatEffetSiPiegeDeclenche('Concentration de Chakra', 0, 1, EffetVolDeVie(15, 15, "Feu"), "Concentration de Chakra", "lanceur", "porteur"))], [
        ], 0, 1, 1, 2, 0, "ligne", True, description="""Vole de la vie dans l'élément Feu lorsque la cible déclenche un piège.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège à Fragmentation", 155, 4, 1, 8, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeAFragmentation, "Piège à Fragmentation", (120, 0, 0), cible_non_requise=True)], [], 0, 1, 99, 0, 1, "cercle", True, description="""Pose un piège mono-cellule qui inflige des dommages Feu.
    Les dommages augmentent en fonction de la distance avec le centre de la zone d'effet.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège d'Immobilisation", 44, 4, 1, 4, [EffetPiege(Zones.TypeZoneCercle(2), activationPiegeDimmobilisation, "Piège d'Immobilisation", (
            120, 0, 120), cible_non_requise=True)], [], 0, 1, 1, 7, 1, "ligne", False, description="""Retire des PM.""", chaine=True),

        Sort.Sort("Piège d'Immobilisation", 97, 4, 1, 4, [EffetPiege(Zones.TypeZoneCercle(3), activationPiegeDimmobilisation, "Piège d'Immobilisation", (
            120, 0, 120), cible_non_requise=True)], [], 0, 1, 1, 6, 1, "ligne", False, description="""Retire des PM.""", chaine=True),

        Sort.Sort("Piège d'Immobilisation", 137, 4, 1, 5, [EffetPiege(Zones.TypeZoneCercle(3), activationPiegeDimmobilisation, "Piège d'Immobilisation", (
            120, 0, 120), cible_non_requise=True)], [], 0, 1, 1, 5, 1, "ligne", False, description="""Retire des PM.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège de Dérive", 160, 2, 1, 6, [EffetPiege(Zones.TypeZoneCroixDiagonale(1), activationPiegeDeDerive, "Piège de Dérive", (
            0, 0, 120), cible_non_requise=True)], [], 0, 1, 1, 2, 1, "cercle", False, description="""Pose un piège qui pousse de 2 cases.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège Insidieux", 50, 3, 1, 4, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeInsidieux, "Piège Insidieux", (0, 200, 0), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 1, "cercle", False, description="""Pose un piège. Une fois déclenché, les ennemis qui terminent leur tour dans sa zone d'effet subissent des dommages Air.""", chaine=True),

        Sort.Sort("Piège Insidieux", 103, 3, 1, 5, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeInsidieux, "Piège Insidieux", (0, 200, 0), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 1, "cercle", False, description="""Pose un piège. Une fois déclenché, les ennemis qui terminent leur tour dans sa zone d'effet subissent des dommages Air.""", chaine=True),

        Sort.Sort("Piège Insidieux", 143, 3, 1, 6, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeInsidieux, "Piège Insidieux", (0, 200, 0), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 1, "cercle", False, description="""Pose un piège. Une fois déclenché, les ennemis qui terminent leur tour dans sa zone d'effet subissent des dommages Air.""", chaine=True)
    ]))
    effetPoisonEpidemie = EffetEtat(EtatEffetFinTour("Poison Épidémie", 0, 1, EffetDegats(
        38, 42, "Air"), "Poison Épidémie", "lanceur"), cibles_possibles="Ennemis")
    etatPropageEpidemie = EtatEffetFinTour("Propagation Épidémie", 0, 1, EffetEtat(EtatEffetFinTour("Propagation Poison Épidémie", 0, 1, EffetDegats(
        38, 42, "Air"), "Propagation Poison Épidémie", "lanceur"), cibles_possibles="Ennemis", zone=Zones.TypeZoneCercleSansCentre(2)), "Propagation Épidémie", "lanceur")
    effetPropagationEpidemie = EffetEtat(
        etatPropageEpidemie, cibles_possibles="Ennemis")
    effetPropagationPropagationEpidemie = EffetEtat(EtatEffetFinTour("Continue Épidémie", 0, 1, EffetEtat(
        etatPropageEpidemie, zone=Zones.TypeZoneCercleSansCentre(2)), "Continue Épidémie", "lanceur"), cibles_possibles="Ennemis")

    effetPoisonEpidemieCC = EffetEtat(EtatEffetFinTour("Poison Épidémie", 0, 1, EffetDegats(
        46, 50, "Air"), "Poison Épidémie", "lanceur"), cibles_possibles="Ennemis")
    etatPropageEpidemieCC = EtatEffetFinTour("Propagation Épidémie", 0, 1, EffetEtat(EtatEffetFinTour("Propagation Poison Épidémie", 0, 1, EffetDegats(
        46, 50, "Air"), "Propagation Poison Épidémie", "lanceur"), cibles_possibles="Ennemis", zone=Zones.TypeZoneCercleSansCentre(2)), "Propagation Épidémie", "lanceur")
    effetPropagationEpidemieCC = EffetEtat(
        etatPropageEpidemieCC, cibles_possibles="Ennemis")
    effetPropagationPropagationEpidemieCC = EffetEtat(EtatEffetFinTour("Continue Épidémie", 0, 1, EffetEtat(
        etatPropageEpidemieCC, zone=Zones.TypeZoneCercleSansCentre(2)), "Continue Épidémie", "lanceur"), cibles_possibles="Ennemis")

    epidemie = Sort.Sort("Épidémie", 165, 4, 1, 5, [effetPropagationEpidemie, effetPropagationPropagationEpidemie, effetPoisonEpidemie], [
        effetPropagationEpidemieCC, effetPropagationPropagationEpidemieCC, effetPoisonEpidemieCC
    ], 5, 2, 1, 0, 0, "ligne", True, description="""Applique un poison Air de fin de tour sur les ennemis.
    La cible propage le poison en zone autour d'elle.""", chaine=True)
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [epidemie]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège répulsif", 56, 3, 1, 3, [EffetPiege(Zones.TypeZoneCercle(1), activationPiegeRepulsif, "Piège répulsif", (255, 0, 255), cible_non_requise=True)], [], 0, 1, 1, 1, 1, "cercle", False, description="""Repousse les alliés et les ennemis.
    Occasionne des dommages Air aux ennemis.""", chaine=True),

        Sort.Sort("Piège répulsif", 112, 3, 1, 5, [EffetPiege(Zones.TypeZoneCercle(1), activationPiegeRepulsif, "Piège répulsif", (255, 0, 255), cible_non_requise=True)], [], 0, 1, 1, 1, 1, "cercle", False, description="""Repousse les alliés et les ennemis.
    Occasionne des dommages Air aux ennemis.""", chaine=True),

        Sort.Sort("Piège répulsif", 147, 3, 1, 7, [EffetPiege(Zones.TypeZoneCercle(1), activationPiegeRepulsif, "Piège répulsif", (255, 0, 255), cible_non_requise=True)], [], 0, 1, 1, 1, 1, "cercle", False, description="""Repousse les alliés et les ennemis.
    Occasionne des dommages Air aux ennemis.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège Repoussant", 170, 2, 1, 6, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeRepoussant, "Piège Repoussant", (0, 100, 20), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 1, "cercle", False, description="""Piège mono-cellule qui repousse de 2 cases en zone.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Peur", 62, 2, 2, 3, [EffetPousserJusque(cible_non_requise=True)], [
        ], 0, 99, 99, 0, 0, "ligne", False, description="""Pousse un allié ou un ennemi sur la cellule ciblée.""", chaine=True),

        Sort.Sort("Peur", 116, 2, 2, 5, [EffetPousserJusque(cible_non_requise=True)], [
        ], 0, 99, 99, 0, 0, "ligne", False, description="""Pousse un allié ou un ennemi sur la cellule ciblée.""", chaine=True),

        Sort.Sort("Peur", 153, 2, 2, 7, [EffetPousserJusque(cible_non_requise=True)], [
        ], 0, 99, 99, 0, 0, "ligne", False, description="""Pousse un allié ou un ennemi sur la cellule ciblée.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Méprise", 175, 3, 1, 4, [EffetEchangePlace("cible", zone=Zones.TypeZoneInfini(), cibles_possibles="Double|Comploteur"), EffetRetireEtat("Invisible", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], [], 0, 1, 99, 0, 0, "ligne", True, description="""La cible échange de place avec le Double.
        Dissipe l'invisibilité du lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Arnaque", 69, 3, 1, 6, [EffetDegats(25, 29, "Air")], [EffetDegats(
            32, 32, "Air")], 5, 99, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Air.""", chaine=True),

        Sort.Sort("Arnaque", 122, 3, 1, 6, [EffetDegats(29, 33, "Air")], [EffetDegats(
            36, 36, "Air")], 5, 99, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Air.""", chaine=True),

        Sort.Sort("Arnaque", 162, 3, 1, 6, [EffetDegats(33, 37, "Air")], [EffetDegats(
            40, 40, "Air")], 5, 99, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Air.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège de Proximité", 180, 3, 1, 4, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeDeProximite, "Piège de Proximité", (30, 120, 30), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 0, "cercle", False, description="""Pose un piège mono-cellule qui occasionne des dommages Air en zone.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Poisse", 77, 4, 1, 4, [EffetVolDeVie(22, 26, "Eau"), EffetEtat(EtatBoostCaracFixe("Poisse", 0, 1, "cc", -15))], [EffetVolDeVie(27, 31, "Eau"), EffetEtat(EtatBoostCaracFixe(
            "Poisse", 0, 1, "cc", -20))], 15, 3, 2, 0, 0, "cercle", True, description="""Vole de la vie dans l'élément Eau et réduit les chances de Coup critique.""", chaine=True),

        Sort.Sort("Poisse", 128, 4, 1, 4, [EffetVolDeVie(25, 29, "Eau"), EffetEtat(EtatBoostCaracFixe("Poisse", 0, 1, "cc", -20))], [EffetVolDeVie(30, 34, "Eau"), EffetEtat(EtatBoostCaracFixe(
            "Poisse", 0, 1, "cc", -25))], 15, 3, 2, 0, 0, "cercle", True, description="""Vole de la vie dans l'élément Eau et réduit les chances de Coup critique.""", chaine=True),

        Sort.Sort("Poisse", 172, 4, 1, 4, [EffetVolDeVie(28, 32, "Eau"), EffetEtat(EtatBoostCaracFixe("Poisse", 0, 1, "cc", -25))], [EffetVolDeVie(33, 37, "Eau"), EffetEtat(
            EtatBoostCaracFixe("Poisse", 0, 1, "cc", -30))], 15, 3, 2, 0, 0, "cercle", True, description="""Vole de la vie dans l'élément Eau et réduit les chances de Coup critique.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Calamité", 185, 4, 1, 6, [EffetPiege(Zones.TypeZoneCercle(0), activationCalamite, "Calamité", (30, 30, 220), cible_non_requise=True)], [
        ], 0, 1, 99, 0, 1, "cercle", False, description="""Pose un piège mono-cellule qui vole de la vie Eau en zone et retire de la fuite.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Fourberie", 84, 4, 0, 0, [EffetEtat(EtatBoostCaracFixe("Fourberie", 0, 3, "int", -40), zone=Zones.TypeZoneCroix(2, 3)), EffetEtatSelf(EtatBoostCaracFixe("Fourberie", 0, 3, "int", 40), zone=Zones.TypeZoneCroix(2, 3)), EffetAttire(2, zone=Zones.TypeZoneCroix(2, 3)), EffetDegats(30, 34, "Feu", zone=Zones.TypeZoneCroix(2, 3))], [EffetEtat(EtatBoostCaracFixe("Fourberie", 0, 3, "int", -60), zone=Zones.TypeZoneCroix(2, 3)), EffetEtatSelf(EtatBoostCaracFixe("Fourberie", 0, 3, "int", 60), zone=Zones.TypeZoneCroix(2, 3)), EffetAttire(2, zone=Zones.TypeZoneCroix(2, 3)), EffetDegats(36, 40, "Feu", zone=Zones.TypeZoneCroix(2, 3))], 25, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Feu en zone.
    Attire les cibles.
    Vole de l'Intelligence.""", chaine=True),
        Sort.Sort("Fourberie", 134, 4, 0, 0, [EffetEtat(EtatBoostCaracFixe("Fourberie", 0, 3, "int", -60), zone=Zones.TypeZoneCroix(2, 3)), EffetEtatSelf(EtatBoostCaracFixe("Fourberie", 0, 3, "int", 60), zone=Zones.TypeZoneCroix(2, 3)), EffetAttire(2, zone=Zones.TypeZoneCroix(2, 3)), EffetDegats(35, 39, "Feu", zone=Zones.TypeZoneCroix(2, 3))], [EffetEtat(EtatBoostCaracFixe("Fourberie", 0, 3, "int", -80), zone=Zones.TypeZoneCroix(2, 3)), EffetEtatSelf(EtatBoostCaracFixe("Fourberie", 0, 3, "int", 80), zone=Zones.TypeZoneCroix(2, 3)), EffetAttire(2, zone=Zones.TypeZoneCroix(2, 3)), EffetDegats(41, 45, "Feu", zone=Zones.TypeZoneCroix(2, 3))], 25, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Feu en zone.
    Attire les cibles.
    Vole de l'Intelligence.""", chaine=True),
        Sort.Sort("Fourberie", 178, 4, 0, 0, [EffetEtat(EtatBoostCaracFixe("Fourberie", 0, 3, "int", -80), zone=Zones.TypeZoneCroix(2, 3)), EffetEtatSelf(EtatBoostCaracFixe("Fourberie", 0, 3, "int", 80), zone=Zones.TypeZoneCroix(2, 3)), EffetAttire(2, zone=Zones.TypeZoneCroix(2, 3)), EffetDegats(40, 44, "Feu", zone=Zones.TypeZoneCroix(2, 3))], [EffetEtat(EtatBoostCaracFixe("Fourberie", 0, 3, "int", -100), zone=Zones.TypeZoneCroix(2, 3)), EffetEtatSelf(EtatBoostCaracFixe("Fourberie", 0, 3, "int", 100), zone=Zones.TypeZoneCroix(2, 3)), EffetAttire(2, zone=Zones.TypeZoneCroix(2, 3)), EffetDegats(46, 50, "Feu", zone=Zones.TypeZoneCroix(2, 3))], 25, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Feu en zone.
    Attire les cibles.
    Vole de l'Intelligence.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Perquisition", 190, 3, 1, 5, [EffetEtat(EtatEffetSiSubit('Etat temporaire', 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneCercle(2), cibles_possibles="Allies", cibles_exclues="Lanceur"), "Perquisition", "lanceur", "cible")), EffetPousser(2), EffetDegats(19, 23, "Eau"), EffetRetireEtat('Etat temporaire')], [EffetEtat(EtatEffetSiSubit('Etat temporaire', 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneCercle(3)), "Perquisition", "lanceur", "cible")), EffetPousser(2), EffetDegats(23, 27, "Eau"), EffetRetireEtat('Etat temporaire')], 5, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Eau et pousse la cible de 2 cases.
    100% des dommages sont distribués sous forme de soin aux alliés à 2 cellules de distance de la cible.
    N'affecte pas le lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Attaque Mortelle", 92, 4, 1, 2, [EffetDegats(39, 43, "Terre")], [EffetDegats(
            49, 53, "Terre")], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Attaque Mortelle", 141, 4, 1, 2, [EffetDegats(46, 50, "Terre")], [EffetDegats(
            56, 60, "Terre")], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Attaque Mortelle", 187, 4, 1, 2, [EffetDegats(53, 57, "Terre")], [EffetDegats(
            63, 67, "Terre")], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège Funeste", 195, 3, 1, 6, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeFuneste, "Piège Funeste", (30, 30, 50), cible_non_requise=True)], [], 0, 2, 99, 0, 1, "cercle", False, description="""Pose un piège monocible qui occasionne des dommages Terre.
    Les dommages sont augmentés en fonction du nombre d'ennemis à proximité du piège.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Piège Mortel", 100, 3, 1, 3, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeMortel, "Piège Mortel", (20, 10, 10), cible_non_requise=True)], [
        ], 0, 1, 1, 2, 1, "ligne", False, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Piège Mortel", 147, 3, 1, 3, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeMortel, "Piège Mortel", (20, 10, 10), cible_non_requise=True)], [
        ], 0, 1, 1, 1, 1, "ligne", False, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Piège Mortel", 197, 3, 1, 4, [EffetPiege(Zones.TypeZoneCercle(0), activationPiegeMortel, "Piège Mortel", (20, 10, 10), cible_non_requise=True)], [
        ], 0, 2, 99, 0, 1, "ligne", False, description="""Occasionne des dommages Terre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Perfidie", 200, 6, 1, 1, [EffetDegats(58, 62, "Terre"), EffetRetireEtat("Perfidie", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], [EffetDegats(64, 68, "Terre"), EffetRetireEtat("Perfidie", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], 25, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Terre. Chaque piège déclenché réduit le coût en PA de Perfidie.
    La réduction du coût en PA disparaît quand le sort est lancé.""", chaine=True)
    ]))
    return sorts
