__author__ = 'halley'
import scale as sc
import random
from chunk import *

#transform half phrase into a cadence
def transformToCadence(chunk, cad_type):
    if len(chunk.cells) != 4:
        print('error! - cells != 4!')
        return chunk
    new_durs = []
    new_pits = []
    if chunk.depth == 2:
        pits_before = chunk.cells[2].pits
        if cad_type == 'half':
            if random.uniform(0,1) < 1.0:
                new_durs = [2.0]
                new_pits = [sc.closestNoteDegreeInChord(pits_before[-1], [4,8])]
            elif random.uniform(0,1) < 0.5:
                new_durs = [1.0, -1.0]
                new_pits = [sc.closestNoteDegreeInChord(pits_before[-1], [4,8]), -1]
            else:
                new_durs = [1.0, 0.5, 0.5]
                new_pits = [sc.closestNoteDegreeInChord(pits_before[-1], [4,8])]
                new_pits.append(new_pits[-1] - 1)
                new_pits.append(new_pits[-1] - 1)
        elif cad_type == 'authentic':
            if random.uniform(0,1) < 1.0:
                new_durs = [2.0]
                new_pits = [sc.closestNoteDegreeInChord(pits_before[-1], [0])]
            else:
                new_durs = [1.0, -1.0]
                new_pits = [sc.closestNoteDegreeInChord(pits_before[-1], [0]), -1]
        elif cad_type == 'inauthentic':
            if random.uniform(0,1) < 1.0:
                new_durs = [2.0]
                new_pits = [sc.closestNoteDegreeInChord(pits_before[-1], [4,2])]
            elif random.uniform(0,1) < 0.5:
                new_durs = [1.0, -1.0]
                new_pits = [sc.closestNoteDegreeInChord(pits_before[-1], [4,2]), -1]
            else:
                new_durs = [1.0, 0.5, 0.5]
                new_pits = [sc.closestNoteDegreeInChord(pits_before[-1], [4,2])]
                new_pits.append(new_pits[-1] - 1)
                new_pits.append(new_pits[-1] - 1)
        else:
            print('invalid cadence type')
        chunk.sub_chunks[1].sub_chunks[1].setPitsDurs(new_pits, new_durs)
    return chunk