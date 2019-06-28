"""@summary: Les sorts du pandawasta (Lien Spiritueux de pandawa)
"""

import Sort
from Effets.EffetEtat import EffetEtat
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.Etat import Etat
# pylint: disable=line-too-long

def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    sorts.append(
        Sort.Sort("Bambou Malchanceux", 0, 0, 0, 1, [
            EffetEtat(EtatBoostCaracFixe("Bambou Malchanceux", 0, 1, "tacle", -23))
        ], [], 0, 1, 1, 0, 0, "ligne", True, description="Retire du tacle à la cible pour 1 tour.")
    )
    sorts.append(
        Sort.Sort("Coup de Bambou", 0, 2, 0, 1, [
            EffetEtat(EtatBoostCaracFixe("Coup de Bambou", 0, 2, "pui", -70)),
            EffetEtat(Etat("Affaibli", 0, 2)),
        ], [], 0, 1, 1, 3, 0, "ligne", True, description="Retire de la puissance à la cible et lui applique l'état affaibli.")
    )
    return sorts
