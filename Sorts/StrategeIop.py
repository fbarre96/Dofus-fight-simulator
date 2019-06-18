"""@summary: Les sorts de stratège iop
"""

import Sort
from Effets.EffetEtat import EffetEtat
from Etats.EtatRedistribuerPer import EtatRedistribuerPer


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
    sorts.append(Sort.Sort("Strategie_iop", 0, 0, 0, 0, [EffetEtat(EtatRedistribuerPer(
        "Stratégie Iop", 0, -1, 50, "Ennemis|Allies", 2))], [], 0, 99, 99, 0, 0, "cercle", False))
    return sorts
