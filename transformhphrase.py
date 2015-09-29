__author__ = 'halley'

import transforms as tfs
from chunk import *
import random

#map function to hphrase
def mapToHPhrase(f, chunk, chords, prev_note):
    new_chunks = []
    for j in range(0, 7):
        prev = prev_note
        new_sub_chunks = []
        for i in range(0, len(chunk.sub_chunks)):
            new_subs = f(chunk.sub_chunks[i], chords[2*i:2*i+2], prev)
            if len(new_subs) > 0:
                new_sub_chunks.append(random.choice(new_subs))
            else:
                break
            prev = new_sub_chunks[-1].pits[-1]
        new_chunks.append(Chunk(new_sub_chunks))
    return new_chunks

