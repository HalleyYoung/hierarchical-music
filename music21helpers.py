
from music21 import *
from constants import *
import scale as sc
import functionalhelpers as fh

def listsToPart(pits, durs):
    notes = []
    length = min(len(pits), len(durs))
    pits = pits[:length]
    durs = durs[:length]
    for i in range(0, len(pits)):
        pit = pits[i]
        if type(pit) == tuple:
            chord_notes = []
            for pit_type in pit:
                n = note.Note(pit_type)
                n.quarterLength = durs[i]
                chord_notes.append(n)
            notes.append(chord.Chord(chord_notes))
        elif pit > 30 and pit < 90 and durs[i] > 0:
            n = note.Note(pit)
            n.quarterLength = durs[i]
            notes.append(n)
        else:
            n = note.Rest()
            n.isRest = True
            n.quarterLength = abs(durs[i])
            notes.append(n)
    s = stream.Part()
    for i in range(0, len(notes)):
        s.append(notes[i])
    return s

def chunkToPart(chunk):
    pits = sc.degreesToNotes(chunk.pits)
    durs = chunk.durs
    return listsToPart(pits, durs)

def writeChunk(chunks, fname):
    s = stream.Stream()
    for chunk_part in chunks:
        part = chunkToPart(chunk_part)
        s.append(part)
    s.write('mid', '/Users/halley/Desktop/' + fname)

def writePart(part, fname):
    part.write('xml', '/Users/halley/Desktop/' + fname)
