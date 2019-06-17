"""@summary: Rassemble les sorts de l'éniripsa
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetDegats import EffetDegats
from Effets.EffetSoin import EffetSoinSelonSubit
from Effets.EffetEtat import EffetEtat, EffetRetireEtat

from Etats.EtatEffet import EtatEffetSiSubit
import Zones

import Personnages


def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    sorts = []
    motDAirEffetAvant = EffetEtat(EtatEffetSiSubit('Etat temporaire', 0, 1, EffetSoinSelonSubit(
        100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'Air", "lanceur", "attaquant"))
    motDAirEffetApres = EffetRetireEtat('Etat temporaire')
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Blessant", 1, 4, 1, 6, [motDAirEffetAvant, EffetDegats(13, 15, "Air"), motDAirEffetApres], [motDAirEffetAvant, EffetDegats(17, 17, "Air"), motDAirEffetApres], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air.
        Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True),

        Sort.Sort("Mot Blessant", 30, 4, 1, 7, [motDAirEffetAvant, EffetDegats(16, 18, "Air"), motDAirEffetApres], [motDAirEffetAvant, EffetDegats(20, 20, "Air"), motDAirEffetApres], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air.
        Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True),

        Sort.Sort("Mot Blessant", 60, 4, 1, 8, [motDAirEffetAvant, EffetDegats(19, 21, "Air"), motDAirEffetApres], [motDAirEffetAvant, EffetDegats(23, 23, "Air"), motDAirEffetApres], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air.
        Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True)
    ]))
    return sorts
