from chunk import *
import probabilityhelpers as ph
import rhythms as rhy
import random
from constants import *
import music21helpers as mh
import scale as sc
from collections import OrderedDict

p_cell_dict = {}
p_cell_dict[SCALEWISE] = 0.7
p_cell_dict[REP_PATTERN] = 0
p_cell_dict[CHORDAL] = 0.3


#generate scalewise cells
def genScalewiseCell(length, prev_note = 0, first_note = None, chord = [], durs = [], name = 'c'):
    if durs == []:
        rhythm = rhy.randomDuration(length)
    else:
        rhythm = durs
    direction = 1
    if first_note != None:
        pitches = [first_note]
    else:
        if chord == []:
            pitches = [prev_note + random.choice([1,-1])]
        else:
            pitches = [sc.closestNoteDegreeInChord(prev_note, chord, True, 0)]
    for i in range(1, len(rhythm)):
        direction = direction if random.uniform(0,1) < 0.7 else direction * -1
        if pitches[i - 1] > 14:
            direction = -1
        elif pitches[i - 1] < 0:
            direction = 1
        pitches.append(pitches[i - 1] + direction)
    if pitches[-1] > 0 and pitches[-1] < 14:
        return Chunk(sub_chunks = None, pits = pitches, durs = rhythm, ctype = SCALEWISE, name=name)
    elif pitches[-1] <= 0:
        return genScalewiseCell(length, prev_note + 1, first_note, chord, durs, name)
    else:
        return genScalewiseCell(length, prev_note - 1, first_note, chord, durs, name)


#get random next degree
def randomNextDegree(prev_note, up_down):
    direction = up_down if random.uniform(0,1) < 0.63 else up_down * -1
    new_note = prev_note + 1*direction
    return new_note

#gen next chord note up or down a certain amount
def getNthChordNote(prev_note, cord, up_down, how_many):
    if prev_note + up_down*2 > 14:
        up_down = -1
    elif prev_note < 0:
        up_down == 1
    n = 0
    while n < how_many:
        prev_note += up_down
        if prev_note % 7 in [i % 7 for i in cord]:
            n += 1
    return prev_note
    

#get a random chord note
def randomChordNote(prev_note, cord, per_up = '0.5'):
    upOrDown = 1 if random.uniform(0,1) < per_up else -1
    how_many = ph.probDictToChoice({0:0.05, 1:0.95})
    if prev_note >= 10:
        upOrDown = -1
    if prev_note >= 14:
        upOrDown = -1
        how_many = 2
    if prev_note < 0:
        upOrDown = 1
    if abs(getNthChordNote(prev_note, cord, upOrDown, how_many) - prev_note) > 3:
        print('upOrDown = ' + str(upOrDown) + ' how_many = ' + str(how_many) + ' prev_note = ' + str(prev_note) + ' chord = ' + str(cord) + ' next note is ' + str(getNthChordNote(prev_note, cord, upOrDown, how_many)))
    return getNthChordNote(prev_note, cord, upOrDown, how_many)

#generate chordal cells
def genChordalCell(length, prev_note = 0, first_note = None, cord = [], durs = [], name = 'c'):
    pitches = []
    def strToNum(string):
        return [int(i) for i in string.split()]
    if cord == []:
        cord = strToNum(ph.probDictToChoice({'0 2 4':0.5, '4 6 8':0.3, '3 5 7':0.2}))
    if durs == []:
        durs = rhy.randomDuration(length)
    if first_note != None:
        pitches = [first_note]
    else:
        pitches = [sc.closestNoteDegreeInChord(prev_note, cord, 1, False)]
    for i in range(1, len(durs)):
        """if tot_durs[i] % 1.0 == 0:
            pitches.append(randomChordNote(prev_note, cord, up_down))
        elif random.uniform(0,1) < 0.3:
            pitches.append(randomChordNote(prev_note, cord, up_down))
        elif i > 0 and durs[i - 1] == 1.5 and random.uniform(0,1) < 7:
            pitches.append(randomChordNote(prev_note, cord, up_down))
        else:
            pitches.append(randomNextDegree(prev_note, 1))"""
        pitches.append(randomChordNote(prev_note, cord))
        prev_note = pitches[-1]
    if pitches[-1] > 0 and pitches[-1] < 14:
        return Chunk(sub_chunks = None, pits = pitches, durs = durs, ctype = CHORDAL, harm = cord, name=name)
    else:
        if pitches[-1] < 0:
            return genScalewiseCell(length, prev_note + 1, first_note, cord, durs, name)
        else:
            return genScalewiseCell(length, prev_note - 1, first_note, cord, durs, name)


