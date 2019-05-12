# -*- coding: utf-8 -*
import re
import json
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

def CreateChargerSorts(classe):
    nomClasse = classe.lower()
    text_func = ""
    
    with open("sorts_db/sorts_"+nomClasse+".json","r") as f:
        classe_sorts = json.loads(f.read())
        count = 0
        for nom_sort, sort_values in classe_sorts.items():
            text_func+="\nsorts.append(Personnage.getSortRightLvl(lvl,["
            isVariante = (count%2 == 1)
            count += 1
            levels = range(1,4)
            if isVariante:
                levels = range(1,2)
            for level in levels:
                text_func+="\n\tSort.Sort(\""+nom_sort+"\","
                text_func+=str(int(sort_values[str(level)]["level"]))+","
                text_func+=str(int(sort_values[str(level)]["PA"]))+","
                try:
                    text_func+=str(int(sort_values[str(level)]["PO_min"]))+","
                except:
                    raise Exception("No PO_min pour "+str(nomClasse)+" "+nom_sort)
                text_func+=str(int(sort_values[str(level)]["PO_max"]))+","
                text_func+=getListeEffets(sort_values[str(level)],"Effets", sort_values["desc"])+"," # tab effet
                text_func+=getListeEffets(sort_values[str(level)],"EffetsCritiques", sort_values["desc"]) +"," # tab effet critique
                nbTourEntreDeuxLancer = int(sort_values[str(level)]["Autres"].get("Nb. de tours entre deux lancers",0))
                if nbTourEntreDeuxLancer == 0:
                    nbLancerParTour = int(sort_values[str(level)]["Autres"].get("Nb. de lancers par tour",99))
                    nbLancerParTourParJoueur = int(sort_values[str(level)]["Autres"].get("Nb. de lancers par tour par joueur",99))
                else:
                    nbLancerParTour = 1
                    nbLancerParTourParJoueur = 1
                text_func+=str(int(sort_values[str(level)]["Autres"].get("Probabilité de coup critique","0%").split("%")[0]))+","
                text_func+=str(int(nbLancerParTour))+","
                text_func+=str(int(nbLancerParTourParJoueur))+","
                text_func+=str(int(nbTourEntreDeuxLancer))+","
                poMod = 1 if sort_values[str(level)]["Autres"].get("Portée modifiable", "Oui") == "Oui" else 0
                text_func+=str(int(poMod))+","
                if "diagonale" in str(sort_values["desc"]).lower():
                    typeLancer = "diagonale"
                else:
                    typeLancer = "ligne" if sort_values[str(level)]["Autres"].get("Lancer en ligne", "Non") == "Oui" else "cercle"
                text_func+="\""+str(typeLancer)+"\","
                ldv = "True" if sort_values[str(level)]["Autres"].get("Ligne de vue", "Oui") == "Oui" else "False"
                text_func += ldv+","
                text_func += "description=\"\"\""+str(sort_values["desc"])+"\"\"\""
                otherInfos = "chaine="+str("True")
                text_func += ", "+str(otherInfos)
                text_func+= ")"
                if level != levels[-1]:
                    text_func+=",\n"
                else:
                    text_func+="\n]))"
            
    return text_func

