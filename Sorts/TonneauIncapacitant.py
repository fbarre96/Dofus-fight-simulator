"""@summary: Les sorts du tonneau attractif (Ivresse de pandawa)
"""

import Sort
import Zones
from Effets.EffetEtat import EffetEtatSelf, EffetEtat
from Effets.EffetRet import EffetRetPM
from Etats.EtatEffet import EtatEffetSiLance
from Etats.EtatBoostCarac import EtatBoostCaracFixe
# pylint: disable=line-too-long

def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    sortsDebutCombat.append(Sort.Sort("Ebrité", 0, 0, 0, 0, [
        EffetEtatSelf(EtatEffetSiLance("Tournée Générale si lancé", 0, -1, EffetRetPM(3, 1, cibles_possibles="Ennemis", cibles_possibles_direct="Tonneau Incapacitant", zone=Zones.TypeZoneCercle(1)), "Tournée Générale")),
    ], [], 0, 99, 99, 0, 0, "cercle", False, chaine=False))
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    sorts.append(
        Sort.Sort("Potion Magique", 0, 0, 0, 0, [
            EffetEtat(EtatBoostCaracFixe("Potion Magique", 0, 1, "pui", 150), cibles_possibles="Allies", cibles_possibles_direct="Lanceur", zone=Zones.TypeZoneCercle(2))
        ], [], 0, 99, 1, 0, 0, "ligne", True)
    )
    return sorts
