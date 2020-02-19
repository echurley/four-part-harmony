from collections import namedtuple
import random
import turtle
from midiutil import MIDIFile

chordNotes = ["024", "135", "246", "350", "461", "502", "613"]
cadences = ['AC', 'HC', 'P', 'D']

voice = namedtuple('voice', 'part notes')
s = voice('s', [21])
a = voice('a', [16])
t = voice('t', [11])
b = voice('b', [7])
chords = namedtuple('chords', 'part chords')
chords = chords('chords', ['00'])
beatNotes = ['024']


    
def parallelFourths(voice1, voice2, beat):
    parallelFourths = "go"
    if voice1.notes[beat] - voice2.notes[beat] == 3:
        if voice1.notes[beat - 1] - voice2.notes[beat - 1] == 3:
            if voice1.notes[beat - 1] != voice1.notes[beat] and voice2.notes[beat - 1] != voice2.notes[beat]:
                if (voice1.notes[beat - 1] > voice1.notes[beat] and voice2.notes[beat - 1] > voice2.notes[beat]) or (voice1.notes[beat - 1] < voice1.notes[beat] and voice2.notes[beat - 1] < voice2.notes[beat]):
                    parallelFourths = "no"
    return(parallelFourths)
    
def parallelFifths(voice1, voice2, beat):
    parallelFifths = "go"
    if voice1.notes[beat] - voice2.notes[beat] == 4:
        if voice1.notes[beat - 1] - voice2.notes[beat - 1] == 4:
            if voice1.notes[beat - 1] != voice1.notes[beat] and voice2.notes[beat - 1] != voice2.notes[beat]:
                if (voice1.notes[beat - 1] > voice1.notes[beat] and voice2.notes[beat - 1] > voice2.notes[beat]) or (voice1.notes[beat - 1] < voice1.notes[beat] and voice2.notes[beat - 1] < voice2.notes[beat]):
                    parallelFifths = "no"
    return(parallelFifths)
    
def parallelOctaves(voice1, voice2, beat):
    parallelOctaves = "go"
    if voice1.notes[beat] - voice2.notes[beat] == 7:
        if voice1.notes[beat - 1] - voice2.notes[beat - 1] == 7:
            #if voice1.notes[beat - 1] != voice1.notes[beat] and voice2.notes[beat - 1] != voice2.notes[beat]:
               # if (voice1.notes[beat - 1] > voice1.notes[beat] and voice2.notes[beat - 1] > voice2.notes[beat]) or (voice1.notes[beat - 1] < voice1.notes[beat] and voice2.notes[beat - 1] < voice2.notes[beat]):
            parallelOctaves = "no"
    return(parallelOctaves)
    
def inRange(voice, beat):
    inRange = "go"
    note = voice.notes[beat]
    if voice.part == "s":
        if note > 26 or note < 14:
            inRange = "no"
    elif voice.part == "a":
        if note > 22 or note < 11:
            inRange = "no"
    elif voice.part == "t":
        if note > 18 or note < 7:
            inRange = "no"
    else:
        if note > 16 or note < 2:
            inRange = "no"
    return(inRange)
    
def spacing(voice1, voice2, beat): #voice1 is above voice2 btw
    spacing = "go"
    if voice1.part == 't':
        if (voice1.notes[beat] - voice2.notes[beat]) > 9:
            spacing = "no"        
    elif voice1.part == "s" and voice2.part == "b":
        if (voice1.notes[beat] - voice2.notes[beat]) > 23:
            spacing = "no"
    else:
        if abs(voice1.notes[beat] - voice2.notes[beat]) > 7:
            spacing = "no"
    return(spacing)
    
def twoLeaps(voice, beat):
    leap = "go"
    if abs(voice.notes[beat - 2] - voice.notes[beat - 1]) > 3:
        if abs(voice.notes[beat - 1] - voice.notes[beat]) > 3:
            leap = "no"
    return(leap)
    
def voiceCrossing(voice1, voice2, beat):
    crossing = "go"
    if voice1.notes[beat] < voice2.notes[beat - 1]:
        crossing = "no"
    if voice2.notes[beat] < voice1.notes[beat - 1]:
        crossing = "no"
    if voice1.notes[beat] < voice2.notes[beat]:
        crossing = "no"
    return(crossing)

def randChord():
    inversion = str(random.randrange(3))
    chord = str(random.randrange(7))
    chord = chord + inversion
    return(chord)
    
def cadence():
    cadence = cadences[random.randrange(3)]
    if cadence == 'AC':
        chords.chords.extend(('4' + str(random.randrange(2)), '0' + str(random.randrange(2))))
    elif cadence == 'HC':
        chords.chords.extend((randChord(), '4' + str(random.randrange(2))))
    elif cadence == 'P':
        chords.chords.extend(('3' + str(random.randrange(2)), '0' + str(random.randrange(2))))
    else:
        chords.chords.extend(('4' + str(random.randrange(2)), '3' + str(random.randrange(2))))

def findNotes(beat):
    chord = chords.chords[beat]
    root = int(chord[0])
    notes = chordNotes[root]
    return(notes)

def findMoreNotes(voice, beat):
    notes = list(beatNotes[beat])
    octave = int(voice.notes[beat - 1] / 7)
    moreNotes = []
    for x in notes:
        moreNotes.append(int(x) + octave * 7)
    for x in notes:
        moreNotes.append(int(x) + 7 + octave * 7)
    return(moreNotes)

def bass(beat):
    chord = chords.chords[beat]
    root = int(chord[0])
    inversion = chord[1]
    if inversion == "0":
        bass = root
    elif inversion == "1":
        bass = root + 2
    else:
        bass = root + 4
    if bass < 4:
        bass = bass + 7
    return(bass)