def getListeEffets(sort_values, tab, desc):
    ret_str = "["
    tab_effets = sort_values[tab]
    for effet in tab_effets:
        zone = sort_values["Autres"].get("Zone d'effet","")
        nomZone = ""
        if zone.strip()!="":
            if "jusqu'à la cellule ciblée" in desc:
                zone = "ligne jusque de 0 cases"
            elif "Tout le monde" in zone:
                nomZone="Cercle"
                tailleZone = "99"
            else:
                tailleZone = zone.split(" ")[-2].strip()
                typeZone = " ".join(zone.split(" ")[:-3]).strip().lower()
                #listeZones = {"cercle":"TypeZoneCercle","croix":"TypeZoneCroix", "croix diagonale":"TypeZoneCroixDiagonale", "anneau":"TypeZoneAnneau", "ligne":"TypeZoneLigne", "ligne jusque":"TypeZoneLigneJusque", "ligne perpendiculaire":"TypeZoneLignePerpendiculaire", "carré":"TypeZoneCarre"}
                
                typeZone = map(lambda x: x[0].upper() + x[1:].lower(),typeZone.split(" "))
                nomZone = "".join(typeZone)
            
            nomZone = "TypeZone"+nomZone+"("+tailleZone+")"
        if "(dommages " in effet:
            effetsCaracs = effet.split(" ")
            degMin = effetsCaracs[0]
            if effetsCaracs[1] == "à":
                degMax = effetsCaracs[2]
                degType = effetsCaracs[-1][:-1] # enleve la parenthese de fin d'effet de dommage
            else:
                degMax = degMin
                degType = effetsCaracs[-1][:-1] # enleve la parenthese de fin d'effet de dommage
            ret_str+="Effets.EffetDegats("+str(degMin)+","+str(degMax)+",\""+degType+"\""
        elif "(vol " in effet:
            effetsCaracs = effet.split(" ")
            degMin = effetsCaracs[0]
            degMax = effetsCaracs[2]
            degType = effetsCaracs[-1][:-1] # enleve la parenthese de fin d'effet de dommage
            ret_str+="Effets.EffetVolDeVie("+str(degMin)+","+str(degMax)+",\""+degType+"\""
        else:
            ret_str+="Effets.TODO("+str(effet)
        if nomZone != "":
            ret_str +=",zone=Zones."+nomZone
        # ret_str +=",faire_au_vide=False"
        # ret_str +=",etat_requis=\"\""
        # ret_str +=",etat_requis_cibles=\"\""
        # ret_str +=",consomme_etat=False" 
        # ret_str +=",cibles_possibles=\"Allies|Ennemis|Lanceur\""
        # ret_str +=",cibles_exclues=\"\""
        ret_str +=")"
        if effet != tab_effets[-1]:
            ret_str+=","
    return ret_str+"]"

