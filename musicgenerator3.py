from collections import namedtuple
import random
import os
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
voiceError = ''


def parallelFourths(voice1, voice2, beat):
    parallelFourths = "go"
    if voice1.notes[beat] - voice2.notes[beat] == 3:
        if voice1.notes[beat - 1] - voice2.notes[beat - 1] == 3:
            if voice1.notes[beat - 1] != voice1.notes[beat] and voice2.notes[beat - 1] != voice2.notes[beat]:
                if (voice1.notes[beat - 1] > voice1.notes[beat] and voice2.notes[beat - 1] > voice2.notes[beat]) or (
                        voice1.notes[beat - 1] < voice1.notes[beat] and voice2.notes[beat - 1] < voice2.notes[beat]):
                    parallelFourths = "no"
    return (parallelFourths)


def parallelFifths(voice1, voice2, beat):
    parallelFifths = "go"
    if voice1.notes[beat] - voice2.notes[beat] == 4:
        if voice1.notes[beat - 1] - voice2.notes[beat - 1] == 4:
            if voice1.notes[beat - 1] != voice1.notes[beat] and voice2.notes[beat - 1] != voice2.notes[beat]:
                if (voice1.notes[beat - 1] > voice1.notes[beat] and voice2.notes[beat - 1] > voice2.notes[beat]) or (
                        voice1.notes[beat - 1] < voice1.notes[beat] and voice2.notes[beat - 1] < voice2.notes[beat]):
                    parallelFifths = "no"
    return (parallelFifths)


def parallelOctaves(voice1, voice2, beat):
    parallelOctaves = "go"
    if voice1.notes[beat] - voice2.notes[beat] == 7:
        if voice1.notes[beat - 1] - voice2.notes[beat - 1] == 7:
            parallelOctaves = "no"
    return (parallelOctaves)


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
    return (inRange)


def spacing(voice1, voice2, beat):  # voice1 is above voice2 btw
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
    return (spacing)


def twoLeaps(voice, beat):
    leap = "go"
    if abs(voice.notes[beat - 2] - voice.notes[beat - 1]) > 3:
        if abs(voice.notes[beat - 1] - voice.notes[beat]) > 3:
            leap = "no"
    return (leap)


def voiceCrossing(voice1, voice2, beat):
    crossing = "go"
    if voice1.notes[beat] < voice2.notes[beat - 1]:
        crossing = "no"
    if voice2.notes[beat] > voice1.notes[beat - 1]:
        crossing = "no"
    if voice1.notes[beat] < voice2.notes[beat]:
        crossing = "no"
    return (crossing)


def doubling(beat):
    doubling = "go"
    doubledVoices = 0
    if s.notes[beat] % 7 == a.notes[beat] % 7:
        doubledVoices += 1
    if s.notes[beat] % 7 == t.notes[beat] % 7:
        doubledVoices += 1
    if s.notes[beat] % 7 == b.notes[beat] % 7:
        doubledVoices += 1
    if a.notes[beat] % 7 == t.notes[beat] % 7:
        doubledVoices += 1
    if a.notes[beat] % 7 == b.notes[beat] % 7:
        doubledVoices += 1
    if t.notes[beat] % 7 == b.notes[beat] % 7:
        doubledVoices += 1
    if doubledVoices > 1:
        doubling = 'no'
    return (doubling)


def randChord():
    inversion = str(random.randrange(3))
    chord = str(random.randrange(7))
    chord = chord + inversion
    return (chord)


def cadence():
    aCadence = cadences[random.randrange(3)]
    if aCadence == 'AC':
        chords.chords.extend(('4' + str(random.randrange(2)), '0' + str(random.randrange(2))))
    elif aCadence == 'HC':
        chords.chords.extend((randChord(), '4' + str(random.randrange(2))))
    elif aCadence == 'P':
        chords.chords.extend(('3' + str(random.randrange(2)), '0' + str(random.randrange(2))))
    else:
        chords.chords.extend(('4' + str(random.randrange(2)), '3' + str(random.randrange(2))))
    return (aCadence)


