hierarchical-music
rhythms.py
scale.py
transform.py
transform2.py
transformhphrase.py
transforms.pyimport gencell as gc
import random
from chunk import *
from constants import *
import harmony as hm
import copy
"""
musical transforms:
(partial) inversion
(partial) retrograde
(partial) transposition
changing chord
ornamentation
any combination of the above
"""
#transpose chunk
def transpose(chunk, prev_note = 0, chordal = [], names = {}, name = ''):
    if chunk.depth == 0:
        new_chunks = []
        transpose_to_prev_amounts = [i + prev_note - chunk.pits[0] for i in range(-1,1)]
        transpose_amounts = [-2,2,-1,1] + transpose_to_prev_amounts
        for transpose_amount in transpose_amounts:
            new_chunk = copy.deepcopy(chunk)
            new_chunk.setName(name)
            new_pits = [i + transpose_amount for i in chunk.pits]
            new_chunk.setPitsDurs(new_pits, chunk.durs)
            new_chunks.append(new_chunk)
        return new_chunks
    elif chunk.depth == 1:
        new_chunks = []
        transpose_to_prev_amounts = [i + prev_note - chunk.pits[0] for i in range(-1,1)]
        transpose_amounts = [-2,2,-1,1] + transpose_to_prev_amounts
        for transpose_amount in transpose_amounts:
            sub_chunks = chunk.sub_chunks.values()
            sub_names = chunk.sub_chunks.keys()
            new_chunk_subchunks = OrderedDict()
            for i in range(0, len(sub_chunks)):
                new_name = getName(names,sub_names[i])
                new_chunk_subchunks[new_name] = Chunk(sub_chunks=None, pits = [j + transpose_amount for j in sub_chunks[i].pits], durs=sub_chunks[i].durs, ctype = sub_chunks[i].ctype, name=new_name)
            new_chunks.append(Chunk(sub_chunks=new_chunk_subchunks, name = name))
        return new_chunks
    else:
        return []


#keep same chunk, or just change what chord
def identity(chunk, prev_note = 0, chordal = [], names = {}, name = ''):
    if chordal == []:
        return [chunk]
    else:
        if chunk.depth == 0:
            if chunk.ctype == SCALEWISE:
                a = transposeToChord(chunk, chordal)
                a.setName(name)
                return a
            else:
                above = []
                below = []
                for pit in chunk.pits:
                    above.append(hm.getClosestAbove(pit, chordal))
                    below.append(hm.getClosestBelow(pit, chordal))
                return [Chunk(sub_chunks = None, pits = above, durs = chunk.durs, ctype = chunk.ctype, name = name), Chunk(sub_chunks = None, name=name, pits = below, durs = chunk.durs, ctype=chunk.ctype)]
        elif chunk.depth == 1:
            all_subs = OrderedDict()
            i = 0
            for sub_chunk_name, sub_chunk in chunk.sub_chunks.items():
                new_name = getName(names, sub_chunk_name)
                all_subs[new_name] = (identity(sub_chunk, chordal[i], name=new_name)[random.choice([0,1])])
                i += 1
            return [Chunk(sub_chunks = all_subs, name = name)]
        else:
            new_chunk = copy.deepcopy(chunk)
            new_chunk.setName(name)
            return new_chunk

def inversion(chunk, prev_note = 0, chordal = [], names = {}, name = ''):
    if chunk.depth == 0:
        new_notes = [chunk.pits[0]]
        for i in range(1, len(chunk.pits)):
            new_notes.append(new_notes[-1] - chunk.pits[i] + chunk.pits[i - 1])
        return [Chunk(sub_chunks = None, pits = new_notes, durs = chunk.durs, ctype = chunk.ctype, name=name)]
    elif chunk.depth == 1:
        sub_names = chunk.sub_chunks.keys()
        subs = chunk.sub_chunks.values()
        new_subs = OrderedDict()
        prev_sub = None
        for j in range(0, len(subs)):
            new_durs = subs[j].durs
            if j == 0:
                first_note = subs[0].pits[0]
            else:
                first_note = prev_sub.pits[-1] + subs[j].pits[0] - subs[j - 1].pits[-1]
            new_pits = [first_note]
            for i in range(1, len(subs[j].pits)):
                new_pits.append(new_pits[-1] - subs[j].pits[i] + subs[j].pits[i - 1])
            new_name = getName(names, sub_names[j])
            new_subs[new_name] = Chunk(sub_chunks=None, pits=new_pits, durs=new_durs, ctype=chunk.ctype, name=new_name)
            prev_sub = new_subs[new_name]
        return [Chunk(sub_chunks=new_subs, name = name)]
    else:
        return []

