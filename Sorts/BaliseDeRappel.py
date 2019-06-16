import Sort as Sort
from Effets.EffetTp import EffetEchangePlace
from Effets.EffetTue import EffetTue
import Zones as Zones
import Etats as Etats
import Personnages as Personnages

def getSortsDebutCombat(lvl):
    sortsDebutCombat = []
    return sortsDebutCombat

def getSorts(lvl):
    sorts = []
    sorts.append(Sort.Sort("Rappel",0,0,0,0,[EffetEchangePlace(zone=Zones.TypeZoneInfini(),cibles_possibles="Cra"), EffetTue(zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],[],0,99,99,0,0,"cercle",False))
    return sorts