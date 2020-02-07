#c2 = 1
#c3 = 8
#c4 = 15
#c5 = 22
#an increase by one integer = movement up by one note name

import turtle
import time
import random
from collections import namedtuple
#from midiutil import MIDIFile



#create midi file with four voices
#mf = MIDIFile(4)
#soprano = 0
#alto = 1
#tenor = 2
#bass = 3



noteList = ''
beatNotes = []
moreNotes = []
chords = ['00']
chordNotes = ["024", "135", "246", "350", "461", "502", "613"]
s = ["s", 21]
a = ["a", 16]
t = ["t", 11]
b = ["b", 7]



def findInterval(voice1, voice2):
    interval = (voice1 - voice2) % 7
    return(interval)

#determine if two notes violate parallel fourths
def parallelFourths(voice1, voice2, beat):
    parallelFourths = "n"
    if findInterval(voice1[beat], voice2[beat]) == 3:
        if findInterval(voice1[beat], voice2[beat]) == 3:	#if the second two notes are a fifth
            parallelFourths = "y"
    return(parallelFourths)
    
# check for parallel octaves
def parallelOctaves(voice1, voice2, beat):
    parallelOctaves = "n"
    if findInterval(voice1[beat], voice2[beat]) == 0:
        if findInterval(voice1[beat], voice2[beat]) == 0:
            if voice1[beat - 1] != voice1[beat] and voice2[beat - 1] != voice2[beat]:
                if (voice1[beat - 1] > voice1[beat] and voice2[beat - 1] > voice2[beat]) or (voice1[beat - 1] < voice1[beat] and voice2[beat - 1] < voice2[beat]):
                    parallelOctaves = "y"
    return(parallelOctaves)    

# check for parallel fifths
def parallelFifths(voice1, voice2, beat):
    parallelFifths = "n"
    if findInterval(voice1[beat], voice2[beat]) == 4:
        if findInterval(voice1[beat - 1], voice2[beat - 1]) == 4:
            parallelFifths = "y"
    return(parallelFifths)

# check if the voice is within the correct range
def inRange(voice, note):
    inRange = "n"
    if voice == "s":
        if note > 26 or note < 14:
            inRange = "y"
    elif voice == "a":
        if note > 22 or note < 11:
            inRange = "y"
    elif voice == "t":
        if note > 18 or note < 7:
            inRange = "y"
    else:
        if note > 16 or note < 2:
            inRange = "y"
    return(inRange)

# see if a voice is too far away from another voice
def spacing(voice1, voice2, beat):
    spacing = "n"
    if voice1[0] == 't':
        if abs(voice1[beat] - voice2[beat]) > 9:
            spacing = "y"        
    elif voice1[0] == "s" and voice2[0] == "b":
        if abs(voice1[beat] - voice2[beat]) > 23:
            spacing = "y"
    else:
        if abs(beat - voice2[beat]) > 7:
            spacing = "y"
    return(spacing)

# check for voice crossing
def voiceCrossing(voice1, voice2):
    crossing = "n"
    voice1a = voice1[beat - 1]
    voice2a = voice1[beat - 1]
    voice1b = voice1[beat]
    voice2b = voice2[beat]
    if voice1a < voice2b or voice2a > voice1b:
        crossing = "y"
    return(crossing)

#two leaps in a row

#dont double leading tone (b)

#try to weight nearest chord tones, yikes thats gonna suck

#similar motion -> perfect w/o step in soprano



#create random chord progression
def randChord():
    inversion = str(random.randrange(0,3))
    chord = str(random.randrange(0,7))
    chord = chord + inversion
    return(chord)
    
#determine what notes are available on each beat based on chord
def findNotes(beat):
    chord = str(chords[beat])
    root = int(chord[0])
    notes = chordNotes[root]
    return(notes)

#create bass line from bass notes in chords
def bassNote(beat):
    chord = chords[beat]
    root = int(chord[0])
    inversion = chord[1]
    if inversion == "0":
        bNote = root
    elif inversion == "1":
        bNote = root + 2
    else:
        bNote = root + 4
    return(bNote)

#choose a note for the soprano voice on a specific beat
def closestNote(voice1, beat):
    notes = list(map(int, list(beatNotes[beat])))
    for x in notes:
        moreNotes.append(x)
    for x in notes:
        moreNotes.append(x + 7)
    closestNote = moreNotes[0]
    voice1 = voice1 % 7
    for x in moreNotes:
        if findInterval(voice1, x) <= findInterval(closestNote, voice1):
            closestNote = x
    del moreNotes[:]
    return(closestNote)

def bassVoice(beat):    
    bNote = bassNote(beat)
    if inRange(b, bNote) == "y":
        bNote = bNote + 7
    if bNote <= 4:
        bNote = bNote + 7
    return(bNote)



#creates chord progression
for beat in range(2,16):
    chord = randChord()
    chords.append(chord)
chords.append('40')
chords.append('00')

#available notes on each beat
for beat in range(0, 17):
    notes = findNotes(beat)
    beatNotes.append(notes)

#bass voice    
for beat in range(2, 17):
    b.append(bassVoice(beat))
 
