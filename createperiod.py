# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:35:16 2015

@author: halley
"""
import random
#tree constructed as blueprint for a musical piece
class PlanTree():
    def __init__(self, onBeat, beats, depth = -1, children = [], transformation = None, reference = None, isBasic = True):
        self.depth = depth
        self.children = children
        self.transform = transformation
        self.reference = reference
        self.isBasic = isBasic
        self.ids = {}
        self.identification = random.randint(100000, 200000)
        self.onBeat = onBeat
        self.beats = beats
    def setID(self):
        if self.id != None:
            old_id = self.id 
        self.identification = max(self.ids) + 1
        if self.depth not in self.ids:
            self.ids[self.depth] = []
        self.ids[self.depth].append(self.identification)
        self.ids[self.depth].remove(old_id)
    def addChild(self, new_child): #add a single child
        self.children.append(new_child)
        for (k,v) in new_child.ids.items():
            self.ids[k].append(v)
    def addChildren(self, new_children): #add multiple children
        self.children.extend(new_children)
        for child in new_children:
            for (k,v) in child.ids.items():
                self.ids[k].append(v)
            
#split a chunk into two parts
def getSplit(onBeat):
    return onBeat/2            

#create a planning tree
def createTree(depth, onBeat, beats):
    tree = PlanTree(onBeat, beats, depth)
    split_beats = getSplit(onBeat, beats)
    split_onbeats = [onBeat]
    
    transforms = []
    references = []
    
    for i in range(1, len(split_beats)):
        split_onbeats.append(split_onbeats[-1] + split_beats[i - 1])
    if tree.depth <= 2:
        #if random.uniform((4 - depth)**2*0.05):
        if False:
            for i in range(0, len(split_beats)):
                tree.addChild(PlanTree(split_onbeats[i], split_beats[i], depth - 1, [], transforms[i], references[i], True))
                
        