def findNotes(beat):
    chord = chords.chords[beat]
    root = int(chord[0])
    notes = chordNotes[root]
    return (notes)


def findMoreNotes(voice, beat):
    notes = list(beatNotes[beat])
    octave = int(voice.notes[beat - 1] / 7)
    moreNotes = []
    for x in notes:
        moreNotes.append(int(x) + octave * 7)
    for x in notes:
        moreNotes.append(int(x) + 7 + octave * 7)
    return (moreNotes)


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
    return (bass)


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
    return (closestNote)


def soprano(beat):
    global voiceError
    notes = findMoreNotes(s, beat)
    sNote = closestNote(s, beat, notes)
    s.notes.append(sNote)
    while parallelFourths(s, b, beat) == "no" or parallelFifths(s, b, beat) == "no" or parallelOctaves(s, b,
                                                                                                       beat) == "no" or spacing(
            s, b, beat) == "no" or inRange(s, beat) == "no":
        notes.remove(s.notes[-1])
        del s.notes[-1]
        if len(notes) == 0:
            voiceError = 's'
            return ('no')
        notesLeft = ''
        for note in notes:
            if notesLeft.find(str(note % 7)) == -1:
                notesLeft += str(note % 7)
        beatNotes[beat] = notesLeft
        sNote = closestNote(s, beat, notes)
        s.notes.append(sNote)


def tenor(beat):
    global voiceError
    notes = findMoreNotes(t, beat)
    tNote = closestNote(t, beat, notes)
    t.notes.append(tNote)
    while parallelFifths(t, b, beat) == "no" or parallelFifths(s, t, beat) == "no" or parallelOctaves(t, b,
                                                                                                      beat) == "no" or parallelOctaves(
            s, t, beat) == "no" or spacing(t, b, beat) == "no" or inRange(t, beat) == "no" or voiceCrossing(t, b,
                                                                                                            beat) == 'no':
        notes.remove(t.notes[-1])
        del t.notes[-1]
        if len(notes) == 0:
            voiceError = 't'
            return ('no')
        notesLeft = ''
        for note in notes:
            if notesLeft.find(str(note % 7)) == -1:
                notesLeft += str(note % 7)
        beatNotes[beat] = notesLeft
        tNote = closestNote(t, beat, notes)
        t.notes.append(tNote)


def alto(beat):
    global voiceError
    notes = findMoreNotes(a, beat)
    alto = closestNote(a, beat, notes)
    a.notes.append(alto)
    while parallelFifths(a, b, beat) == "no" or parallelFifths(a, t, beat) == "no" or parallelFifths(s, a,
                                                                                                     beat) == "no" or parallelOctaves(
            a, b, beat) == "no" or parallelOctaves(a, t, beat) == "no" or parallelOctaves(s, a,
                                                                                          beat) == "no" or spacing(a, t,
                                                                                                                   beat) == "no" or spacing(
            s, a, beat) == "no" or inRange(a, beat) == "no" or voiceCrossing(s, a, beat) == 'no' or voiceCrossing(a, t,
                                                                                                                  beat) == 'no' or doubling(
            beat) == 'no':
        notes.remove(a.notes[-1])
        del a.notes[-1]
        if len(notes) == 0:
            voiceError = 'a'
            return ('no')
        notesLeft = ''
        for note in notes:
            if notesLeft.find(str(note % 7)) == -1:
                notesLeft += str(note % 7)
        beatNotes[beat] = notesLeft
        alto = closestNote(a, beat, notes)
        a.notes.append(alto)


def fourBars():
    global voiceError
    for beat in range(1, 13):
        chords.chords.append(randChord())
    cadence()

    for beat in range(1, 15):
        counter = 0
        beatNotes.append(findNotes(beat))
        b.notes.append(bass(beat))
        voiceError = ''
        while soprano(beat) == 'no' or tenor(beat) == 'no' or alto(beat) == 'no' and counter < 200:
            counter += 1
            if beat < 13:
                chords.chords[beat] = randChord()
                b.notes[beat] = bass(beat)
            beatNotes[beat] = findNotes(beat)
            if voiceError == 't':
                del s.notes[beat]
            elif voiceError == 'a':
                del s.notes[beat]
                del t.notes[beat]
            if counter > 100:
                break
        if counter >= 100:
            return ('no')
    s.notes.append(s.notes[-1])
    a.notes.append(a.notes[-1])
    t.notes.append(t.notes[-1])
    b.notes.append(b.notes[-1])
    chords.chords.append(chords.chords[-1])
    return('yes')


