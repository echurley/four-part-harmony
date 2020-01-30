import random
#from midiutil import MIDIFile



#create midi file with four voices
#mf = MIDIFile(4)
#soprano = 0
#alto = 1
#tenor = 2
#bass = 3



chordList = ["1", "2", "3", "4", "5", "6", "7"]
inversionList = ["  ", "6 ", "64"]
chords = ["1"]
chordNotes = ["135", "246", "357", "461", "572", "613", "724"]
beatNotes = ""
b = [1]
s = [17]
a = []
t = []
parallelFifths = ""



#create a random inversion
def inversionGenerator():
    inversion = random.choice(inversionList)
    return(inversion)

#determine if two notes violate parallel fifths
def parallelFifths(voice1, voice2):
    parallelFifths = ""
    if (int(voice1[0]) - int(voice2[0])) % 8 == 5:
        if (int(voice1[1]) - int(voice2[1])) % 8 == 5:
            parallelFifths = "y"
        else:
            parallelFifths = "n"
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

#need to make sure voice is within the allowable range

#need to make sure the voices are close enough together

#need to make sure there is no voice crossing

#make is so the fifth isn't doubled


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
    root = chord[0]
    notes = chordNotes[int(root)-1]
    beatNotes = beatNotes + " " + notes

#create bass line from bass notes in chords
for beat in range(1, 16):
    chord = chords[beat]
    root = int(chord[0])
    inversion = chord[1:3]
    if inversion == "  ":
        bNote = root
    elif inversion == "6 ":
        bNote = root + 2
    else:
        bNote = root + 4
    if bNote >= 8:
        bNote = bNote - 8
    b.append(int(bNote))

print(beatNotes)
#create soprano line from available notes and rules about notes
for beat in range(5, 64, 4):
	notes = list(beatNotes[beat:beat + 3])
	sNote = int(random.choice(notes)) + 16
	s.append(sNote)
	#determine if note breaks any rules
	while parallelFifths(s[len(s)-2:len(s)],b[len(s)-2:len(s)]) == "y" or parallelFourths(s[len(s)-2:len(s)],b[len(s)-2:len(s)]) == "y" or parallelFourths(s[len(s)-2:len(s)],b[len(s)-2:len(s)]) == "y":
		#if it does, delete it and try again, removing that note from the available ones
		notes.remove(str(s[-1] - 16))
		del s[-1]
		sNote = random.choice(notes)
		s.append(sNote)
		#if there are no more available notes, change the chord, rinse and repeat
		if len(notes) == 0:
			chords[len(s)] = random.choice(chordList) + inversionGenerator()
			break
	#print(s)				
	#print(s[len(s)-2:len(s)+1],b[len(s)-2:len(s)])

#print(s)
#print(b)
#print(chords)
