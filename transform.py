from inspect import getmembers, isfunction
import gencell as gc
import closenessdistribution as cd
import probabilityhelpers as ph
from chunk import *
import functionalhelpers as fh
import preferences as pref
import random
import transforms as tfs
import music21helpers as mh
import harmony as hm

appropriate_function_list = ['transpose', 'inversion', 'partialTranspose', 'retrograde', 'partialRetrograde', 'subRhythm']
functions_list = dict([(o[0], o[1]) for o in getmembers(tfs) if isfunction(o[1])]) #list of all possible transform functions
functions_list = dict(filter(lambda i: i[0] in appropriate_function_list, functions_list.items()))


#create one motif from another motif
def transformMotif(motif, harm = [tuple([[0,2,4]]), ([0,2,4], [4,6,8])], prev_note = None, names = {}):
    if prev_note == None:
        prev_note = motif.pits[-1]
    if random.uniform(0,1) < 0.5: #transform entire motif
        transformed_already = []
        for function in appropriate_function_list:
            new_motifs = functions_list[function](motif, prev_note)
            transformed_already.append(random.choice(new_motifs))
        #now try transforming already transformed cells
        for transformed_once in transformed_already:
            for function in appropriate_function_list:
                new_motifs = functions_list[function](transformed_once, prev_note)
                random.shuffle(new_motifs)
                for new_motif in new_motifs:
                    for harmony in harm:
                        cells = new_motif.listCells()
                        if fitsMotifPref(cells):
                            return new_motif
    else:
        cell1 = transformCell(motif.listSubchunks()[0], harm[0], prev_note)
        cell2 = transformCell(motif.listSubchunks()[1], harm[1], cell1.pits[-1])
        cell1.name = getName(names, 'cell')
        cell2.name = getName(names, 'cell')
        new_sub_chunks = OrderedDict()
        new_sub_chunks[cell1.name] = cell1
        new_sub_chunks[cell2.name] = cell2
        return Chunk(new_sub_chunks)



#transform cell to a new cell
def transformCell(cell, harm, prev_note = None):
    if prev_note == None:
        prev_note = cell.pits[-1]
    transformed_already = []
    for function in appropriate_function_list:
        new_cells = functions_list[function](cell, prev_note)
        random.shuffle(new_cells)
        transformed_already.append(new_cells[0])
        """for new_cell in new_cells:
            for harmony in harm:
                if hm.chunkInChord(new_cell, harmony) and pref.fitsPref(new_cell, prev_note, harmony):
                    return new_cell"""
    #now try transforming already transformed cells
    for transformed_once in transformed_already:
        for function in appropriate_function_list:
            new_cells = functions_list[function](transformed_once, prev_note)
            random.shuffle(new_cells)
            for new_cell in new_cells:
                for harmony in harm:
                    if hm.chunkInChord(new_cell, harmony) and pref.fitsPref(new_cell, prev_note,harmony):
                        if random.uniform(0,1) < 0.8:
                            return random.choice(tfs.subRhythm(new_cell, prev_note, harmony, how_many=1))
                        else:
                            return new_cell
    return gc.getCell(2, prev_note, first_note = None, chord = harm[0], durs = cell.durs)

def fitsMotifPref(cells):
    if sum([sum(i.durs) for i in cells]) != 4.0:
        return False
    if cells[0].pits == cells[1].pits and cells[0].durs == cells[1].durs:
        #print('in same')
        return False
    if abs(cells[0].pits[-1] - cells[1].pits[0]) > 2:
        #print('in too far apart')
        return False
    all_pits = fh.concat([i.pits for i in cells])
    all_durs = fh.concat([i.durs for i in cells])
    if len(all_pits) > 4 and len(set(all_pits)) < 3:
        #print('in not enough pits')
        return False
    if all_durs.count(1.0) > 3:
        #print('in too many 1.0')
        return False
    if all_durs.count(2.0) > 1:
        #print('in too many 2.0')
        return False
    return True