while fourBars() == 'no':
    del beatNotes[1:]
    del s.notes[1:]
    del a.notes[1:]
    del t.notes[1:]
    del b.notes[1:]
    del chords.chords[1:]

def translator(inputList):
    newList = []
    for x in inputList:
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
        degree2 = int(x) - int(x % 7)
        octave = (degree2 / 7)
        newNote = 36 + (octave * 12) + degree  # c0 plus extra octave plus octave generated plus degree
        newNote = int(newNote)
        newList = newList + [newNote]
    return (newList)


def letterNote(list):
    newList = []
    for x in list:
        noteFinder = x % 7
        if noteFinder == 0:
            degree = 'C'  # c
        elif noteFinder == 1:
            degree = 'D'  # d
        elif noteFinder == 2:
            degree = 'E'  # e
        elif noteFinder == 3:
            degree = 'F'  # f
        elif noteFinder == 4:
            degree = 'G'  # g
        elif noteFinder == 5:
            degree = 'A'  # a
        else:
            degree = 'B'  # b
        newList = newList + [degree]
    print(newList)


def halfNoteAddition(inputlist):
    newList = []
    for note in inputlist:
        newList = newList + [note]
    listlength = len(newList)
    newList.pop(listlength - 1)
    return (newList)

def findEnding(inputlist):
    return (inputlist.pop())

def export():
    filename = input("Write desired filename here!")
    checker = bool(filename.find(".mid"))
    if checker == False:
        filename = (str(filename) + (".mid"))
        print(filename)
    MIDI = str(filename)
    checker = MIDI.find('.mid')
    if checker != False:
        MIDI = (MIDI + ".mid")
    with open(MIDI, "wb") as output_file:
        MyMIDI.writeFile(output_file)
    path = os.path.abspath(MIDI)
    print(path)
    os.startfile(path)



sList = translator(s.notes)
aList = translator(a.notes)
tList = translator(t.notes)
bList = translator(b.notes)
letterNote(s.notes)
letterNote(a.notes)
letterNote(t.notes)
letterNote(b.notes)
sList = halfNoteAddition(sList)
sEnding = [findEnding(sList)]
tList = halfNoteAddition(tList)
tEnding = [findEnding(tList)]
aList = halfNoteAddition(aList)
aEnding = [findEnding(aList)]
bList = halfNoteAddition(bList)
bEnding = [findEnding(bList)]

time = 0
duration = 1
channel = 0
tempo = 100
volume = 100
MyMIDI = MIDIFile(2)
MyMIDI.addTempo(1, time, tempo)
bVerify = "no"
sVerify = "no"
aVerify = "no"
tVerify = "no"

MyMIDI = MIDIFile(2)
MyMIDI.addTempo(1, time, tempo)

for pitch in bList:
    if time != 0 and bVerify == "no":
        time = 0
    MyMIDI.addNote(1, channel, pitch, time, duration, volume)
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
    MyMIDI.addNote(0, channel, pitch, time, duration, volume)
    time = time + 1
    aVerify = "go"
for pitch in tList:
    if time != 0 and tVerify == "no":
        time = 0
    MyMIDI.addNote(1, channel, pitch, time, duration, volume)
    time = time + 1
    tVerify = "go"
for pitch in sEnding:
    MyMIDI.addNote(0, channel, pitch, time, 2, volume)
for pitch in aEnding:
    MyMIDI.addNote(0, channel, pitch, time, 2, volume)
for pitch in tEnding:
    MyMIDI.addNote(1, channel, pitch, time, 2, volume)
for pitch in bEnding:
    MyMIDI.addNote(1, channel, pitch, time, 2, volume)

export()