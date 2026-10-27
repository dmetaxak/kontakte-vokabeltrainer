import re
OVR = {  # singular German -> full English plural string
 'die Information':'pieces of information','das Datum':'dates; data','der Held':'male heroes','die Heldin':'female heroes','das Prozent':'percentages, percents',
 'der Fernseher':'TV sets','die Rechnung':'bills; calculations','das Bild':'pictures','der Schuh':'shoes','der Stiefel':'boots',
 'die Frau':'women; wives','der Herr':'gentlemen','der Mann':'men; husbands','das Kind':'children','der Fuß':'feet',
 'die Platte':'vinyl records; disks, boards','die Höhe':'heights; amounts','die Nachfrage':'inquiries; demands',
 'die Angabe':'details, indications','die Geschichte':'histories; stories','der Spaß':'jokes','der Doktor':'doctors',
 'der Mensch':'human beings, people','die Person':'people','der Schweizer':'male Swiss people','die Schweizerin':'female Swiss people',
 'der Franzose':'male French people','die Französin':'female French people','der/die Deutsche':'Germans',
 'die Brille':'glasses','die Hose':'pants','das Haar':'hair','die Forschung':'research projects','die Sicherheit':'securities; safeguards',
 'die Wirtschaft':'economies','die Größe':'heights; sizes','das Studium':'university studies','die Tasche':'bags, purses, pockets',
 'der Herbst':'falls, autumns','die Universität':'universities','das Mädchen':'girls','die Kundin':'female customers, clients',
 'der Kunde':'male customers, clients','das Auge':'eyes','die Decke':'ceilings','der Grad':'degrees','der Euro':'euros',
 'die Liebe':'loves','die Freude':'joys, pleasures','das Wort':'words','die Frage':'questions','die Hoffnung':'hopes','die Zeit':'times',
 'die Struktur':'structures, patterns','das Hemd':'shirts','der Rucksack':'backpacks','das Regal':'bookshelves, bookcases',
 'das Gesicht':'faces','das Gebiet':'areas','die Reihenfolge':'orders, sequences','die Sonne':'suns','der Wortschatz':'vocabularies',
 'die Prüfung':'tests','der Wald':'forests, woods','der Bauch':'bellies, stomachs','die Hausaufgabe':'homework','das Fach':'academic subjects','der Schrank':'wardrobe cabinets, cupboards','das Geschäft':'stores',
 'das Frühstück':'breakfasts','der Einfluss':'influences','das Tier':'animals','der Hintergrund':'backgrounds','der Vordergrund':'foregrounds',
 'die Zukunft':'futures','die/der Erwachsene':'adults, grown-ups','die/der Jugendliche':'teenagers, youths','die/der Geliebte':'beloved friends, lovers',
 'die Ordnung':'orders, regulations','der Mittag':'noons, middays','der Arzt':'male physicians','die Ärztin':'female physicians','die Angst':'fears',
}
IRREG = {'man':'men','woman':'women','child':'children','foot':'feet','person':'people','mouse':'mice','tooth':'teeth'}
def pl1(w):
    w=w.strip()
    if not w: return w
    m=re.match(r'^(.*?)(\s*\(.*\))?$',w)
    core,paren=m.group(1),m.group(2) or ''
    last=core.split(' ')[-1]
    if last in IRREG: new=IRREG[last]
    elif re.search(r'(s|x|z|ch|sh)$',last): new=last+'es'
    elif re.search(r'[^aeiou]y$',last): new=last[:-1]+'ies'
    elif last.endswith('.'): new=last
    else: new=last+'s'
    return ' '.join(core.split(' ')[:-1]+[new])+paren
def en_plural(g,e):
    if g in OVR and OVR[g]: return OVR[g]
    return re.sub(r'[^;,]+',lambda m:(' ' if m.group(0).startswith(' ') else '')+pl1(m.group(0)),e)
