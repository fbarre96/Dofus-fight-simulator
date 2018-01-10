def getDistancePoint(p1 ,p2):
    	return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])
def getDistanceY(p1 ,p2):
	return abs(p1[1]-p2[1])
def getDistanceX(p1 ,p2):
	return abs(p1[0]-p2[0])

class TypeZone:
    def __init__(self):
        pass
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
    	print "zone inconnue"
        return False
    

class TypeZoneCercle(TypeZone):
    def __init__(self, zonePO):
    	self.zonePO = zonePO
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        return getDistancePoint(departZone,caseTestee) <= self.zonePO

class TypeZoneCercleSansCentre(TypeZone):
    def __init__(self, zonePO):
    	self.zonePO = zonePO
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        return getDistancePoint(departZone,caseTestee) <= self.zonePO and getDistancePoint(departZone,caseTestee) != 0

class TypeZoneCroix(TypeZone):
    def __init__(self, zonePO):
    	self.zonePO = zonePO
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        if getDistanceY(departZone,caseTestee) >0 and getDistanceX(departZone,caseTestee)>0:
            return False
        return getDistancePoint(departZone,caseTestee) <= self.zonePO        
class TypeZoneCroixDiagonale(TypeZone):
    def __init__(self, zonePO):
    	self.zonePO = zonePO*2
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        if getDistanceY(departZone,caseTestee)== getDistanceX(departZone,caseTestee):
            return False
        return getDistancePoint(departZone,caseTestee) <= self.zonePO        

class TypeZoneAnneau(TypeZone):
    def __init__(self, zonePO):
    	self.zonePO = zonePO
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        return getDistancePoint(departZone,caseTestee) == self.zonePO

class TypeZoneLigne(TypeZone):
    def __init__(self, zonePO):
    	self.zonePO = zonePO
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        horizontal = getDistanceY(joueurLanceur,departZone) == 0
        if horizontal and getDistanceY(departZone,caseTestee)>0:
            return False
        if not horizontal and getDistanceX(departZone,caseTestee)>0:
            return False
        if horizontal:
            if joueurLanceur[0] <= departZone[0]:
                return (caseTestee[0]-departZone[0] < self.zonePO) and caseTestee[0]-departZone[0]>=0
            else:
                return (abs(caseTestee[0]-departZone[0]) < self.zonePO) and caseTestee[0]-departZone[0]<=0
        else:
            if joueurLanceur[1] <= departZone[1]:
                return (caseTestee[1]-departZone[1] < self.zonePO) and caseTestee[1]-departZone[1]>=0
            else:
                return (abs(caseTestee[1]-departZone[1]) < self.zonePO) and caseTestee[1]-departZone[1]<=0

class TypeZoneLigneJusque(TypeZone):
    def __init__(self):
    	pass
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        horizontal = getDistanceY(joueurLanceur,departZone) == 0
        if horizontal and getDistanceY(departZone,caseTestee)>0:
            return False
        if not horizontal and getDistanceX(departZone,caseTestee)>0:
            return False
        if horizontal:
            if joueurLanceur[0] <= departZone[0]:
                return joueurLanceur[0] < caseTestee[0] and caseTestee[0] <= departZone[0]
            else:
                return joueurLanceur[0] > caseTestee[0] and caseTestee[0] >= departZone[0]
        else:
            if joueurLanceur[1] <= departZone[1]:
                return joueurLanceur[1] < caseTestee[1] and caseTestee[1] <= departZone[1]
            else:
                return joueurLanceur[1] > caseTestee[1] and caseTestee[1] >= departZone[1]

class TypeZoneLignePerpendiculaire(TypeZone):
    def __init__(self, zonePO):
    	self.zonePO = zonePO
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        horizontal = getDistanceX(joueurLanceur,departZone) == 0
        if horizontal and getDistanceY(departZone,caseTestee)>0:
            return False
        if not horizontal and getDistanceX(departZone,caseTestee)>0:
            return False
        return getDistancePoint(departZone,caseTestee) <= self.zonePO

class TypeZoneCarre(TypeZone):
    def __init__(self, zonePO):
    	self.zonePO = zonePO
    def testCaseEstDedans(self, departZone, caseTestee, joueurLanceur):
        return (getDistanceX(caseTestee,departZone) == self.zonePO or getDistanceY(caseTestee,departZone) == self.zonePO) and getDistanceX(caseTestee,departZone) <= self.zonePO and getDistanceY(caseTestee,departZone) <= self.zonePO