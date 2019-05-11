import requests
import bs4 as BeautifulSoup
import json
import time
from random import choice 
import sys
import urllib.request

def normaliser(chaine):
	"""@summary: enlève les accents d'une chaîne de caractère et la met en minuscule. Remplace également les espaces et apostrophes par un underscore.
	@chaine: chaîne de caractère à normaliser
	@type: string
	@return: La chaîne de caractère une fois les remplacements effectués.
	"""
	chaine = chaine.lower()
	chaine = chaine.replace(" ","_")
	chaine = chaine.replace("'","_")
	chaine = chaine.replace("é","e")
	chaine = chaine.replace("è","e")
	chaine = chaine.replace("ê","e")
	chaine = chaine.replace("à","a")
	chaine = chaine.replace("ï","i")
	chaine = chaine.replace("î","i")
	chaine = chaine.replace("ç","c")
	chaine = chaine.replace("â","a")
	return chaine

def load_requests(source_url, sink_path, headers):
    """
    Load a file from an URL (e.g. http).

    Parameters
    ----------
    source_url : str
        Where to load the file from.
    sink_path : str
        Where the loaded file is stored.
    """
    
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', headers["User-Agent"])
    opener.retrieve(source_url, sink_path)

def random_headers():
    desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
 

url = "https://www.dofus.com/fr/mmorpg/encyclopedie/classes/"
url_sorts = "https://www.dofus.com/fr/mmorpg/encyclopedie/sorts/details?"
url_classes = ["7-eniripsa","6-ecaflip","8-iop","9-cra","1-feca","11-sacrieur","10-sadida","2-osamodas","3-enutrof","4-sram","5-xelor","12-pandawa","13-roublard","14-zobal","15-steamer","16-eliotrope","17-huppermage","18-ouginak"]
url_classes = ["1-feca","11-sacrieur","10-sadida","2-osamodas","3-enutrof","4-sram","5-xelor","12-pandawa","13-roublard","14-zobal","15-steamer","16-eliotrope","17-huppermage","18-ouginak"]
if len(sys.argv) > 1:
    classes = sys.argv[1:]
else:
    classes = map(lambda x:x.split("-")[1].strip(),url_classes)
