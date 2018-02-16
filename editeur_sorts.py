# -*- coding: utf-8 -*
import Zones
import Personnages
import Effets
import re
import sys, locale
def TrouveClassesEffets():
    classesEffet = []
    findRegs = []
    found = False
    regEffet = r"class\s+Effet(\w+)"
    with open("Effets.py") as file:
        for line in file:
            if found:
                if "def __init__" in line:
                    found = False
                    args = line.strip().replace("def __init__(self,","")
                    args = args.strip().replace("**kwargs):","").rstrip()[:-1]
                    classesEffet.append([findRegs[0],args])
            else:
                findRegs=re.findall(regEffet, line)
                if len(findRegs)>0:
                    found = True
    return classesEffet

def TrouveClassesEtats():
    classesEtat = []
    findRegs = []
    found = False
    regEffet = r"class\s+Etat(\w+)"
    with open("Etats.py") as file:
        for line in file:
            if found:
                if "def __init__" in line:
                    found = False
                    args = line.strip().replace("def __init__(self,","")
                    args = args.strip().replace("):","").rstrip()
                    classesEtat.append([findRegs[0],args])
            else:
                findRegs=re.findall(regEffet, line)
                if len(findRegs)>0:
                    found = True
    return classesEtat
def TrouveClassesZones():
    classesZones = []
    regEffet = r"class\s+TypeZone(\w+)"
    with open("Zones.py") as file:
        for line in file:
            classesZones.extend(re.findall(regEffet, line))
    return classesZones