def closestNote(voice, beat, notes):
    closestNote = notes[0]
    voice = voice.notes[beat - 1]
    if beat < 8:
        for x in notes:
            if abs(voice - x) <= abs(voice - closestNote):
                closestNote = x   
    else:
        for x in notes:
            if abs(voice - x) < abs(voice - closestNote):
                closestNote = x  
    return(closestNote)
    
def soprano(beat):
    notes = findMoreNotes(s, beat)
    soprano = closestNote(s, beat, notes)
    s.notes.append(soprano)
    while parallelFourths(s, b, beat) == "no" or parallelFifths(s, b, beat) == "no" or parallelOctaves(s, b, beat) == "no" or spacing(s, b, beat) == "no" or inRange(s, beat) == "no":
        notes.remove(s.notes[-1])
        if len(notes) == 0:
            return('no')
        beatNotes[beat] = notes
        del s.notes[-1]
        soprano = closestNote(s, beat, notes)
        s.notes.append(soprano)

def tenor(beat):
    notes = findMoreNotes(t, beat)
    tenor = closestNote(t, beat, notes)
    t.notes.append(tenor)
    while parallelFifths(t, b, beat) == "no" or parallelFifths(s, t, beat) == "no" or parallelOctaves(t, b, beat) == "no" or parallelOctaves(s, t, beat) == "no" or spacing(t, b, beat) == "no" or inRange(t, beat) == "no":
        notes.remove(t.notes[-1])
        if len(notes) == 0:
            return('no')
        beatNotes[beat] = notes
        del t.notes[-1]
        tenor = closestNote(t, beat, notes)
        t.notes.append(tenor)
        
def alto(beat):
    notes = findMoreNotes(a, beat)
    alto = closestNote(a, beat, notes)
    a.notes.append(alto)
    if beat == 1:
        while parallelFifths(a, b, beat) == "no" or parallelFifths(a, t, beat) == "no" or parallelFifths(s, a, beat) == "no" or parallelOctaves(a, b, beat) == "no" or parallelOctaves(a, t, beat) == "no" or parallelOctaves(s, a, beat) == "no" or spacing(a, t, beat) == "no" or spacing(s, a, beat) == "no" or inRange(a, beat) == "no":    
            notes.remove(a.notes[-1])
            if len(notes) == 0:
                return('no')
            beatNotes[beat] = notes
            del a.notes[-1]
            alto = closestNote(a, beat, notes)
            a.notes.append(alto)
    else:
        while parallelFifths(a, b, beat) == "no" or parallelFifths(a, t, beat) == "no" or parallelFifths(s, a, beat) == "no" or parallelOctaves(a, b, beat) == "no" or parallelOctaves(a, t, beat) == "no" or parallelOctaves(s, a, beat) == "no" or spacing(a, t, beat) == "no" or spacing(s, a, beat) == "no" or inRange(a, beat) == "no" or twoLeaps(a, beat) == "no":    
            notes.remove(a.notes[-1])
            if len(notes) == 0:
                return('no')
            beatNotes[beat] = notes
            del a.notes[-1]
            alto = closestNote(a, beat, notes)
            a.notes.append(alto)



for beat in range(1, 13):
    chords.chords.append(randChord())
cadence()

for beat in range(1, 15):
    beatNotes.append(findNotes(beat))
    b.notes.append(bass(beat))
    while soprano(beat) == 'no' or tenor(beat) == 'no' or alto(beat) == 'no':
        if beat < 13:
            chords.chords[beat] = randChord()
            beatNotes[beat] = findNotes(beat)
            b.notes[beat] = bass(beat)
            print('not cadence')
        del s.notes[beat]
        del a.notes[beat]
        del t.notes[beat]
    print(beat)



def translator(RANDOMLIST):
    newList = []
    for x in RANDOMLIST:
        noteFinder = x % 7
        if noteFinder == 0:
            degree = 0  # c
        elif noteFinder == 1:
            degree = 2  # d
        elif noteFinder == 2:
            degree = 4  # e
        elif noteFinder == 3:
            degree = 5  # f
        elif noteFinder == 4:
            degree = 7  # g
        elif noteFinder == 5:
            degree = 9  # a
        else:
            degree = 11  # b
        scraped = int(x) - int(x % 7)
        octave = (scraped / 7)
        newNote = 12 + 12 +12 + (octave * 12) + degree  # c0 plus extra octave plus octave generated plus degree
        newNote = int(newNote)
        newList = newList + [newNote]
    return(newList)


sList = translator(s.notes)
aList = translator(a.notes)
tList = translator(t.notes)
bList = translator(b.notes)

# 21 = C5
# 16 = E4
# 11 = G3
# 7 = C3
# find note, then octave

bVerify = "no"
sVerify = "no"
aVerify = "no"
tVerify = "no"

time = 0
duration = 1
channel = 0
tempo = 100
volume = 100
MyMIDI = MIDIFile(4)
MyMIDI.addTempo(1, time, tempo)

for pitch in bList:
    if time != 0 and bVerify == "no":
        time = 0
    MyMIDI.addNote(3, channel, pitch, time, duration, volume)
    time = time + 1
    bVerify = "go"
for pitch in sList:
    if time != 0 and sVerify == "no":
        time = 0
    MyMIDI.addNote(0, channel, pitch, time, duration, volume)
    time = time + 1
    sVerify = "go"
for pitch in aList:
    if time != 0 and aVerify == "no":
        time = 0
    MyMIDI.addNote(1, channel, pitch, time, duration, volume)
    time = time + 1
    aVerify = "go"
for pitch in tList:
    if time != 0 and tVerify == "no":
        time = 0
    MyMIDI.addNote(2, channel, pitch, time, duration, volume)
    time = time + 1
    tVerify = "go"

with open("test1.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
