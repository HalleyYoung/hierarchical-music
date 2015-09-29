
__author__ = 'halley'
from constants import *

def inChord(note, chord):
    if chord == []:
        return True
    else:
        return (note % 7) in [i%7 for i in chord]

#check if a chunk is in a chord
def chunkInChord(chunk, chord):
    if chunk.depth == 0:
        for i in range(0, len(chunk.beat_durs), 2):
            if not inChord(chunk.beat_pits[i][0], chord):
                return False
        pits = chunk.pits
        for i in range(1, len(pits)):
            if abs(pits[i] - pits[i - 1]) > 1:
                if not (inChord(pits[i], chord) and inChord(pits[i - 1], chord)):
                    return False
        return True
    else:
        return all([chunkInChord(i, chord) for i in chunk.sub_chunks])

def getClosestAbove(note, chord):
    #print('note ' + str(note) + 'chord ' + str(chord))
    i = 1
    while (not inChord(note + i, chord)):
        i += 1
    return note + i

def getClosestBelow(note, chord):
    #print('note ' + str(note) + 'chord ' + str(chord))
    i = 1
    while (not inChord(note - i, chord)):
        i += 1
    return note - i

#find what chord matches a given cell
def getChord(cell):
    pits = cell.pits
    diffs = [abs(pits[i] - pits[i - 1]) for i in range(1, len(pits))]
    important = []
    for i in range(0, len(diffs)):
        if diffs[i] > 2:
            important.append(pits[i])
            important.append(pits[i + 1])
    if cell.ctype != SCALEWISE:
        for beat_pit in cell.beat_pits:
            important.append(beat_pit[0])
    return (-7,-5,-3)