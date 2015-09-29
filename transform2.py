__author__ = 'halley'
import gencell as gc
import probabilityhelpers as ph
from chunk import *
from inspect import getmembers, isfunction
import random
import preferences as pref
import transforms as tfs
import music21helpers as mh
import transformhphrase as thp
import cadence as cd
import accomp

#transform one cell to produce another cell
def transformChunk(chunk, prev_note, chords):
    #get list of transform functions
    appropriate_function_list = ['identity', 'partialTranspose', 'retrograde', 'partialRetrograde', 'subRhythm']
    functions_list = dict([(o[0], o[1]) for o in getmembers(tfs) if isfunction(o[1])]) #list of all possible transform functions
    functions_list = dict(filter(lambda i: i[0] in appropriate_function_list, functions_list.items()))
    functions_names = functions_list.keys()
    random.shuffle(functions_names)
    have_chunk = False #haven't created new cell yet
    i = 0
    while not have_chunk and i < len(appropriate_function_list): #loop until appropriate cell is found
        if chunk.depth == 2:
            print (functions_names[i])
        if chunk.depth <= 1:
            new_variations = functions_list[functions_names[i]](chunk, chords, prev_note)
        elif chunk.depth == 2:
            new_variations = thp.mapToHPhrase(functions_list[functions_names[i]],chunk, chords, prev_note)
        random.shuffle(new_variations)
        for variation in new_variations:
            if pref.fitsPref(variation, prev_note, chords):
                return variation
        i += 1
    if chunk.depth == 0:
        return gc.getCell(2, prev_note, None, chords[0], chunk.durs, chunk.ctype)
    elif chunk.depth == 1:
        cell1 = gc.getCell(2, prev_note, None, chords[0], chunk.sub_chunks[0].durs, chunk.sub_chunks[0].ctype)
        cell2 = transformChunk(cell1, cell1.pits[-1], [chords[1]])
        return Chunk([cell1, cell2])
    else:
        print('sucker')
        motif1 = genMotif(prev_note, chords[0:2])
        motif2 = transformChunk(motif1, motif1.pits[-1], chords[2:])
        return Chunk([motif1, motif2])

#get the "opposite" harmony
def getAntiHarm(harmony):
    if harmony == [0,2,4]:
        return [4,6,8]
    else:
        return [0,2,4]

#generate a single period
def genPeriod(authentic_cadence = True, first_hphrase = None):
    if first_hphrase == None:
        first_hphrase = genHPhrase(prob_transform_dict={'transformed':1.0})
    second_hphrase = cd.transformToCadence(genHPhrase(prev_note = first_hphrase.pits[-1], harmony=[[4,6,8], [4,6,8], [0,2,4], [4,6,8]], prob_transform_dict={'transformed':1.0}), cad_type = 'half')
    first_phrase = Chunk([first_hphrase, second_hphrase])
    third_hphrase = transformChunk(first_hphrase, 3, [[0,2,4], [3,5,7], [0,2,4], [4,6,8]])
    fourth_cad_type = 'authentic' if authentic_cadence == True else 'inauthentic'
    fourth_hphrase = cd.transformToCadence(transformChunk(second_hphrase, third_hphrase.pits[-1], [[0,2,4], [3,5,7], [4,6,8], [0,2,4]]), cad_type = fourth_cad_type)
    second_phrase = Chunk([third_hphrase, fourth_hphrase])
    return Chunk([first_phrase, second_phrase])

#generate a double period
def genDoublePeriod():
    first_period = genPeriod(authentic_cadence = False)
    second_period = genPeriod(authentic_cadence=True, first_hphrase=transformChunk(first_period.sub_chunks[0].sub_chunks[0], first_period.pits[-1], [[0,2,4],[0,2,4],[3,5,7], [4,6,8]]))
    return Chunk([first_period, second_period])

#gen a half phrase
def genHPhrase(prev_note = 0, harmony = [[0,2,4], [0,2,4], [4,6,8], [0,2,4]], prob_transform_dict = {'transformed':0.6, 'new':0.4}):
    first_motif = genMotif(prev_note, harmony[:2])
    next_motif_type = ph.probDictToChoice(prob_transform_dict)
    if next_motif_type == 'new':
        second_motif = genMotif(first_motif.pits[-1], harmony[2:])
    else:
        second_motif = transformChunk(first_motif, first_motif.pits[-1], harmony[2:])
    return Chunk([first_motif, second_motif])

#shift half phrase down to new harmony
def shiftHalfPhrase(hphrase, new_harmony):
    index = 0
    all_motifs = []
    above_or_below = random.choice([0,1])
    for motif in hphrase.sub_chunks:
        all_cells = []
        for cell in motif.sub_chunks:
            all_cells.append(tfs.identity(cell, [new_harmony[index]])[above_or_below])
            index += 1
        all_motifs.append(Chunk(all_cells))
    return Chunk(all_motifs)

#generate a motif
def genMotif(prev_note = 0, harmony = [[0,2,4],[4,6,8]]):
    first_chord = harmony[0]
    second_chord = harmony[1]
    #gen first cell
    cell1 = gc.getCell(2, prev_note, None, first_chord, [])
    #either gen or transform second cell
    next_cell_type = ph.probDictToChoice({'transformed':0.7, 'new':0.3})
    if len(set(cell1.durs)) < 2 and len(cell1.durs) > 1:
        next_cell_type = 'new'
    if next_cell_type == 'new':
        cell2 = gc.getCell(2, cell1.pits[-1], None, second_chord, [])
    else:
        cell2 = transformChunk(cell1, cell1.pits[-1], [second_chord])
    return Chunk([cell1, cell2])

def writeChunk(chunk, fname):
    f = open('/Users/halley/Desktop/' + fname, 'w+')
    for cell in chunk.cells:
        f.write(str(cell.pits) + '-' + str(cell.durs) + '\n')
    f.close()
"""
prev_note = 0
hphrases = []
for i in range(0,20):
    hphrases.append(genHPhrase(prev_note))
    hphrases.append(transformChunk(hphrases[-1], hphrases[-1].pits[-1], [[0,2,4],[4,6,8],[0,2,4],[4,6,8]]))
    prev_note = hphrases[-1].pits[-1]

chunk = Chunk(hphrases)
mh.writeChunk(chunk, 'test.xml')"""

periods = []
for i in range(0, 10):
    doublePeriod = genDoublePeriod()
    periods.append(doublePeriod)
mh.writeChunk([Chunk(periods)], 'periods.xml')
    #writeChunk(doublePeriod, 'test' + str(i) + '.txt')