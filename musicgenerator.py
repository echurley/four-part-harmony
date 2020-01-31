#c2 = 1
#c3 = 8
#c4 = 15
#c5 = 22
#an increase by one integer = movement up by one note name



import random
from inspect import signature
#from midiutil import MIDIFile



#create midi file with four voices
#mf = MIDIFile(4)
#soprano = 0
#alto = 1
#tenor = 2
#bass = 3



chordList = ["1", "2", "3", "4", "5", "6", "7"]
inversionList = ["  ", "6 ", "64"]
chords = ["1  "]
chordNotes = ["135", "246", "357", "461", "572", "613", "724"]
beatNotes = ""
b = ["b", 8]
s = ["s", 22]
a = ["a"]
t = ["t"]
parallelFifths = ""
#ranges = [15, 26, 12, 22, 8, 19, 3, 15]



#create a random inversion
def inversionGenerator():
    inversion = random.choice(inversionList)
    return(inversion)

#determine if two notes violate parallel fourths
def parallelFourths(voice1, voice2):
    parallelFourths = ""
    if (int(voice1[0]) - int(voice2[0])) % 7 == 5:
        if (int(voice1[1]) - int(voice2[1])) % 7 == 5:
            parallelFourths = "y"
        else:
            parallelFourths = "n"
    else:
        parallelFourths = "n"
    return(parallelFourths)
    
#determine if two notes violate parallel octaves
def parallelOctaves(voice1, voice2):
    voice1 = voice1[len(voice1)-2:len(voice1)]
    parallelOctaves = ""
    if (int(voice1[0]) - int(voice2[0])) % 7 == 5:
        if (int(voice1[1]) - int(voice2[1])) % 7 == 5:
            parallelOctaves = "y"
        else:
            parallelOctaves = "n"
    else:
        parallelOctaves = "n"
    return(parallelOctaves)    

#determine if two notes violate parallel fifths
def parallelFifths(voice1, voice2):
    parallelFifths = ""
    voice1a = int(voice1[len(voice1) - 1])
    voice2a = int(voice2[len(voice1) - 1])
    print(voice1a, voice2a)
    if (int(voice1[1]) - int(voice2[1])) % 7 == 5:
        if (int(voice1[2]) - int(voice2[2])) % 7 == 5:
            parallelFifths = "y"
        else:
            parallelFifths = "n"
    else:
        parallelFifths = "n"
    return(parallelFifths)

#make sure voice is within the allowable range
def rangeFinder(voice):
    length = len(voice) - 1
    note = int(voice[length])
    if voice[0] == "s":
    	if note > 26 or note < 15:
    	    inRange = "y"
    	else:
    	    inRange = "n"
    elif voice[0] == "a":
        if note > 22 or note < 12:
            inRange = "y"
        else:
            inRange = "n"
    elif voice[0] == "t":
        if note > 19 or note < 8:
            inRange = "y"
        else:
            inRange = "n"
    else:
        if note > 15 or note < 3:
            inRange = "y"
        else:
            inRange = "n"

#need to make sure the voices are close enough together

#need to make sure there is no voice crossing

#two leaps in a row

#dont double leading tone (b)

#try to weight nearest chord tones, yikes thats gonna suck

#similar motion -> perfect w/o step in soprano



#create random chord progression
for beat in range(2,16):
    inversion = inversionGenerator()
    chord = random.choice(chordList)
    chord = chord + inversion
    chords.append(chord)
chords.append('5  ')
chords.append('1  ')

#determine what notes are available on each beat based on chord
for beat in range(1, 17):
    chord = chords[beat]
    root = chord[0]
    notes = chordNotes[int(root)-1]
    beatNotes = beatNotes + " " + notes
#print(beatNotes)

#create bass line from bass notes in chords
for beat in range(2, 17):
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
        bNote = bNote - 7
    bNote = bNote + 7
    b.append(int(bNote))

#create soprano line from available notes and rules about notes
for beat in range(1, 60, 4):
    notes = list(beatNotes[beat:beat + 3])
    #print(notes)
    sNote = int(random.choice(notes)) + 14
    s.append(sNote)
    #determine if note breaks any rules
    while parallelFifths(s, b) == "y" or parallelFourths(s[len(s)-2:len(s)], b[len(s)-2:len(s)]) == "y" or parallelFourths(s[len(s)-2:len(s)], b[len(s)-2:len(s)]) == "y" or rangeFinder(s):
        #if it does, delete it and try again, remove note from available ones
        notes.remove(str(int(s[-1]) - 14))
        del s[-1]
        sNote = random.choice(notes)
        s.append(sNote)
        #if there are no more available notes, change the chord, rinse and repeat
        if len(notes) == 0:
            chords[len(s)-1] = random.choice(chordList) + inversionGenerator()
            chord = chords[len(s)-1]
            root = int(chord[0])
            inversion = chord[1:3]
            if inversion == "  ":
                bNote = root
            elif inversion == "6 ":
                bNote = root + 2
            else:
                bNote = root + 4
            if bNote >= 8:
                bNote = bNote - 7
            bNote = bNote + 7
            b[len(s) - 1] = (int(bNote))
    #print(s)				
    #print(s[len(s)-2:len(s)+1],b[len(s)-2:len(s)])

print(s)
print(a)
print(t)
print(b)
#print(chords)
#print(beatNotes)
