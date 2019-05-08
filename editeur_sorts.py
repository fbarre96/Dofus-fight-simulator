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
    print("---Création d'un nouveau sort---")
    print("Entrez le nom du sort:")
    nomSort = input()
    print("Coût PA:")
    coutPA = input()
    print("Portée min:")
    minPO = input()
    print("Portée max:")
    maxPO = input()
    print("Nombre d'utilisation par tour:")
    nbLancerParTour = input()
    print("Nombre d'utilisation par cible:")
    nbLancerParTourParCible = input()
    print("Nombre de tours entre 2 utilisations:")
    nbLancerEntreDeux = input()
    print("La porté est modifiable (o/n)?")
    poMod = input()
    poMod = str(int(poMod == "o"))
    print("Le lancer est comment ? (cercle/ligne/diagonale)")
    typeLancer = input()
    print("Le lancer est-il chainé ? (o/n)")
    chaine = input()
    chaine = "True" if chaine == "o" else "False"
    print("Description:")
    desc = input()
    print("\n")
    print("Ajouter un effet (o/n) ?")
    listeEffets = TrouveClassesEffets()
    listeZones = TrouveClassesZones()
    effetsAjoutes = []
    continuerEffet = input()
    while continuerEffet=="o":
        print("choisissez un Effet par son nom:")
        for effet in listeEffets:
            print("-"+effet[0])
        effetsAAjoutes = input()
        trouve = False
        for effet in listeEffets:
            if effet[0].lower() == effetsAAjoutes.lower():
                buffEffet="Effet"+effet[0]+"("
                trouve = True
                argsDeLEffet = effet[1].split(",")
                print("Entrez les arguments de l'effet:")
                argsBuff=[]
                for arg in argsDeLEffet:
                    if arg.strip() != "":
                        typeArg = arg[:arg.index("_")]
                        nameArg = arg[arg.index("_")+1:]
                        print(nameArg+" (type: "+typeArg+"):")
                        valArg = input()
                        if typeArg == "int":
                            argsBuff.append(valArg)
                        elif typeArg == "str":
                            argsBuff.append("u\""+valArg+"\"")
                        elif typeArg == "sort":
                            argsBuff.append(valArg)
                        elif typeArg == "etat":
                            argsBuff.append(valArg)
                        else:
                            print("type inconnu "+typeArg)
                print("L'effet a une zone (o/n)?")
                aZone = input()
                zoneChoisie = None
                if aZone == "o":
                    for zone in listeZones:
                        print("-"+zone)
                    print("Choix de la zone:")
                    while zoneChoisie not in listeZones:
                        zoneChoisie = input()
                    print("Taille de la zone:")
                    zonePO = input()
                    argsBuff.append("zone=TypeZone"+zoneChoisie+"("+zonePO+")")
                print("L'effet a des cibles/etats speciaux (o/n)?")
                checkKwargs = input()
                if checkKwargs == "o":
                    print("L'effet ne cible pas tout le monde (o/n)?")
                    aCiblePossibles = input()
                    ciblesPossibles = []
                    if aCiblePossibles == "o":    
                        print("L'effet peut cibler des allies (o/n)?")
                        tmp = input()
                        if tmp == "o":
                            ciblesPossibles.append("Allies")
                        print("L'effet peut cibler des ennemis (o/n)?")
                        tmp = input()
                        if tmp == "o":
                            ciblesPossibles.append("Ennemis")
                        print("L'effet peut cibler le lanceur (o/n)?")
                        tmp = input()
                        if tmp == "o":
                            ciblesPossibles.append("Lanceur")
                        print("L'effet a une cible custom (o/n)?")
                        cibleCustom = input()
                        while cibleCustom=="o":
                            print("Nom de la cible custom:")
                            tmp = input()
                            ciblesPossibles.append(tmp)
                            print("L'effet a une autre cible custom (o/n)?")
                            cibleCustom = input()
                        argsBuff.append("cibles_possibles=\""+"|".join(ciblesPossibles)+"\"")
                    print("L'effet a des cibles exclues (o/n)?")
                    aCibleExclues = input()
                    ciblesExclues = []
                    if aCibleExclues == "o":    
                        print("L'effet est interdit sur le lanceur (o/n)?")
                        tmp = input()
                        if tmp == "o":
                            ciblesExclues.append("Lanceur")
                        print("L'effet a une cible interdite custom (o/n)?")
                        cibleCustom = input()
                        while cibleCustom=="o":
                            print("Nom de la cible interdite custom:")
                            tmp = input()
                            ciblesExclues.append(tmp)
                            print("L'effet a une autre cible interdite custom (o/n)?")
                            cibleCustom = input()
                        argsBuff.append("cibles_exclues=\""+"|".join(ciblesExclues)+"\"")
                    print("L'effet sera  applique sur les cases vides (o/n)?")
                    tmp = input()
                    faireAuVide = tmp == "o"
                    if faireAuVide:
                        argsBuff.append("faire_au_vide="+str(faireAuVide))
                    print("L'effet a des etats requis pour la cible direct (o/n)?")
                    aEtatsRequisDirect = input()
                    etatsRequisDirect = []
                    if aEtatsRequisDirect == "o":    
                        EtatRequis = "o"
                        while EtatRequis=="o":
                            print("Nom de l'etat requis:")
                            tmp = input()
                            etatsRequisDirect.append(tmp)
                            print("L'effet a un autre etats requis pour la cible direct (o/n)?")
                            EtatRequis = input()
                        argsBuff.append("etat_requis=\""+"|".join(etatsRequisDirect)+"\"")
                    print("L'effet a des etats requis pour chaque cible (o/n)?")
                    aEtatsRequisCibles= input()
                    etatsRequisCibles = []
                    if aEtatsRequisCibles == "o":    
                        EtatRequis = "o"
                        while EtatRequis=="o":
                            print("Nom de l'etat requis:")
                            tmp = input()
                            etatsRequisCibles.append(tmp)
                            print("L'effet a un autre etats requis pour chaque cibles  (o/n)?")
                            EtatRequis = input()
                        argsBuff.append("etat_requis_cible=\""+"|".join(etatsRequisCibles)+"\"")
                    if len(etatsRequisCibles) + len(etatsRequisDirect)>0:
                        print("L'effet consommera les etats requis (o/n)?")
                        tmp = input()
                        consommeEtat = tmp == "o"
                        argsBuff.append("consomme_etat="+str(consommeEtat))
                buffEffet+=",".join(argsBuff)
                buffEffet+=")"
                effetsAjoutes.append(buffEffet)
                break
        if not trouve:
            print("Effet non trouve :"+str(effetsAAjoutes))

        print("Ajouter un autre effet (o/n) ?")
        continuerEffet = input()
    efffff=",".join(effetsAjoutes)
    print("Sort(u\""+nomSort+"\","+coutPA+","+minPO+","+maxPO+",["+efffff+"],"+nbLancerParTour+","+nbLancerParTourParCible+","+nbLancerEntreDeux+","+poMod+", \""+typeLancer+"\", chaine="+chaine+", description=u\""+desc+"\"))")
if __name__ == "__main__":
    #Importation des bibliothèques nécessaires
    #TODO : Modularite
    main()