def main():
    print u"---Création d'un nouveau sort---"
    print u"Entrez le nom du sort:"
    nomSort = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print u"Coût PA:"
    coutPA = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print u"Portée min:"
    minPO = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print u"Portée max:"
    maxPO = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print u"Nombre d'utilisation par tour:"
    nbLancerParTour = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print u"Nombre d'utilisation par cible:"
    nbLancerParTourParCible = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print u"Nombre de tours entre 2 utilisations:"
    nbLancerEntreDeux = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print u"La porté est modifiable (o/n)?"
    poMod = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    poMod = unicode(int(poMod == "o"))
    print u"Le lancer est comment ? (cercle/ligne/diagonale)"
    typeLancer = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print u"Le lancer est-il chainé ? (o/n)"
    chaine = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    chaine = u"True" if chaine == "o" else u"False"
    print u"Description:"
    desc = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    print "\n"
    print "Ajouter un effet (o/n) ?"
    listeEffets = TrouveClassesEffets()
    listeZones = TrouveClassesZones()
    effetsAjoutes = []
    continuerEffet = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    while continuerEffet=="o":
        print "choisissez un Effet par son nom:"
        for effet in listeEffets:
            print "-"+effet[0]
        effetsAAjoutes = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
        trouve = False
        for effet in listeEffets:
            if effet[0].lower() == effetsAAjoutes.lower():
                buffEffet="Effet"+effet[0]+"("
                trouve = True
                argsDeLEffet = effet[1].split(",")
                print "Entrez les arguments de l'effet:"
                argsBuff=[]
                for arg in argsDeLEffet:
                    if arg.strip() != "":
                        typeArg = arg[:arg.index("_")]
                        nameArg = arg[arg.index("_")+1:]
                        print nameArg+" (type: "+typeArg+"):"
                        valArg = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        if typeArg == "int":
                            argsBuff.append(valArg)
                        elif typeArg == "str":
                            argsBuff.append("u\""+valArg+"\"")
                        elif typeArg == "sort":
                            argsBuff.append(valArg)
                        elif typeArg == "etat":
                            argsBuff.append(valArg)
                        else:
                            print "type inconnu "+typeArg
                print "L'effet a une zone (o/n)?"
                aZone = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                zoneChoisie = None
                if aZone == "o":
                    for zone in listeZones:
                        print "-"+zone
                    print "Choix de la zone:"
                    while zoneChoisie not in listeZones:
                        zoneChoisie = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                    print "Taille de la zone:"
                    zonePO = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                    argsBuff.append("zone=TypeZone"+zoneChoisie+"("+zonePO+")")
                print "L'effet a des cibles/etats speciaux (o/n)?"
                checkKwargs = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                if checkKwargs == "o":
                    print "L'effet ne cible pas tout le monde (o/n)?"
                    aCiblePossibles = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                    ciblesPossibles = []
                    if aCiblePossibles == "o":    
                        print "L'effet peut cibler des allies (o/n)?"
                        tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        if tmp == "o":
                            ciblesPossibles.append("Allies")
                        print "L'effet peut cibler des ennemis (o/n)?"
                        tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        if tmp == "o":
                            ciblesPossibles.append("Ennemis")
                        print "L'effet peut cibler le lanceur (o/n)?"
                        tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        if tmp == "o":
                            ciblesPossibles.append("Lanceur")
                        print "L'effet a une cible custom (o/n)?"
                        cibleCustom = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        while cibleCustom=="o":
                            print "Nom de la cible custom:"
                            tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                            ciblesPossibles.append(tmp)
                            print "L'effet a une autre cible custom (o/n)?"
                            cibleCustom = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        argsBuff.append("cibles_possibles=\""+"|".join(ciblesPossibles)+"\"")
                    print "L'effet a des cibles exclues (o/n)?"
                    aCibleExclues = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                    ciblesExclues = []
                    if aCibleExclues == "o":    
                        print "L'effet est interdit sur le lanceur (o/n)?"
                        tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        if tmp == "o":
                            ciblesExclues.append("Lanceur")
                        print "L'effet a une cible interdite custom (o/n)?"
                        cibleCustom = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        while cibleCustom=="o":
                            print "Nom de la cible interdite custom:"
                            tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                            ciblesExclues.append(tmp)
                            print "L'effet a une autre cible interdite custom (o/n)?"
                            cibleCustom = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        argsBuff.append("cibles_exclues=\""+"|".join(ciblesExclues)+"\"")
                    print "L'effet sera  applique sur les cases vides (o/n)?"
                    tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                    faireAuVide = tmp == "o"
                    if faireAuVide:
                        argsBuff.append("faire_au_vide="+str(faireAuVide))
                    print "L'effet a des etats requis pour la cible direct (o/n)?"
                    aEtatsRequisDirect = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                    etatsRequisDirect = []
                    if aEtatsRequisDirect == "o":    
                        EtatRequis = "o"
                        while EtatRequis=="o":
                            print "Nom de l'etat requis:"
                            tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                            etatsRequisDirect.append(tmp)
                            print "L'effet a un autre etats requis pour la cible direct (o/n)?"
                            EtatRequis = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        argsBuff.append("etat_requis=\""+"|".join(etatsRequisDirect)+"\"")
                    print "L'effet a des etats requis pour chaque cible (o/n)?"
                    aEtatsRequisCibles= raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                    etatsRequisCibles = []
                    if aEtatsRequisCibles == "o":    
                        EtatRequis = "o"
                        while EtatRequis=="o":
                            print "Nom de l'etat requis:"
                            tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                            etatsRequisCibles.append(tmp)
                            print "L'effet a un autre etats requis pour chaque cibles  (o/n)?"
                            EtatRequis = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        argsBuff.append("etat_requis_cible=\""+"|".join(etatsRequisCibles)+"\"")
                    if len(etatsRequisCibles) + len(etatsRequisDirect)>0:
                        print "L'effet consommera les etats requis (o/n)?"
                        tmp = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
                        consommeEtat = tmp == "o"
                        argsBuff.append("consomme_etat="+str(consommeEtat))
                buffEffet+=",".join(argsBuff)
                buffEffet+=")"
                effetsAjoutes.append(buffEffet)
                break
        if not trouve:
            print "Effet non trouve :"+str(effetsAAjoutes)

        print "Ajouter un autre effet (o/n) ?"
        continuerEffet = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    efffff=u",".join(effetsAjoutes)
    print u"Sort(u\""+nomSort+u"\","+coutPA+u","+minPO+u","+maxPO+u",["+efffff+u"],"+nbLancerParTour+u","+nbLancerParTourParCible+u","+nbLancerEntreDeux+u","+poMod+u", \""+typeLancer+u"\", chaine="+chaine+u", description=u\""+desc+u"\"))"
if __name__ == "__main__":
    #Importation des bibliothèques nécessaires
    #TODO : Modularite
    main()