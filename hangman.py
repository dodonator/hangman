# coding: utf-8
import random
import os
import collections
# TODO:
# ratenRelativ richtig machen
# configurationsdatei einbinden
# Dokumentation!
# Windowskompatibilität
# Wortlistensäuberung
# Warum funktioniert das Eingeben von WÖrtern nicht?
# Themenspezifische Wortlisten (pokemon, personen und ähnliches)
# Die main() Funktion entflechten
# und vieles mehr...

haeufigkeitsTabellenDateiName = "haeufigkeitstabelleGER.csv"
HTDN = haeufigkeitsTabellenDateiName
wortListenDateiName = "wortliste.txt"
WLDN = wortListenDateiName

# Eingabefunktionen:

def wortEingabeManuell():
	"""
	Hier kann der Benutzer selber das Wort
	eingeben, dass geraten werden soll. Nach
	der Eingabe wird die Anzeige gelöscht.
	"""
	result = raw_input("Bitte geben sie das zu ratende Wort ein: ")	
	result = result.upper().strip()
	# os.system("cls") # Windows
	os.system("clear") # Unix
	return result
	
def wortEingabeAuto():
	"""
	Hier wird aus einer, vorher definierten Datei,
	eine Wortliste gezogen, aus der zufällig ein
	Wort ausgesucht und zurückgegeben wird.
	"""
	filename = WLDN
	f1 = open(filename,'r')
	content = f1.read().upper()
	f1.close()
	content = content.strip().split('\n')
	content.pop()
	wort = random.choice(content)
	return wort

# Ratefunktionen:
	
def ratenManuell():
	"""
	In dieser Funktion gibt der User ein Wort
	oder einen Buchstaben ein. Die Verarbeitung
	erfolgt hier noch nicht.
	"""
	wort = raw_input("Raten sie einen Buchstaben: ")
	return wort.upper()

def ratenZufallM():
	"""
	In dieser Funktion wird durch Zufall geraten,
	indem ein zufälliger Buchstabe zurückgegeben
	wird.
	"""
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	result = random.choice(alphabet)
	x = raw_input(":")
	return result

def ratenRelativ():
	"""
	In dieser Funktion rät der Computer die Buchstaben
	anhand einer vorher definierten Häufigkeitstabelle.
	Somit soll das typische Vorgehen eines Menschen, wenn
	er Hangman spielt, nämlich zuerst die häufigen Buch-
	staben zu raten, simuliert werden.
	"""
	f1 = open(HTDN,"r")
	content = f1.read()
	f1.close()

	lines = content.split("\n")
	for i in range(len(lines)):
		lines[i] = lines[i].split(";")

	alphabet = []
	haeufigkeit = []
	indexList = []
	lines.pop()
	for element in lines:
		alphabet.append(element[0])
		haeufigkeit.append(int(element[1]))

	for i in range(len(haeufigkeit)):
		tmp = 0
		for i2 in range(0,i):
			tmp += haeufigkeit[i2]
		indexList.append(tmp)
	
	r = random.randint(0,sum(haeufigkeit))

	for (index, element) in enumerate(indexList):		
		if element > r:
			result = alphabet[index].upper()			
			break
	
	x = raw_input(":")
	
	return result

# Hier können die Funktionen eingegeben werden, die
# benutzt werden sollen:
eingabe = wortEingabeManuell
raten = ratenManuell

