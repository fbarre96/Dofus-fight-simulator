"""@summary: Les sorts du tonneau attractif (Ivresse de pandawa)
"""

import Sort
import Zones
from Effets.EffetEtat import EffetEtatSelf, EffetRetireEtat
from Effets.EffetSoin import EffetSoin
from Effets.EffetPousser import EffetAttire
from Etats.EtatEffet import EtatEffetSiPorte, EtatEffetSiLance, EtatEffetDebutTour
# pylint: disable=line-too-long

def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    sortsDebutCombat.append(Sort.Sort("Ivresse", 0, 0, 0, 0, [
        EffetEtatSelf(EtatEffetSiPorte("Tournée Générale si porté", 0, -1, EffetEtatSelf(EtatEffetDebutTour("Tournée Générale", 0, 1, EffetSoin(53, 81, cibles_possibles="Allies", zone=Zones.TypeZoneCercle(1)), "Tournée Générale", "cible")), "Tournée Générale")),
        EffetEtatSelf(EtatEffetSiLance("Tournée Générale si lancé", 0, -1, EffetSoin(53, 81, cibles_possibles="Allies", zone=Zones.TypeZoneCercle(1)), "Tournée Générale")),
        EffetEtatSelf(EtatEffetSiLance("Tournée Générale annulé", 0, -1, EffetRetireEtat("Tournée Générale"), "Tournée Générale annulé"))
    ], [], 0, 99, 99, 0, 0, "cercle", False, chaine=False))
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    sorts.append(
        Sort.Sort("Beuverie", 0, 0, 0, 15, [
            EffetAttire(8, cibles_possibles="Ennemis"),
            EffetAttire(8, cibles_possibles="Allies", etat_requis_cibles="Saoul")
        ], [], 0, 99, 1, 0, 0, "cercle", True, chaine=False)
    )
    return sorts
