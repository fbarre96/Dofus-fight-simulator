import Sort as Sort
from Effets.EffetEtat import EffetEtat
from Etats.EtatRedistribuerPer import EtatRedistribuerPer


def getSortsDebutCombat(lvl):
    sortsDebutCombat = []
    return sortsDebutCombat


def getSorts(lvl):
    sorts = []
    sorts.append(Sort.Sort("Strategie_iop", 0, 0, 0, 0, [EffetEtat(EtatRedistribuerPer(
        "Stratégie Iop", 0, -1, 50, "Ennemis|Allies", 2))], [], 0, 99, 99, 0, 0, "cercle", False))
    return sorts
