"""@summary: Les sorts de cadran de la synchro
"""
import Sort
from Effets.EffetDegats import EffetDegats
from Effets.EffetTue import EffetTue
from Effets.EffetEtat import EffetEtatSelfTF, EffetEtatSelf
from Effets.EffetEntiteLanceSort import EffetEntiteLanceSort
import Zones
from Etats.EtatEffet import EtatEffetSiTFGenere
from Etats.EtatBoostBaseDeg import EtatBoostBaseDegLvlBased
from Etats.Etat import Etat
# pylint: disable=line-too-long

def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    activationFinDesTemps = Sort.Sort("Fin des temps", 0, 0, 0, 0, [EffetDegats(0, 0, "air", zone=Zones.TypeZoneCercle(
        3), cibles_possibles="Ennemis"), EffetTue(cibles_possibles="Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False, chaine=False)
    sortsDebutCombat.append(
        Sort.Sort("Synchronisation", 0, 0, 0, 0, [
            EffetEtatSelf(EtatEffetSiTFGenere("Synchronisation", 0, -1, [EffetEtatSelfTF(EtatBoostBaseDegLvlBased("toReplace", 0, -1, "Fin des temps", 190), "Rembobinage",
                                                                                         cumulMax=1, etat_requis="!DejaBoost"), EffetEtatSelfTF(Etat("DejaBoost", 0, 1), "Rembobinage", remplaceNom=False, cumulMax=1)], "Téléfrageur", "porteur", "porteur")),
            EffetEtatSelf(EtatEffetSiTFGenere("Attente de la fin des temps", 0, -1, EffetEntiteLanceSort("Synchro", activationFinDesTemps), "Téléfrageur", "porteur", "porteur", True, "Rembobinage"))], [], 0, 99, 99, 0, 0, "cercle", False, description="""""", chaine=False)
    )
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort> """
    # pylint: disable=unused-argument
    sorts = []
    return sorts
