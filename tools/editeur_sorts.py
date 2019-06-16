"""@summary: Regroupe les outils qui ne font pas partie du simulateur mais qui aide à sa conception
"""
# -*- coding: utf-8 -*
import json
import sys


def createChargerSorts(classe):
    """@summary: tente de créer du code python pour le simulateur.
                lire les fichiers db et pond du code de construction de sort.
    """
    nomClasse = classe.lower()
    textFunc = ""

    with open("sorts_db/sorts_"+nomClasse+".json", "r") as fichier:
        classeSorts = json.loads(fichier.read())
        count = 0
        for nomSort, sortValues in classeSorts.items():
            textFunc += "\nsorts.append(Personnage.getSortRightLvl(lvl,["
            isVariante = (count % 2 == 1)
            count += 1
            levels = range(1, 4)
            if isVariante:
                levels = range(1, 2)
            for level in levels:
                textFunc += "\n\tSort.Sort(\""+str(nomSort)+"\","
                textFunc += str(int(sortValues[str(level)]["level"]))+","
                textFunc += str(int(sortValues[str(level)]["PA"]))+","
                try:
                    textFunc += str(int(sortValues[str(level)]
                                        ["PO_min"]))+","
                except:
                    raise Exception("No PO_min pour " +
                                    str(nomClasse)+" "+nomSort)
                textFunc += str(int(sortValues[str(level)]["PO_max"]))+","
                # tab effet
                textFunc += getListeEffets(
                    sortValues[str(level)], "Effets", sortValues["desc"])+","
                #  tab effet critique
                textFunc += getListeEffets(
                    sortValues[str(level)], "EffetsCritiques", sortValues["desc"]) + ","
                nbTourEntreDeuxLancer = int(sortValues[str(level)]["Autres"].get(
                    "Nb. de tours entre deux lancers", 0))
                if nbTourEntreDeuxLancer == 0:
                    nbLancerParTour = int(sortValues[str(level)]["Autres"].get(
                        "Nb. de lancers par tour", 99))
                    nbLancerParTourParJoueur = int(sortValues[str(level)]["Autres"].get(
                        "Nb. de lancers par tour par joueur", 99))
                else:
                    nbLancerParTour = 1
                    nbLancerParTourParJoueur = 1
                textFunc += str(int(sortValues[str(level)]["Autres"].get(
                    "Probabilité de coup critique", "0%").split("%")[0]))+","
                textFunc += str(int(nbLancerParTour))+","
                textFunc += str(int(nbLancerParTourParJoueur))+","
                textFunc += str(int(nbTourEntreDeuxLancer))+","
                poMod = 1 if sortValues[str(level)]["Autres"].get(
                    "Portée modifiable", "Oui") == "Oui" else 0
                textFunc += str(int(poMod))+","
                if "diagonale" in str(sortValues["desc"]).lower():
                    typeLancer = "diagonale"
                else:
                    typeLancer = "ligne" if sortValues[str(level)]["Autres"].get(
                        "Lancer en ligne", "Non") == "Oui" else "cercle"
                textFunc += "\""+str(typeLancer)+"\","
                ldv = "True" if sortValues[str(level)]["Autres"].get(
                    "Ligne de vue", "Oui") == "Oui" else "False"
                textFunc += ldv+","
                textFunc += "description=\"\"\"" + \
                    str(sortValues["desc"])+"\"\"\""
                otherInfos = "chaine="+str("True")
                textFunc += ", "+str(otherInfos)
                textFunc += ")"
                if level != levels[-1]:
                    textFunc += ",\n"
                else:
                    textFunc += "\n]))"

    return textFunc


def getListeEffets(sortValues, tab, desc):
    """@summary: Renvoie la liste d'effets traduit vers un constructeur d'Effet
    """
    retStr = "["
    tabEffets = sortValues[tab]
    for effet in tabEffets:
        zone = sortValues["Autres"].get("Zone d'effet", "")
        nomZone = ""
        if zone.strip() != "":
            if "jusqu'à la cellule ciblée" in desc:
                zone = "ligne jusque de 0 cases"
            elif "Tout le monde" in zone:
                nomZone = "Cercle"
                tailleZone = "99"
            else:
                tailleZone = zone.split(" ")[-2].strip()
                typeZone = " ".join(zone.split(" ")[:-3]).strip().lower()

                typeZone = map(lambda x: x[0].upper(
                ) + x[1:].lower(), typeZone.split(" "))
                nomZone = "".join(typeZone)

            nomZone = "TypeZone"+nomZone+"("+tailleZone+")"
        if "(dommages " in effet:
            effetsCaracs = effet.split(" ")
            degMin = effetsCaracs[0]
            if effetsCaracs[1] == "à":
                degMax = effetsCaracs[2]
                # enleve la parenthese de fin d'effet de dommage
                degType = effetsCaracs[-1][:-1]
            else:
                degMax = degMin
                # enleve la parenthese de fin d'effet de dommage
                degType = effetsCaracs[-1][:-1]
            retStr += "Effets.EffetDegats("+str(degMin) + \
                ","+str(degMax)+",\""+degType+"\""
        elif "(vol " in effet:
            effetsCaracs = effet.split(" ")
            degMin = effetsCaracs[0]
            degMax = effetsCaracs[2]
            # enleve la parenthese de fin d'effet de dommage
            degType = effetsCaracs[-1][:-1]
            retStr += "Effets.EffetVolDeVie("+str(degMin) + \
                ","+str(degMax)+",\""+degType+"\""
        else:
            retStr += "Effets.TODO("+str(effet)
        if nomZone != "":
            retStr += ",zone=Zones."+nomZone
        # retStr +=",faire_au_vide=False"
        # retStr +=",etat_requis=\"\""
        # retStr +=",etat_requis_cibles=\"\""
        # retStr +=",consomme_etat=False"
        # retStr +=",cibles_possibles=\"Allies|Ennemis|Lanceur\""
        # retStr +=",cibles_exclues=\"\""
        retStr += ")"
        if effet != tabEffets[-1]:
            retStr += ","
    return retStr+"]"

if __name__ == "__main__":
    # Importation des bibliothèques nécessaires
    # main()
    ret = createChargerSorts(sys.argv[1])
    print(ret)
