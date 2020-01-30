import random

chordList = ["1", "2", "3", "4", "5", "6", "7"]
inversionList = ["  ", "6 ", "64"]
chords = ["1"]
chordNotes = ["135", "246", "357", "461", "572", "613", "724"]
scale = ["1", "2", "3", "4", "5", "6", "7", "8", "1", "2", "3", "4", "5", "6", "7", "8"]
beatNotes = ""
errors = 0
b = [1]
s = [17]
a = []
t = []

#create a random inversion
def inversionGenerator():
    inversion = random.choice(inversionList)
    return(inversion)

#determine if two notes violate parallel fifths
def parallelFifths(voice1, voice2):
    if (int(voice1[0]) - int(voice2[0])) % 8 == 5:
        first = "y"
    else:
        first = "n"
    if (int(voice1[1]) - int(voice2[1])) % 8 == 5:
    	second = "y"
    else:
    	second = "n"
    if first == "y" and second == "y":
    	parallelFifths = "y"
    else:
    	parallelFifths = "n"
    return(parallelFifths)
    
#determine if two notes violate parallel fourths
def parallelFourths(voice1, voice2):
    if (int(voice1[0]) - int(voice2[0])) % 8 == 4:
        first = "y"
    else:
        first = "n"
    if (int(voice1[1]) - int(voice2[1])) % 8 == 4:
    	second = "y"
    else:
    	second = "n"
    if first == "y" and second == "y":
    	parallelFourths = "y"
    else:
    	parallelFourths = "n"
    return(parallelFourths)    

#determine if two notes violate parallel octaves
def parallelOctaves(voice1, voice2):
    if (int(voice1[0]) - int(voice2[0])) % 8 == 0:
        first = "y"
    else:
        first = "n"
    if (int(voice1[1]) - int(voice2[1])) % 8 == 0:
    	second = "y"
    else:
    	second = "n"
    if first == "y" and second == "y":
    	parallelOctaves = "y"
    else:
    	parallelOctaves = "n"
    return(parallelOctaves)

#create random chord progression
for beat in range(1,14):
    inversion = inversionGenerator()
    chord = random.choice(chordList)
    chord = chord + inversion
    chords.append(chord)
chords.append('5  ')
chords.append('1  ')

#determine what notes are available on each beat based on chord
for beat in range(0, 16):
    chord = chords[beat]
    degree = chord[0]
    notes = chordNotes[int(degree)-1]
    beatNotes = beatNotes + " " + notes

#create bass line from bass notes in chords
for beat in range(1, 16):
    chord = chords[beat]
    degree = int(chord[0])
    inversion = chord[1:3]
    if inversion == "  ":
        bNote = degree
    elif inversion == "6 ":
        bNote = degree + 2
    else:
        bNote = degree + 4
    if bNote >= 8:
        bNote = bNote - 8
    b.append(int(bNote))
#b = map(int, b)
#print(b)

#create soprano line from available notes and rules about notes
for beat in range(5, 64, 4):
	notes = list(beatNotes[beat:beat + 3])
	sNote = int(random.choice(notes)) + 16
	s.append(sNote)
	while parallelFifths(s[len(s)-2:len(s)],b[len(s)-2:len(s)]) == "y" or parallelFourths(s[len(s)-2:len(s)],b[len(s)-2:len(s)]) == "y" or parallelFourths(s[len(s)-2:len(s)],b[len(s)-2:len(s)]) == "y":
		del s[-1]
		sNote = random.choice(notes)
		s.append(sNote)
		errors = errors + 1
		print(errors)
		if errors >= 2:
			errors = 0
			chords[len(s)] = random.choice(chordList) + inversionGenerator()
			break
	#print(s)				
	#print(s[len(s)-2:len(s)+1],b[len(s)-2:len(s)])

#print(chords)
#print(beatNotes)
print(s)
print(b)
