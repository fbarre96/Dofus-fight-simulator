"""@summary: Les sorts de Fiole
"""
# pylint: disable=line-too-long
import Sort
import Zones
from Effets.EffetEtat import EffetEtatSelf
from Effets.EffetDegats import EffetDegats
from Effets.EffetTue import EffetTue
from Effets.EffetSoin import EffetSoinSelonSubit
from Etats.EtatModDeg import EtatModDegPer
from Etats.EtatEffet import EtatEffetSiSubit, EtatEffetSiMeurt, EtatEffetSiNouvelEtat

def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    sortsDebutCombat.append(
        Sort.Sort("Réduction des dégâts alliés", 0, 0, 0, 0, [EffetEtatSelf(EtatModDegPer("Réduction des dégâts alliés", 0, -1, 50, provenance="Allies"))], [], 0, 99, 99, 0, 0, "cercle", False)
    )
    sortsDebutCombat.append(
        Sort.Sort("Soin si subit", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiSubit("Soigne allié qui l'attaque", 0, -1, EffetSoinSelonSubit(100), "Soin de fiole", "cible", "attaquant", "", "Allies"))], [], 0, 99, 99, 0, 0, "cercle", False)
    )
    sortsDebutCombat.append(
        Sort.Sort("Explose", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiMeurt("Explose", 0, -1, EffetDegats(22, 26, "Terre", zone=Zones.TypeZoneCercleSansCentre(2)), "Soin de fiole", "lanceur", "mouru"))], [], 0, 99, 99, 0, 0, "cercle", False)
    )
    sortsDebutCombat.append(
        Sort.Sort("Trop de stimulation!", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiNouvelEtat("Meurt si stimulé", 0, -1, EffetTue(), "Meurt si stimulé", "porteur", "Stimulé"))], [], 0, 99, 99, 0, 0, "cercle", False)
    )
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    return sorts
