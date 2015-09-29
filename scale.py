# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 07:54:25 2014

@author: halley
"""
from constants import *
from operator import itemgetter
import random
import probabilityhelpers as ph
import functionalhelpers as fh

scales = {}
scales['major'] = [0,2,4,5,7,9,11]

#used for determining a random pitch movement
horizontalmarkov = {0:1, 1:20, 2:8, 3:2, 4:1}

#convert pitches to scale degrees, given a scale
def pitchesToDegrees(pitches, scale=scales['major'], octave=5):
    degs = []
    for pitch in pitches:
        for i in range(0, len(scale)):
            if pitch%12 == (scale[i])%12:
                degs.append(i + (pitch/12 - octave)*7)
                break
            elif pitch % 12 > scale[i] and i == len(scale) - 1:
                degs.append(i + .5 + (pitch/12 - octave)*7)
            elif pitch%12 > scale[i] and pitch%12 < scale[i+1]:
                degs.append(i + .5 + (pitch/12 - octave)*7)
    return degs

#returns numerical notes in scale        
def notesInScale(scale=scales["major"], octave=4, startkey=0):
    return map(lambda i: i + (12*octave) + startkey, scale)
    
#get nth note of a scale
def getNote(nindex, scale=scales["major"], octave=4, startkey=0):
    return notesInScale(scale, octave, startkey)[nindex]

#given array xs, give pitches x1...xn of scale
def getNotes(nindices, octaves, scale=scales["major"], startkey=0):
    notes = []
    for note in nindices:
        notes.extend(map(lambda i: getNote(note, scale=scale, octave = i, startkey=startkey), octaves))
    return notes

#get the triad starting at scaleDeg n of scale
def triad(scaleDeg, scale=scales["major"], octave = 0):
    return [scale[scaleDeg], scale[(scaleDeg + 2) % 7] + 12*((scaleDeg + 2)/7), scale[(scaleDeg + 4) % 7] + 12*((scaleDeg + 4)/7)]

#get the interval between pitch1 and pitch2
def getInterval(pitch1, pitch2):
    return pitch2 - pitch1

#returns whether the interval between pitch1 and pitch2 is dissonant
def isDissonant(pitch1, pitch2):
    return abs(getInterval(pitch1, pitch2)) in intervals["dissonant"].values()
    
#get closest note in a chord to a given note
def closestNoteInTriad(note, chord):
    allnotes = getNotess([chord, ((chord+2)%7), ((chord+4)%7)], range(3,7))
    dChords = map(lambda i: abs(note - i), allnotes)
    minindex = min(enumerate(dChords), key=itemgetter(1))[0] 
    return allnotes[minindex]

#get closest scale degree in triad to a given scale degree
def closestNoteDegreeInTriad(note, chord):
    allnotes = fh.concat([[i,i+2,i+4]  for i in range(-14,14,7)])
    dChords = map(lambda i: abs(note - i), allnotes)
    minindex = min(enumerate(dChords), key=itemgetter(1))[0] 
    return allnotes[minindex]

#get closest scale degree in chord to a given scale degree
def closestNoteDegreeInChord(note, chord, same = True, up_down = 0):
    allnotes = fh.concat([map(lambda j: i + j, chord) for i in range(-14,14,7)])
    tmp_allnotes = allnotes
    if up_down == 1:
        allnotes = filter(lambda i: i >= note, allnotes)
    elif up_down == -1:
         allnotes = filter(lambda i: i <= note, allnotes)
    if allnotes == [] and up_down == 1:
        allnotes = [tmp_allnotes[-1]]
    elif allnotes == [] and up_down == -1:
        allnotes = [tmp_allnotes[0]]
    dChords = map(lambda i: abs(note - i), allnotes)
    if same:
        minindex = min(enumerate(dChords), key=itemgetter(1))[0] 
        return allnotes[minindex]
    else:
        minnotsameindex = -1
        minnotsame = 1000
        for i in range(0, len(dChords)):
            if dChords[i] != 0 and dChords[i] < minnotsame:
                minnotsame = dChords[i]
                minnotsameindex = i
        return allnotes[minnotsameindex]

#get notes octave
def getOctave(note):
    return (note/12)
    
#get pitchclass
def getPitchClass(note):
    return (note % 12)

#find out what index the note is in the scale
def getNoteIndex(note, scale=scales["major"], key=0):
    for i in range(0, len(scale)):
        if (note%12) == scale[i]:
            return i
    return -1
    
#get note from previous notes and intervals    
def noteAtInterval(startnote, interval, scale=scales["major"], key=0):
    nindex = getNoteIndex(startnote) #index of startnote in scale
    if nindex + interval >= len(scale):
        return (getOctave(startnote)+1)*12 + scale[(nindex + interval) % 7]
    elif nindex + interval < 0:
        return (getOctave(startnote)-1)*12 + scale[(nindex + interval) % 7]
    else:
        return startnote + scale[nindex + interval] - scale[nindex]

#get a list of intervals between notes
def getIntervals(notes, scale=scales["major"]):
    intervals = []
    for i in range(1, len(notes)):
        ind1 = scale.index(notes[i-1]  % 12)
        ind2 = scale.index(notes[i]  % 12)
        intervals.append(ind2 - ind1)
    return intervals
    
#convert intervals to notes given intervals and startnote
def intervalsToNotes(start_note, intervals):
    notes = [start_note]
    for i in range(0, len(intervals)):
        noteNew = noteAtInterval(notes[i], intervals[i])
        if (noteNew % 12) in scales["major"]:
            notes.append(noteNew)
        else:
            print("error")
            notes.append(noteNew + random.choice([1,-1]))
    return notes
    
#convert scale degrees, octaves, scales to midi pitches
def degreesToNotes(degrees, octave = 5, scale=scales["major"]):
    notes = []
    for degree in degrees:
        if type(degree) == tuple:
            return tuple(degreesToNotes(list(degree), octave, scale))
        elif degree % 1.0 == 0:
            notes.append((octave+(degree/7))*12 + scale[int(degree % 7)])
        else:
            degree = int(degree)
            notes.append((octave+(degree/7))*12 + scale[int(degree % 7)] + 1)
    return notes

def degreeToNote(degree, octave = 5, scale=scales["major"]):
    if degree % 1.0 == 0:
            return((octave+(degree/7))*12 + scale[int(degree % 7)])
    else:
            degree = int(degree)
            return((octave+(degree/7))*12 + scale[int(degree % 7)] + 1)

