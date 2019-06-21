"""@summary: Les sorts de Lapino
"""
# pylint: disable=line-too-long

import Sort
from Effets.EffetEtat import EffetEtat
from Etats.EtatBouclier import EtatBouclierPerLvl

def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    sorts.append(Sort.Sort("Protection du Lapino", 0, 3, 0, 8, [EffetEtat(EtatBouclierPerLvl("Protection du lapino", 0, 1, 73), cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False,
                           description="""Applique un bouclier de 72% du lvl de la cible."""))
    return sorts
