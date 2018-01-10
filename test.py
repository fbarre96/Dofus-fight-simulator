texte = "ABCDEFGH IJKLMNOPQ RSTUVWXZ1 234567 890"
i=0
tabMorceauTitre=texte.split(" ")
lignesTitre=[]
calcWidth = 0
nextWidth = 0
calcHeight = 0
while i+1 < len(tabMorceauTitre):
    buff = ""
    prevI = i
    while (calcWidth + nextWidth < 30) and i+1 < len(tabMorceauTitre):
        w = len(tabMorceauTitre[i]+" ")
        calcWidth+=w
        nextWidth = len(tabMorceauTitre[i+1]+" ")
        buff+=tabMorceauTitre[i]+" "
        i+=1
    if prevI == i:
        buff = tabMorceauTitre[i]
        i+=1
    lignesTitre.append(buff)
print str(lignesTitre)