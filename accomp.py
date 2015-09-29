__author__ = 'halley'
import harmony as hm
from chunk import *

#generate the basic chords underneath the chunk
def genChords(chunk):
    all_chords = []
    all_durs = []
    for cell in chunk.cells:
        all_durs.append(2.0)
        all_chords.append(hm.getChord(cell))
    return Chunk(None, all_chords, all_durs)