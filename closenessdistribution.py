import probabilityhelpers as ph
import functionalhelpers as fh
from operator import itemgetter
import random

#get a note a certain distance from the previous note that is in the right chord
def closenessDistribution(chord, prev_note, dist):
    if chord == []:
        return prev_note + random.choice([-1,-1,1,1,-2,2])
    if dist == 'close':
        far_dict = {0:0.6, 1:0.4}
    elif dist == 'med':
        far_dict = {0:0.4, 1:0.35, 2:0.2, 3:0.05}
    n = ph.probDictToChoice((far_dict))

    #get note in chord that is nth away from prev_note
    all_notes_in_chord = fh.concat([[root_note + octave for root_note in chord] for octave in range(-21,21,7)])


    #get distances between notes and prev_note
    notes_distances = map(lambda i: (i, abs(i - prev_note)), all_notes_in_chord)

    #sort notes_distances by the distance
    notes_distances = sorted(notes_distances, key = itemgetter(1))

    return notes_distances[n][0]