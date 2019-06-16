import Sort as Sort
from Effets.EffetEtat import EffetEtat
import Zones as Zones
import Etats as Etats
import Personnages as Personnages

def getSortsDebutCombat(lvl):
    sortsDebutCombat = []
    return sortsDebutCombat

def getSorts(lvl):
    sorts = []
    sorts.append(Sort.Sort("Strategie_iop",0,0,0,0,[EffetEtat(Etats.EtatRedistribuerPer("Stratégie Iop",0,-1, 50,"Ennemis|Allies",2))],[],0,99,99,0,0,"cercle",False))
    return sorts