def woerterHinzufuegen(wort,av = False):
	"""
	Formal:
	
		woerterHinzufuegen(wort,av = False)
	
	Parameter:
	
		wort: Wort, das hinzugefügt werden soll
	
		av: Boolean der entscheidet ob bei dem
			Hinzufuegen des Wortes in die Wortliste
			seine Bewertung beachtet werden soll.
			Wenn dies so ist, wird dem Wort ein Wert
			zugewiesen. Nun wird die Wortliste durch-
			laufen und es wird ebenfalls jedem Wort
			in der Wortliste ein Wert zugeordnet.
			Aus den Werten der Wortliste wird ein Durch-
			schnitt gebildet. Das übergebene Wort wird
			nur hinzugefügt, wenn seine Wertung <= der
			Durchschnitt der Wortliste ist. Dies soll
			dazu sorgen, dass die Wortliste wächst und
			dem automatischen Raten aus der Wortliste
			helfen.
	"""
	result = av
	filename = WLDN
	f1 = open(filename,"r")
	content = f1.read().upper()
	f1.close()
	content = content.split("\n")
	
	if av:
		scores = {}
		for element in content:
			scores[element] = bewertung(element,True)
		
		b = bewertung(wort,True)
		
		durchschnitt = 0
		summe = 0
		counter = 0
		for element in scores:
			summe += scores[element]
			counter += 1
		durchschnitt = float(summe)/float(counter)
		
		if b <= durchschnitt and wort not in content:
			con = "\n" + wort
			result = True
		else:
			con = ''
			result = False
	else:
		con = "\n" + wort
		result = False
	
	f1 = open(filename,"a")
	f1.write(con)
	f1.close()
	
	return result

def wortListeDrucken(av = False, sortiert = False):
	f1 = open(WLDN,"r")
	content = f1.read().upper().split("\n")
	f1.close()
	if sortiert:
		scores = {}
		for element in content:
			tmp = bewertung(element)
			scores[tmp] = element

		print "Verwendete Wortliste: " + WLDN

		oScores = collections.OrderedDict(sorted(scores.items()))
		for element in oScores:
			print str(element) + ' : ' + str(oScores[element])

	else:

		print "Wortliste: " + WLDN
		for element in content:
			tmp = bewertung(element,av)
			print element + ' : ' + str(tmp)
		print ''

def bewertung(wort,relScore=False):
	"""
	Formal:
	
		bewertung(wort,relScore=False)
	
	Parameter:
	
		wort: Wort, dass bewertet werden soll
		
		relScore: Boolean der entscheidet, ob
				  die Bewertung des Wortes re-
				  lativ zur Länge des Wortes ist
				  oder nicht. Der default-Wert
				  für relSCore ist False.
	
	Die Bewertung:
		
		Die Bewertung des WOrtes beruht auf drei
		verschiedenen Kriterien: w, s und l:
		
		w: Anzahl an Wiederholungen der Buchstaben
		   im Wort
		   (Sollte möglichst niedrig sein.)
		
		s: Seltenheitswert der Buchstaben im Wort
		   (Sollte möglichst niedrig sein.)
		   
		l: Länge des Wortes
		   (Sollte möglichst niedrig sein.)
		   
		Die Berechnung der Bewertung aus den drei
		Kriterien ist abhängig von dem Boolean relScore:
		
		relScore = True:
		
			result = float(s+w)/float(l)
			
		relSCore = False:
			
			result = s + w + l
		
		Diese Funktion übernimmt noch nicht den Vergleich
		von zwei Wörtern, weshalb darauf geachtet werden
		muss, wenn man zwei Wörter vergleichen möchte, dass
		sie mit der gleichen Formel (relScore muss gleich sein)
		bewertet werden.
	"""
	wort = wort.upper()
	
	f1 = open(HTDN,"r")
	ht = f1.read().upper()
	f1.close()
	
	lines = ht.split("\n")
	lines.pop()
	
	ht = {}
	for i in range(len(lines)):
		tmp = lines[i].split(";")
		ht[tmp[0]] = int(tmp[1])
	
	# ht ist nun eine Häufigkeitstabelle
	
	# Wiederholungen von Buchstaben:
	w = 1
	chars = []
	for tmp in wort:
		if tmp in chars:
			w += 1
		else:
			chars.append(tmp)
	# Länge eines Wortes:
	l = len(wort)
	
	# Seltenheit der Buchstaben:
	s = 0
	for char in wort:
		s += ht[char]
	
	# print "w: " + str(w)
	# print "s: " + str(s)
	# print "l: " + str(l)
	
	# Scoring:
	if relScore:
		result = float(s+w)/float(l)
	else:
		result = s + w + l
	
	# print "r: " + str(result)
	
	return result
	
