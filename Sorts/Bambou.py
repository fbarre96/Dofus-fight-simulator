"""@summary: Les sorts de Bamboou de pandawa
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetEtat import EffetEtatSelf, EffetEtat
from Effets.EffetPorte import EffetPorte
from Etats.EtatEffet import EtatEffetSiSubit
from Etats.EtatBoostCarac import EtatBoostCaracFixe


def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    sortsDebutCombat.append(
        Sort.Sort("Bamboozel", 0, 0, 0, 0, [
            EffetEtatSelf(EtatEffetSiSubit("Bamboozleur", 0, -1, EffetEtat(EtatBoostCaracFixe("Karcham", 0, -1, "checkLdv", False), etat_requis="!Karcham"), "Bamboozel", "lanceur", "attaquant", "melee")),
            EffetEtatSelf(EtatEffetSiSubit("Bamboozleur", 0, -1, EffetPorte(etat_requis="!Saoul"), "Bamboozel", "lanceur", "attaquant", "melee"))
            ], [], 0, 99, 99, 0, 0, "cercle", False)
    )

    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    return sorts