print("Cela va prendre un moment car un délai est ajouté pour prévenir l'anti-bruteforce de dofus.com")
headers={}
for classe in classes:
    print("Récupération des sorts "+str(classe))
    url_classe = None
    for url_classe in url_classes:
        if classe in url_classe:
            break
    if url_classe is None:
        break
    resp = requests.get(url+url_classe, headers=random_headers())
    while resp.status_code == 429:
        print("Le serveur indique qu'il recoit trop de requetes, attente de 5 sec.")
        time.sleep(5)
        resp = requests.get(url+url_classe,headers=random_headers())
    if resp.status_code != 200:
        raise Exception("Status code :"+str(resp.status_code) +" pour l'url "+url+url_classe)
    time.sleep(5)
    soup = BeautifulSoup.BeautifulSoup(resp.text, 'html.parser')
    mydivs = soup.findAll("a", {"data-target": ".ak-spell-details"})
    del mydivs[-1] # Remove celui ouvert de base
    len_total = len(mydivs)
    sorts = {}
    for count,my_div in enumerate(mydivs):
        print("Sort "+str(classe)+ " : "+str(count+1)+"/"+str(len_total))
        link_spell = my_div.get("href")
        idSpell = link_spell.split("id=")[1].split("&")[0]
        isVariante = (count%2 == 1)
        levels = range(1,4)
        if isVariante:
            levels = range(1,2)
        for level in levels:
            crafted_link = url_sorts+"id="+idSpell+"&level="+str(level)+"&selector=1"
            resp = requests.get(crafted_link,headers=random_headers())
            while resp.status_code == 429:
                print("Le serveur indique qu'il recoit trop de requetes, attente de 5 sec.")
                time.sleep(5)
                resp = requests.get(crafted_link,headers=random_headers())
            if resp.status_code != 200:
                raise Exception("Status code :"+str(resp.status_code) +" pour l'url "+crafted_link)
            time.sleep(5)
            soup_sort = BeautifulSoup.BeautifulSoup(resp.text, 'html.parser')
            div_sort = soup_sort.find("h2", {"class": "ak-spell-name"})
            nom_sort = div_sort.contents[0].strip()
            nom_variante = div_sort.find("a", {"class": "ak-ajaxloader"}).string.strip()
            sorts[nom_sort] = dict()
            img_div = soup_sort.find("div", {"class": "ak-spell-details-illu"})
            img_src = img_div.span.img.get("src")
            if level == levels[0]:
                load_requests(img_src,"sorts_db/sorts_icones/"+normaliser(nom_sort.lower())+".png",random_headers())
            sorts[nom_sort]["img"] = img_src
            sorts[nom_sort]["id"] = idSpell
            sorts[nom_sort][str(level)] = dict()
            sorts[nom_sort]["nom_variante"] = str(nom_variante)
            sorts_attr = div_sort.find("span", {"class": "ak-spell-po-pa"}).string.strip()
            PO_valeurs = sorts_attr.split("PO")[0].strip()
            PO_min_max = PO_valeurs.split("-")
            if len(PO_min_max) == 1 :# PO min et max sont égaux
                po_min = str(PO_min_max[0].strip())
                po_max = po_min
            elif len(PO_min_max) == 2:
                po_min = str(PO_min_max[0].strip())
                po_max = str(PO_min_max[1].strip())
            else:
                raise Exception("PO format inattendu : "+str(PO_valeurs))
            sorts[nom_sort][str(level)]["PO_min"] = str(po_min)
            sorts[nom_sort][str(level)]["PO_max"] = str(po_max)
            PA_valeur = sorts_attr.split("/")[1].split("PA")[0].strip()
            try:
                int(PA_valeur)
            except ValueError:
                raise Exception("PA valeur n'est pas un entiere : "+str(PA_valeur))
            sorts[nom_sort][str(level)]["PA"] = str(PA_valeur)
            description = soup_sort.find("span", {"class": "ak-spell-description"}).string.strip()
            sorts[nom_sort]["desc"] = str(description)
            niveau = soup_sort.find("a", {"class": "ak-selected"}).string.strip()
            sorts[nom_sort][str(level)]["level"] = niveau
            sorts[nom_sort][str(level)]["Effets"] = []
            sorts[nom_sort][str(level)]["EffetsCritiques"] = []
            tab_effets = soup_sort.findAll("div", {"class": "ak-spell-details-effects"})
            for num_tab_effet, tab_effet in enumerate(tab_effets):
                if num_tab_effet == 0:
                    to_fill = sorts[nom_sort][str(level)]["Effets"]
                else:
                    to_fill = sorts[nom_sort][str(level)]["EffetsCritiques"]
                effets = tab_effet.findAll("div", {"class":"ak-title"})
                for effet in effets:
                    to_fill.append(effet.string.strip())
            tab_autre = soup_sort.find("div", {"class": "ak-spell-details-other"})
            sorts[nom_sort][str(level)]["Autres"] = dict()
            autres_details = tab_autre.findAll("div", {"class":"ak-main-content"})
            for autres_detail in autres_details:
                nom_autre = autres_detail.find("div", {"class":"ak-title"}).string.strip()
                valeur_autre = autres_detail.find("div", {"class":"ak-aside"}).string
                if valeur_autre == None:
                    valeur_autre=autres_detail.find("div",{"class":"ak-text"}).string
                valeur_autre = valeur_autre.strip()
                sorts[nom_sort][str(level)]["Autres"][nom_autre] = valeur_autre
    with open("sorts_db/sorts_"+classe+".json","w") as f:
        f.write(json.dumps(sorts))