def fitsProg(pitches, chord):
    return True

#generate chordal cells
def genUsualCell(length, prev_note = 0, first_note = None, cord = [], durs = [], name = 'c'):
    pitches = []
    def strToNum(string):
        return [int(i) for i in string.split()]
    if cord == []:
        cord = strToNum(ph.probDictToChoice({'0 2 4':0.5, '4 6 8':0.3, '3 5 7':0.2}))
    if durs == []:
        durs = rhy.randomDuration(length)
    if first_note != None:
        pitches = [first_note]
    else:
        pitches = [sc.closestNoteDegreeInChord(prev_note, cord, 1, False)]
    tot_durs = [sum(durs[:i]) for i in range(0, len(durs))]
    for i in range(1, len(durs)):
        if tot_durs[i] % 1.0 == 0:
            pitches.append(randomChordNote(prev_note, cord))
        elif random.uniform(0,1) < 0.3:
            pitches.append(randomChordNote(prev_note, cord))
        elif i > 0 and durs[i - 1] == 1.5 and random.uniform(0,1) < .7:
            pitches.append(randomChordNote(prev_note, cord))
        else:
            pitches.append(randomNextDegree(prev_note, 1))
        prev_note = pitches[-1]
    if pitches[-1] > 0 and pitches[-1] < 14 and fitsProg(pitches, cord):
        return Chunk(sub_chunks = None, pits = pitches, durs = durs, ctype = CHORDAL, harm = cord, name = name)
    else:
        if pitches[-1] < 0:
            return genUsualCell(length, prev_note + 1, first_note, cord, durs, name=name)
        else:
            return genUsualCell(length, prev_note - 0, first_note, cord, durs, name=name)



#get any type of cell
def getCell(length, prev_note = 0, first_note = None, chord = [], durs = [], cell_type = None, name = ''):
    if cell_type == None:
        cell_type = ph.probDictToChoice(p_cell_dict)
    if cell_type == SCALEWISE:
        return genScalewiseCell(length, prev_note, first_note, chord, durs, name)
    elif cell_type == CHORDAL:
        return genChordalCell(length, prev_note, first_note, chord, durs, name)
    else:
        return genChordalCell(length, prev_note, first_note, chord, durs, name)
    #elif cell_type == USUAL:
    #    return genUsualCell(length, prev_note, first_note, chord, durs)


cells = []
for i in range(0, 10):
    prev_note = 0
    cadence = [[0,2,4],[0,2,4], [3,5,7],[3,5,7],[4,6,8],[4,6,8],[0,2,4],[0,2,4]]
    for j in range(0, 8):
        cells.append((str(8*i+j), getCell(2, prev_note, None, cadence[j], [])))
        prev_note = cells[-1][1].pits[-1]

cells = OrderedDict(cells)
chunk = Chunk(sub_chunks = cells)
mh.writeChunk([chunk], 'test1.xml')

a = getCell(2, 0, 0, [0,2,4], [1,0.5,0.5], CHORDAL)
b = getCell(2, 0, 0, [0,2,4], [1,0.5,0.25, 0.25], SCALEWISE)
subs = {}
subs['a'] = a
subs['b'] = b
y = Chunk(sub_chunks=subs)