def fehlerStatus(maximum,current):
	"""
	Formal:
		
		fehlerStatus(maximum,current)
		
	Parameter:
		
		maximum: Maximalwert an Fehlern, die gemacht
				 werden dürfen.
				 
		current: Aktuelle Zahl an Fehlern die bereits
				 gemacht wurden.
				 
	Diese Funktion ist dafür zuständig einen Balken zu
	'malen' der anzeigt wie viele Fehler der User schon
	gemacht hat, und wie viele er sich noch leisten kann.
	"""
	if current != maximum:	
				result = "[" + current*"*" + (maximum-current)*" " + "] " + str(current)	
	else:
		result = "You lose"

	print result
		
def main(wort,maximum = 10, av = False):
	wort = wort.upper()	
	wortA = list(wort)
	
	rate = []
	benutzteBuchstaben = []
	benutzteWorte = []
	richtigeBuchstaben = []	
	
	for i in range(len(wortA)):
		rate.append("-")

	fehlerCounter = 0
	gewonnen = False

	while fehlerCounter != maximum:
		
		# Anfangs werden mit dem tmpCounter
		# die Buchstaben gezählt, die der User
		#  schon erraten hat.
		tmpCounter = 0

		for element in wortA:
			if element in richtigeBuchstaben:
				tmpCounter += 1

		if tmpCounter == len(wortA):
			gewonnen = True
			break

		for element in rate:
			print element ,
		
		print '\n'
		
		# Hier werden die Buchstaben angezeigt,
		# die der User schon benutzt hat.
		
		print "Benutzte Buchstaben: "
		for element in benutzteBuchstaben:
			print element ,
		print '\n'
		
		# Hier werden die Wörter angezeigt, die
		# der User schon benutzt hat.
		
		print "Benutzte Wörter: "
		for element in benutzteWorte:
			print element + ' ' ,
		print '\n'
		
		# Hier werden die Fehler des Users angezeigt.
		
		print "Fehlerzähler: "
		fehlerStatus(maximum,fehlerCounter)
		print '\n'
		
		# Nun kommt die Verarbeitung
		
		tmp = raten() # tmp ist nun das geratene Wort
		
		# Hier wird getestet, ob der User einen Buchstaben
		# oder ein Wort eingegeben hat.
		if len(tmp) == 1:		
			
			# Falls es ein Buchstabe war, wird jetzt getestet,
			# ob der Buchstabe schon einmal vom User eingegeben
			# wurde.
			if tmp not in benutzteBuchstaben:

				if tmp in wortA:

					for i in range(len(wort)):

						if wortA[i] == tmp:
							rate[i] = tmp
			
					benutzteBuchstaben.append(tmp)
					richtigeBuchstaben.append(tmp)

				else:
					fehlerCounter += 1
					benutzteBuchstaben.append(tmp)
			else:
				fehlerCounter += 1
		
		# Hier wird getestet, ob das eingegebene Wort
		# die Länge des gesuchten Wortes hat.
		elif len(tmp) == len(wort):
			
			# Falls die Längen identisch sind wird nun
			# getestet, ob auch die Wörter gleich sind.
			if tmp == wort:
				gewonnen = True
			
			else:
				benutzteWorte.append(tmp)
				break
		
		else:
			fehlerCounter += 1
			
		# os.system("cls") # Windows
		os.system("clear") # Unix
	
	# Hier wird nach dem Spiel geklärt, ob
	# der User gewonnen hat.
	if gewonnen:
		print "Das Wort war: " + wort
		f1 = open("gewonnen.txt","r")
		content = f1.read()
		f1.close()
		print content
	
	# Hier wird nun das eingegebene Wort in
	# die Wortliste geschrieben
	tmp = woerterHinzufuegen(wort.upper(),av)
	
	if eingabe == wortEingabeManuell and tmp:
		print "Das eingegebene Wort war so gut, "
		print "dass es in die Wortliste aufgenom-"
		print "men wurde."


x = ""
while x != "q":
	os.system("clear") # Unix
	# os.system("cls") # Windows
	if x != "q":
		wort = eingabe()
		main(wort,10,True)
		x = raw_input("Drücken sie 'q' zum verlassen: ")
		
		r = random.randint(0,10)
		if r < 6:
			eingabe = wortEingabeAuto
		else:
			eingabe = wortEingabeManuell
	else:
		break


# wortListeDrucken(True,True)