#retrograde
def retrograde(chunk, prev_note = 0, chordal = [], names = {}, name = ''):
    if chunk.depth == 0:
        return [Chunk(sub_chunks=None, pits=chunk.pits[::-1], durs=chunk.durs[::-1], name = name)]
    elif chunk.depth == 1:
        new_sub_chunks = OrderedDict()
        sub_names = chunk.sub_chunks.keys()
        subs = chunk.sub_chunks.values()
        for j in range(0, len(subs)):
            sub_chunk = subs[::-1][j]
            new_name = getName(names, sub_names[j])
            new_sub_chunks[new_name] = Chunk(sub_chunks=None, pits=sub_chunk.pits[::-1], durs=sub_chunk.durs, ctype=sub_chunk.ctype, name = new_name)
        return [Chunk(new_sub_chunks, name = name)]
    else:
        return []

#partial retrograde
def partialRetrograde(chunk, prev_note = 0, chordal = [], names = {}, name = ''):
    new_chunks = []
    if chunk.depth == 0:
        #retrograde beginning, keep rhythm const
        new_pits = chunk.beat_pits[0][::-1] + fh.concat(chunk.beat_pits[1:])
        new_chunks.append(Chunk(sub_chunks=None, pits=new_pits, durs = chunk.durs, name = name))
        #retrograde beginning, change rhythm
        new_durs = chunk.beat_durs[0][::-1] + fh.concat(chunk.beat_durs[1:])
        new_chunks.append(Chunk(sub_chunks=None, pits=new_pits, durs = new_durs, name = name))

        #retrograde end, keep rhythm const
        new_pits = fh.concat(chunk.beat_pits[:-1]) + chunk.beat_pits[-1][::-1]
        new_chunks.append(Chunk(sub_chunks=None, pits=new_pits, durs = chunk.durs, name=name))
        #retrograde end, change rhythm
        new_durs = fh.concat(chunk.beat_durs[:-1]) + chunk.beat_durs[-1][::-1]
        new_chunks.append(Chunk(sub_chunks=None, pits=new_pits, durs = new_durs,name=name))

        #switch order of beats
        new_pits = fh.concat(reversed(chunk.beat_pits))
        new_durs = fh.concat(reversed(chunk.beat_durs))
        new_chunks.append(Chunk(sub_chunks = None, pits=new_pits, durs=new_durs,name=name))
        #retrograde and partially retrograde any subchunk
    else:
        sub_names = chunk.sub_chunks.keys()
        sub_chunks = chunk.sub_chunks.values()
        #retrograde last chunk
        new_subs = OrderedDict()
        new_name = getName(names, sub_names[0])
        new_subs[new_name] = copy.deepcopy(sub_chunks[0])
        new_subs[new_name].name = new_name
        for i in range(1, len(names) - 1):
            new_name = getName(names, sub_names[i])
            new_subs[new_name] = copy.deepcopy(sub_chunks[i])
            new_subs[new_name].name = new_name
        new_name = getName(names, sub_names[0])
        new_subs[new_name] = random.choice(retrograde(sub_chunks[-1], prev_note, [], new_name))
        new_chunks.append(Chunk(sub_chunks = new_subs, name=name))

        #retrograde first chunk
        new_subs = OrderedDict()
        new_name = getName(names, sub_names[0])
        new_subs[new_name] = random.choice(retrograde(sub_chunks[0], prev_note))
        new_subs[new_name].name = new_name
        for i in range(1, len(sub_names)):
            new_name = new_name = getName(names, sub_names[i])
            new_subs[new_name] = sub_chunks[i]
            new_subs[new_name].name = new_name
        new_chunks.append(Chunk(sub_chunks = new_subs))

        #retrograde order of subchunks
        new_subs = OrderedDict()
        sub_names = sub_names[::-1]
        sub_chunks = sub_chunks[::-1]
        for i in range(0, len(sub_names)):
            new_name = getName(names, sub_names[i])
            new_subs[new_name] = sub_chunks[i]
            new_subs[new_name].name = new_name

        new_chunks.append(Chunk(sub_chunks=new_subs))
    return new_chunks