def getNonAutoInfos():
    ret = ""
    print("Le lancer est-il chainé (si oui la liste des effets prendra fin si l'un d'eux échoue)? (o/n)")
    chaine = input()
    chaine = "True" if chaine == "o" else "False"
    ret += "chaine="+str(chaine)
    return ret
    # print("Ajouter un effet (o/n) ?")
    # listeEffets = TrouveClassesEffets()
    # listeZones = TrouveClassesZones()
    # effetsAjoutes = []
    # continuerEffet = input()
    # while continuerEffet=="o":
    #     print("choisissez un Effet par son nom:")
    #     for effet in listeEffets:
    #         print("-"+effet[0])
    #     effetsAAjoutes = input()
    #     trouve = False
    #     for effet in listeEffets:
    #         if effet[0].lower() == effetsAAjoutes.lower():
    #             buffEffet="Effet"+effet[0]+"("
    #             trouve = True
    #             argsDeLEffet = effet[1].split(",")
    #             print("Entrez les arguments de l'effet:")
    #             argsBuff=[]
    #             for arg in argsDeLEffet:
    #                 if arg.strip() != "":
    #                     typeArg = arg[:arg.index("_")]
    #                     nameArg = arg[arg.index("_")+1:]
    #                     print(nameArg+" (type: "+typeArg+"):")
    #                     valArg = input()
    #                     if typeArg == "int":
    #                         argsBuff.append(valArg)
    #                     elif typeArg == "str":
    #                         argsBuff.append("u\""+valArg+"\"")
    #                     elif typeArg == "sort":
    #                         argsBuff.append(valArg)
    #                     elif typeArg == "etat":
    #                         argsBuff.append(valArg)
    #                     else:
    #                         print("type inconnu "+typeArg)
    #             print("L'effet a une zone (o/n)?")
    #             aZone = input()
    #             zoneChoisie = None
    #             if aZone == "o":
    #                 for zone in listeZones:
    #                     print("-"+zone)
    #                 print("Choix de la zone:")
    #                 while zoneChoisie not in listeZones:
    #                     zoneChoisie = input()
    #                 print("Taille de la zone:")
    #                 zonePO = input()
    #                 argsBuff.append("zone=TypeZone"+zoneChoisie+"("+zonePO+")")
    #             print("L'effet a des cibles/etats speciaux (o/n)?")
    #             checkKwargs = input()
    #             if checkKwargs == "o":
    #                 print("L'effet ne cible pas tout le monde (o/n)?")
    #                 aCiblePossibles = input()
    #                 ciblesPossibles = []
    #                 if aCiblePossibles == "o":    
    #                     print("L'effet peut cibler des allies (o/n)?")
    #                     tmp = input()
    #                     if tmp == "o":
    #                         ciblesPossibles.append("Allies")
    #                     print("L'effet peut cibler des ennemis (o/n)?")
    #                     tmp = input()
    #                     if tmp == "o":
    #                         ciblesPossibles.append("Ennemis")
    #                     print("L'effet peut cibler le lanceur (o/n)?")
    #                     tmp = input()
    #                     if tmp == "o":
    #                         ciblesPossibles.append("Lanceur")
    #                     print("L'effet a une cible custom (o/n)?")
    #                     cibleCustom = input()
    #                     while cibleCustom=="o":
    #                         print("Nom de la cible custom:")
    #                         tmp = input()
    #                         ciblesPossibles.append(tmp)
    #                         print("L'effet a une autre cible custom (o/n)?")
    #                         cibleCustom = input()
    #                     argsBuff.append("cibles_possibles=\""+"|".join(ciblesPossibles)+"\"")
    #                 print("L'effet a des cibles exclues (o/n)?")
    #                 aCibleExclues = input()
    #                 ciblesExclues = []
    #                 if aCibleExclues == "o":    
    #                     print("L'effet est interdit sur le lanceur (o/n)?")
    #                     tmp = input()
    #                     if tmp == "o":
    #                         ciblesExclues.append("Lanceur")
    #                     print("L'effet a une cible interdite custom (o/n)?")
    #                     cibleCustom = input()
    #                     while cibleCustom=="o":
    #                         print("Nom de la cible interdite custom:")
    #                         tmp = input()
    #                         ciblesExclues.append(tmp)
    #                         print("L'effet a une autre cible interdite custom (o/n)?")
    #                         cibleCustom = input()
    #                     argsBuff.append("cibles_exclues=\""+"|".join(ciblesExclues)+"\"")
    #                 print("L'effet sera  applique sur les cases vides (o/n)?")
    #                 tmp = input()
    #                 faireAuVide = tmp == "o"
    #                 if faireAuVide:
    #                     argsBuff.append("faire_au_vide="+str(faireAuVide))
    #                 print("L'effet a des etats requis pour la cible direct (o/n)?")
    #                 aEtatsRequisDirect = input()
    #                 etatsRequisDirect = []
    #                 if aEtatsRequisDirect == "o":    
    #                     EtatRequis = "o"
    #                     while EtatRequis=="o":
    #                         print("Nom de l'etat requis:")
    #                         tmp = input()
    #                         etatsRequisDirect.append(tmp)
    #                         print("L'effet a un autre etats requis pour la cible direct (o/n)?")
    #                         EtatRequis = input()
    #                     argsBuff.append("etat_requis=\""+"|".join(etatsRequisDirect)+"\"")
    #                 print("L'effet a des etats requis pour chaque cible (o/n)?")
    #                 aEtatsRequisCibles= input()
    #                 etatsRequisCibles = []
    #                 if aEtatsRequisCibles == "o":    
    #                     EtatRequis = "o"
    #                     while EtatRequis=="o":
    #                         print("Nom de l'etat requis:")
    #                         tmp = input()
    #                         etatsRequisCibles.append(tmp)
    #                         print("L'effet a un autre etats requis pour chaque cibles  (o/n)?")
    #                         EtatRequis = input()
    #                     argsBuff.append("etat_requis_cible=\""+"|".join(etatsRequisCibles)+"\"")
    #                 if len(etatsRequisCibles) + len(etatsRequisDirect)>0:
    #                     print("L'effet consommera les etats requis (o/n)?")
    #                     tmp = input()
    #                     consommeEtat = tmp == "o"
    #                     argsBuff.append("consomme_etat="+str(consommeEtat))
    #             buffEffet+=",".join(argsBuff)
    #             buffEffet+=")"
    #             effetsAjoutes.append(buffEffet)
    #             break
    #     if not trouve:
    #         print("Effet non trouve :"+str(effetsAAjoutes))

    #     print("Ajouter un autre effet (o/n) ?")
    #     continuerEffet = input()
    # efffff=",".join(effetsAjoutes)
    # print("Sort(u\""+nomSort+"\","+coutPA+","+minPO+","+maxPO+",["+efffff+"],"+nbLancerParTour+","+nbLancerParTourParCible+","+nbLancerEntreDeux+","+poMod+", \""+typeLancer+"\", chaine="+chaine+", description=u\""+desc+"\"))")
if __name__ == "__main__":
    #Importation des bibliothèques nécessaires
    #TODO : Modularite
    #main()
    ret = CreateChargerSorts(sys.argv[1])
    print(ret)