def fitsBasicIdeaPref(motifs):
    if sum([sum(i.durs) for i in motifs]) != 8.0:
        return False
    if motifs[0].pits == motifs[1].pits and motifs[0].durs == motifs[1].durs:
        return False
    if abs(motifs[0].pits[-1] - motifs[1].pits[0]) > 2:
        return False
    all_pits = fh.concat([i.pits for i in motifs])
    all_durs = fh.concat([i.durs for i in motifs])
    if len(set(all_pits)) < 3:
        return False
    if all_durs.count(2.0) > 2:
        return False
    return True

#generate motif with particular harmony
def genMotif(prev_note = 0, harm = [tuple([[0,2,4]]), ([0,2,4], [4,6,8])], nameA = 'cell', nameB = 'cell', name = 'motif', names = {}):
    #print('harm = ' + str(harm))
    #print('harm[0] = ' + str(harm[0]))
    #print('harm[0][0] ' + str(harm[0][0]))
    cell1 = gc.getCell(length=2, prev_note=prev_note, first_note = None, chord=harm[0][0], durs=[])
    cell1.name = getName(names, nameB)
    prev_note = cell1.pits[-1]
    cell2 = transformCell(cell1, harm[1], prev_note=prev_note)
    cell2.name = getName(names, nameB)
    if fitsMotifPref([cell1, cell2]):
        new_subs = OrderedDict()
        new_subs[cell1.name] = cell1
        new_subs[cell2.name] = cell2
        if cell1.name in names:
            names[cell1.name] += 1
        if cell2.name in names:
            names[cell2.name] += 1
        new_chunk = Chunk(sub_chunks = new_subs, name = getName(names, name))
        return (new_chunk, names)
    else:
        return genMotif(prev_note, harm, nameA, nameB, names=names)

def tooMuchSpread(prev_note, chunk):
    return abs(prev_note - chunk.pits[0]) > 3

#generate basic idea with particular harmony
def genBasicIdea(prev_note = 0, harm = [[tuple([[0,2,4]]), ([0,2,4], [4,6,8])], [tuple([[0,2,4]]), ([0,2,4], [4,6,8])]], names = {}, name = 'bi'):
    (motif1, names) = genMotif(prev_note = prev_note, harm = harm[0], names = names, name = 'motif')
    to_transform = True
    if to_transform:
        motif2 = transformMotif(motif = motif1, harm = harm[1], prev_note = motif1.pits[-1], names = names)
        motif2.name = getName(names, 'motif')
    else:
        (motif2, names) = genMotif(prev_note = motif1.pits[-1], harm = harm[1], names=names, name = 'motif')
    if fitsBasicIdeaPref([motif1, motif2]):
        new_sub_chunks = OrderedDict()
        new_sub_chunks[motif1.name] = motif1
        new_sub_chunks[motif2.name] = motif2
        return (Chunk(sub_chunks=new_sub_chunks, name=getName(names, name)), names)
    else:
        return genBasicIdea(prev_note, harm, names, name)

prev_note = 0
new_bis = OrderedDict()
names = {}
for i in range(0, 40):
    new_bi, names = genBasicIdea(prev_note = prev_note, names=names,  name = 'bi')
    if abs(prev_note - new_bi.pits[0]) > 2:
        print('error - too much spread')
        new_bi, names = genBasicIdea(prev_note = prev_note, names=names,  name = 'bi')
    prev_note = new_bi.pits[-1]
    new_bis[new_bi.name] = new_bi
a = Chunk(sub_chunks=new_bis)
mh.writeChunk([a], 'test3.mid')
"""
prev_note = 0
new_motifs = OrderedDict()
new_motif = genMotif(prev_note)[0]
new_motifs[-1] = new_motif
for i in range(0, 40):
    new_motifs[str(i)] = transformMotif(new_motif, prev_note=prev_note)
a = Chunk(sub_chunks=new_motifs)
mh.writeChunk([a], 'test2.mid')
"""