#partial transpose subs
def partialTranspose(chunk, prev_note = 0, chordal = [], names = {}):
    new_chunks = []
    if chunk.depth == 0:
        pits = chunk.pits
        #transpose every beat
        for amount in ([-2,2,-1,1]):
            for i in range(0, len(chunk.beat_durs)):
                new_pits = fh.concat(chunk.beat_pits[:i]) + [pit + amount for pit in chunk.beat_pits[i]] + fh.concat(chunk.beat_pits[i+1:])
                new_chunks.append(Chunk(sub_chunks=None, pits=new_pits, durs=chunk.durs))
        #transpose every two notes
            for i in range(0, len(pits) - 1):
                new_pits = pits[:i] + [pits[i] + amount, pits[i + 1] + amount] + pits[i+1:]
                new_chunks.append(Chunk(sub_chunks=None, pits=new_pits, durs=chunk.durs))
    elif chunk.depth == 1:
        #partial transpose or full transpose any one of the sub_chunks
        names = chunk.sub_chunks.keys()
        sub_chunks = chunk.sub_chunks.values()
        for k in range(0, 4):
            for i in range(0, len(sub_chunks) - 1):
                new_subs = OrderedDict()
                for j in range(0, i):
                    new_subs[names[j]] = sub_chunks[j]
                prev_note = prev_note if i == 0 else sub_chunks[i - 1].pits[-1]
                new_subs[names[i]] = random.choice(partialTranspose(sub_chunks[i], prev_note))
                for j in range(i+1, len(names)):
                    new_subs[names[j]] = sub_chunks[j]
                new_chunks.append(Chunk(sub_chunks = new_subs))
            #partial transpose all of the sub_chunks
        for i in range(0, 3):
            new_subs = OrderedDict()
            for j in range(0, len(sub_chunks)):
                new_subs[names[j]] = random.choice(partialTranspose(sub_chunks[j]))
            new_chunks.append(Chunk(sub_chunks = new_subs))
    return new_chunks


def transposeToChord(chunk, prev_note = 0, chord = [], names = {}):
    if chunk.depth == 0:
        #get closest above with chord
        distance = hm.getClosestAbove(chunk.pits[0], chord) - chunk.pits[0]
        new_pits = [i + distance for i in chunk.pits]
        chunk_above = Chunk(sub_chunks=None, pits=new_pits, durs=chunk.durs, ctype=chunk.ctype)

        distance = chunk.pits[0] - hm.getClosestBelow(chunk.pits[0], chord)
        new_pits = [i - distance for i in chunk.pits]
        chunk_below = Chunk(sub_chunks=None, pits=new_pits, durs=chunk.durs, ctype=chunk.ctype)

        new_chunks = [chunk_below, chunk_above]
        if hm.chunkInChord(chunk, chord):
            new_chunks.append(chunk)
        return new_chunks
    elif chunk.depth == 1:
        return [Chunk]
    else:
        return [chunk]


def subRhythm(chunk, prev_note = 0, chordal = [0,2,4], names = {}, how_many = 7):
    if chunk.depth == 0:
        new_chunks = []
        for i in range(0,how_many):
            new_durs = []
            for beat_dur in chunk.beat_durs:
                ran = random.uniform(0,1)
                if beat_dur == [2.0]:
                    if ran < 0.5:
                        new_durs.append(2.0)
                    elif ran < 0.7:
                        new_durs.extend([1.0,0,5,0.5])
                    elif ran < 0.8:
                        new_durs.extend([0.5,0.5,1])
                    elif ran < 0.9:
                        new_durs.extend([1.0,1.0])
                    else:
                        new_durs.extend([0.5,0.5,0.5,0.5])
                elif beat_dur == [1.0]:
                    if ran < 0.6:
                        new_durs.append(1.0)
                    elif ran < 0.9:
                        new_durs.extend([0.5,0.5])
                    else:
                        new_durs.extend([0.25,0.25,0.25,0.25])
                elif beat_dur == [0.5,0.5]:
                    if ran < 0.6:
                        new_durs.extend([0.5,0.5])
                    elif ran < 0.8:
                        new_durs.append(1.0)
                    else:
                        new_durs.extend([0.25,0.25,0.25,0.25])
                elif beat_dur == [0.25,0.25,0.25,0.25]:
                    if ran < 0.6:
                        new_durs.extend([0.25,0.25,0.25,0.25])
                    elif ran < 0.9:
                        new_durs.extend([0.5,0.5])
                    else:
                        new_durs.append(1.0)
                else:
                    new_durs.extend(beat_dur)
            new_chunks.append(gc.getCell(int(sum(new_durs)), prev_note, first_note = None, chord=chordal, durs = new_durs, cell_type=chunk.ctype))
        return new_chunks
    elif chunk.depth == 1:
        new_chunks = []
        for j in range(0,7):
            sub_names = chunk.sub_chunks.keys()
            sub_chunks = chunk.sub_chunks.values()
            new_subs = OrderedDict()
            for i in range(0, len(names)):
                new_sub = subRhythm(sub_chunks[i], chordal[i], prev_note)[0]
                new_sub_name = getName(names, sub_names[i])
                new_sub.name = new_sub_name
                new_subs[new_sub_name] = new_sub
                prev_note = new_sub.pits[-1]
            new_chunks.append(Chunk(sub_chunks=new_subs))
        return new_chunks
    else:
        print('error - depth > 1')