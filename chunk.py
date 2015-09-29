# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:11:47 2015

@author: halley
"""
import functionalhelpers as fh
import rhythms as rhy
from collections import OrderedDict

#get name of a cell
def getName(names, new_name):
    new_name = new_name.split('-')[0]
    if new_name in names:
        names[new_name] += 1
        return new_name + '-' + str(names[new_name])
    else:
        names[new_name] = 0
        return new_name + '-0'

#get maximum depth of a chunk
def getMaxDepth(chunk):
    if chunk.sub_chunks == None or chunk.sub_chunks == {}:
        return 0
    else:
        return 1 + max([getMaxDepth(i) for i in chunk.sub_chunks.values()])
#get minimum depth of a chunk
def getMinDepth(chunk):
    if chunk.sub_chunks == None or chunk.sub_chunks == {}:
        return 0
    else:
        return 1 + min([getMinDepth(i) for i in chunk.sub_chunks.values()])

#get cells of a chunk
def getCells(chunk):
    if chunk.depth == 0:
        chunk_dict = OrderedDict()
        chunk_dict[chunk.name] = chunk
        return chunk_dict
    else:
        new_dict = OrderedDict()
        for (sub_chunk_name, sub_chunk) in chunk.sub_chunks.items():
            a = getCells(sub_chunk)
            if len(a) > 0:
                for (name, val) in a.items():
                    new_dict[name] = val
        return new_dict

#get all sub_chunks(big and small)
def getAllChunks(chunk):
    if chunk.depth == 0:
        chunk_dict = {}
        chunk_dict[chunk.name] = chunk
        return chunk_dict
    else:
        new_dict = {}
        new_dict[chunk.name] = chunk
        for (sub_chunk_name, sub_chunk) in chunk.sub_chunks.items():
            a = getAllChunks(sub_chunk)
            if len(a) > 0:
                for (name, val) in a.items():
                    new_dict[name] = val
        return new_dict


#get a string representation of the structure of a chunk
def getStructure(chunk):
    if chunk.depth == 0:
        return chunk.name
    elif chunk.depth == 1:
        new_str = chunk.name + ' { '
        for sub_chunk_name in chunk.sub_chunks.keys():
            new_str += sub_chunk_name + ' '
        new_str += '} '
        return new_str
    else:
        new_str = chunk.name + ' { '
        for sub_chunk in chunk.sub_chunks.values():
            new_str += getStructure(sub_chunk)
        new_str += '} '
        return new_str

#for debugging purposes
def printStructure(chunk):
    if chunk.depth == 0:
        print(chunk.name + ' is a cell')
    elif chunk.depth == 1:
        for sub_chunk_name in chunk.sub_chunks.keys():
            print(sub_chunk_name + ' is a child of ' + chunk.name)
    else:
        for sub_chunk_name, sub_chunk_value in chunk.sub_chunks.items():
            print(sub_chunk_name + ' is a child of ' + chunk.name)
            printStructure(sub_chunk_value)
    
#A chunk of music
class Chunk():
    #for resetting beat_pits and beat_durs after resetting pits and durs
    def resetBeatPitsAndDurs(self):
        self.beat_durs = []
        new_note = True
        for note in self.durs:
            if new_note:
                self.beat_durs.append([note])
                if (note % 1) != 0:
                    new_note = False
            else:
                self.beat_durs[-1].append(note)
                if sum(self.beat_durs[-1]) % 1 == 0:
                    new_note = True
        self.beat_pits = fh.mapStructure(self.beat_durs, self.pits)

    def appendPitsDurs(self, pits, durs):
        self.pits += pits
        self.durs += durs

        self.resetBeatPitsAndDurs()

    def setPitsDurs(self, pits, durs):
        self.pits = pits
        self.durs = durs

        self.resetBeatPitsAndDurs()

    def listSubchunks(self):
        return self.sub_chunks.values()

    def listCells(self):
        return self.cells.values()

    def setName(self, name):
        if name in self.names:
            self.name = name + str(self.names[name] + 1)
            self.names[name] += 1
        else:
            self.name = name + '0'
            self.names[name] = 0

    def __init__(self, sub_chunks = None, cells = None, pits = [], durs = [], ctype = -1, name = '', names = {}, harm = None, structure = '', start_time = 0, depth = -1):
        self.sub_chunks = sub_chunks

        #find depth
        self.depth = getMaxDepth(self)
        self.max_depth = getMaxDepth(self)
        self.min_depth = getMinDepth(self)

        #set names of substructures and name of larger structure
        self.name = name
        self.names = names
        self.name = ''
        self.setName(name)

        #set harmony
        self.harm = harm

        #set structure
        if structure == '':
            self.structure = getStructure(self)
        else:
            self.structure = structure

        #create a dict of all of the different sub_chunks of all sizes
        self.all_chunks = getAllChunks(self)

        #get cells
        if cells == None:
            self.cells = getCells(self)
            #self.resetStructure()
        else:
            self.cells = cells


        #find pits/durs
        if pits == [] and self.depth > 0:
            pits = fh.concat([i.pits for i in self.cells.values()])
            durs = fh.concat([i.durs for i in self.cells.values()])
        self.pits = pits
        self.durs = durs

        #set ctype - basically only useful for cells
        self.ctype = ctype
        
        #set start time
        self.start_time = start_time
        #get beat rhythms and pitches
        self.beat_durs = []
        self.beat_pits = []
        self.resetBeatPitsAndDurs()


    #def resetStructure(self):