#soprano voice    
for beat in range(2, 17):
    sNote = closestNote(s[beat - 1], beat) + 14
    s.append(sNote)
    while parallelFourths(s, b, beat) == "y" or parallelFifths(s, b, beat) == "y" or parallelOctaves(s, b, beat) == "y" or inRange("s", s[beat]) == "y" or spacing(s, b, beat) == "y":
        notes = list(beatNotes[beat])
        notes.remove(str(sNote % 7))
        noteList = ''
        for note in notes:
            noteList = noteList + note
        beatNotes[beat] = noteList
        del s[-1]
        if len(beatNotes[beat]) == 0:
            chords[beat] = randChord()
            beatNotes[beat] = findNotes(beat)
            b[beat] = bassVoice(beat)
        sNote = closestNote(s[beat - 1], beat) + 14
        s.append(sNote)
    beatNotes[beat] = findNotes(beat)
    
#tenor voice
for beat in range(2, 17):
    tNote = closestNote(t[beat - 1], beat)
    t.append(tNote)
    while parallelFifths(t, b, beat) == "y" or parallelOctaves(t, b, beat) == "y" or inRange("t", t[beat]) == "y" or spacing(t, b, beat) == "y":
        notes = list(beatNotes[beat])
        notes.remove(str(tNote % 7))
        noteList = ''
        for note in notes:
            noteList = noteList + note
        beatNotes[beat] = noteList
        del t[-1]
        tNote = closestNote(t[beat - 1], beat)
        t.append(tNote)
    beatNotes[beat] = findNotes(beat)

#alto voice
for beat in range(2, 17):
    aNote = closestNote(a[beat - 1], beat) + 7
    a.append(aNote)
    while parallelFifths(a, t, beat) == "y" or parallelOctaves(a, t, beat) == "y" or inRange("a", a[beat]) == "y" or spacing(a, t, beat) == "y":
        notes = list(beatNotes[beat])
        print(notes)
        notes.remove(str(aNote % 7))
        noteList = ''
        for note in notes:
            noteList = noteList + note
        beatNotes[beat] = noteList
        del a[-1]
        aNote = closestNote(a[beat - 1], beat) + 7
        a.append(aNote)
    beatNotes[beat] = findNotes(beat)
 	
print(s)
print(a)
print(t)
print(b)
print(chords)


#        if parallelFourths(s, b, beat) == "y":
 #           print("fourths")
  #      elif parallelFifths(s, b, beat) == "y":
   #         print("fifths")
    #    elif parallelOctaves(s, b, beat) == "y":
     #       print("octaves")
      #  elif inRange("s", s[beat]) == "y":
       #     print("range", sNote)
        #elif spacing(s, b, beat) == "y":
     #       print("spacing")
      #  else:
        #    print("good")
        
turtle.shape("circle")
turtle.speed(10.5)
turtle.penup()
turtle.forward(-400)
turtle.right(-90)
turtle.forward(100)
turtle.right(90)
turtle.pendown()
for x in range(5):
    turtle.forward(800)
    turtle.penup()
    turtle.right(90)
    turtle.forward(20)
    turtle.right(-90)
    turtle.forward(-800)
    turtle.pendown()
turtle.penup()
turtle.right(90)
turtle.forward(50)
turtle.right(-90)
turtle.pendown()
for x in range(5):
    turtle.forward(800)
    turtle.penup()
    turtle.right(90)
    turtle.forward(20)
    turtle.right(-90)
    turtle.forward(-800)
    turtle.pendown()
turtle.penup()
turtle.right(-90)
turtle.forward(20)
for x in range(5):
    turtle.pendown()
    turtle.forward(230)
    turtle.penup()
    turtle.forward(-230)
    turtle.right(90)
    turtle.forward(200)
    turtle.right(-90)
turtle.right(-90)
turtle.forward(980)
turtle.right(90)
turtle.forward(-40)
def upperTurtleNote(voice, beat):
    turtle.forward(30)
    turtle.forward(10 * voice[beat])
    turtle.stamp()
    turtle.right(90)
    if voice == s or voice == t:
        turtle.forward(10)
    else:
        turtle.forward(-10)
    turtle.right(-90)
    if voice == s or voice == t:
        turtle.forward(70)
    else:
        turtle.forward(-70)
    turtle.pendown()
    if voice == s or voice == t:
        turtle.forward(-70)
    else:
        turtle.forward(70)
    turtle.penup()
    turtle.right(90)
    if voice == s or voice == t:
        turtle.forward(-10)
    else:
        turtle.forward(10)
    turtle.right(-90)
    turtle.forward(-10 * voice[beat])
    turtle.forward(-30)
def lowerTurtleNote(voice, beat):
    turtle.forward(10 * voice[beat])
    turtle.stamp()
    turtle.right(90)
    if voice == s or voice == t:
        turtle.forward(10)
    else:
        turtle.forward(-10)
    turtle.right(-90)
    if voice == s or voice == t:
        turtle.forward(70)
    else:
        turtle.forward(-70)
    turtle.pendown()
    if voice == s or voice == t:
        turtle.forward(-70)
    else:
        turtle.forward(70)
    turtle.penup()
    turtle.right(90)
    if voice == s or voice == t:
        turtle.forward(-10)
    else:
        turtle.forward(10)
    turtle.right(-90)
    turtle.forward(-10 * voice[beat])
for beat in range(1, 17):
    upperTurtleNote(s, beat)
    upperTurtleNote(a, beat)
    lowerTurtleNote(t, beat)
    lowerTurtleNote(b, beat)
    turtle.right(90)
    turtle.forward(50)
    turtle.right(-90)
turtle.forward(10000)

turtle.mainloop()
