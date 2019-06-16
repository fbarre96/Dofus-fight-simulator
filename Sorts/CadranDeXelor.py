import Sort as Sort
from Effets.EffetDegats import EffetDegats
from Effets.EffetEtat import EffetEtat
import Zones as Zones
from Etats.EtatBoostCarac import EtatBoostCaracFixe
import Personnages as Personnages

def getSortsDebutCombat(lvl):
    sortsDebutCombat = []
    return sortsDebutCombat

def getSorts(lvl):
    sorts = []
    sorts.append(Sort.Sort("Synchronisation",0,0,0,0,[EffetDegats(100,130,"feu",zone=Zones.TypeZoneCercleSansCentre(4), cibles_possibles="Ennemis|Lanceur",etat_requis_cibles="Telefrag"), EffetEtat(EtatBoostCaracFixe("Synchronisation",0,1,"PA",2),zone=Zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Lanceur",etat_requis_cibles="Telefrag")],[],0,99,99,0,0,"cercle",False,chaine=False))
    return sorts