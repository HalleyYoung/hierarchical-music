# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 21:01:19 2015

@author: halley
"""

import probabilityhelpers as ph
from functionalhelpers import *
import random

#These two functions are used to convert between string and list representations of rhythms (because lists aren't hashable and therefore can't be used in the probability dict)
def strNum(rhys):
    return ' '.join([str(i) for i in rhys])
def strToRhy(r_str):
    return [float(i) for i in r_str.split(' ')]

def probToRhys(string_dict):
    return strToRhy(ph.probDictToChoice(string_dict))

#return a similar rhythm to the previous rhythm
def alterRhythm(durs, p_alter):
    new_durs = []
    n = 0 #dur index
    while (n < len(durs)):
        durs_appended = False
        ran_alter = ph.getUniform() #random seed
        if (n < len(durs) - 4):
            if (durs[n] == 0.25 and durs[n+1] == 0.25 and durs[n+2] == 0.25 and durs[n+3] == 0.25):
                if ran_alter < p_alter / 2:
                    new_durs.append(1)
                elif ran_alter < p_alter:
                    new_durs.extend([0.5,0.5])
                else:
                    new_durs.extend([0.25,0.25,0.25,0.25]) #keep it the same
                durs_appended = True
                n += 4
        if (n < len(durs) - 2):
            if (durs[n] == 0.5 and durs[n+1] == 0.5):
                if ran_alter < p_alter / 2:
                    new_durs.append(1)
                elif ran_alter < p_alter:
                    new_durs.extend([0.25,0.25,0.25,0.25])
                else:
                    new_durs.extend([0.5, 0.5]) #keep it the same
                durs_appended = True
                n += 2
        if durs[n] == 1.0:
            if ran_alter < p_alter / 2:
                new_durs.extend([0.5,0.5])
            elif ran_alter < p_alter:
                new_durs.extend([0.25,0.25,0.25,0.25])
            else:
                new_durs.append(1.0)
            durs_appended = True
            n += 1
        if not durs_appended:
            new_durs.append(durs[n])
            n += 1
    return new_durs

#defining probabilities for any 2 beats
prob_dict = {'1.0': 0.4, '0.5 0.5': 0.53, '0.75 0.25':0.01, '0.5 0.25 0.25':0.01, '0.25 0.25 0.25 0.25':0.01}
two_prob_dict = {}
prob_dict_keys = list(prob_dict.keys())
for i in range(0, len(prob_dict_keys)):
    two_prob_dict[prob_dict_keys[i] + ' ' + prob_dict_keys[i]] = 1.3*prob_dict[prob_dict_keys[i]]
    for j in range(i + 1, len(prob_dict_keys)):
        two_prob_dict[prob_dict_keys[i] + ' ' + prob_dict_keys[j]] = ph.geometricMean([prob_dict[prob_dict_keys[i]], prob_dict[prob_dict_keys[j]]])
        two_prob_dict[prob_dict_keys[j] + ' ' + prob_dict_keys[i]] = ph.geometricMean([prob_dict[prob_dict_keys[i]], prob_dict[prob_dict_keys[j]]])
two_prob_dict['1.5 0.5'] = 0.5
two_prob_dict['1.5 0.25 0.25'] = 0.1
two_prob_dict['2.0'] = 0.5

#short = nothing with a lot of notes
def randomHalfRhythm(short = False):
    if short:
        return random.choice([[1.5, 0.5], [1.5, 0.25, 0.25], [1.0, 1.0], [1.0,0.5,0.5], [0.5,0.5,1.0]])
    else:        
        return strToRhy(ph.probDictToChoice(two_prob_dict))
        
def halfRhythmDict():
    return two_prob_dict

def randomHalfQuarterEighths():
    half_prob_dict = {'1.0 0.5 0.5':0.3, '0.5 0.5 1': 0.1, '0.5 0.5 0.5 0.5':0.25, '1.0 1.0': 0.15}
    return strToRhy(ph.probDictToChoice(half_prob_dict))

def randomDuration(length):
    if length == 1:
        return strToRhy(ph.probDictToChoice(prob_dict))
    elif length == 2:
        return strToRhy(ph.probDictToChoice(two_prob_dict))
    elif length == 3:
        return strToRhy(ph.probDictToChoice(two_prob_dict)) + strToRhy(ph.probDictToChoice(prob_dict))
    elif length == 4:
        return strToRhy(ph.probDictToChoice(two_prob_dict)) + strToRhy(ph.probDictToChoice(two_prob_dict))
    print('issue!')

#get identifying rhythms
def getIDRhythms(cells_durs):
    id_cell_rhythms = []
    id_rhythms = ['1.5','0.75', '0.125', '0.5 0.25 0.25', '0.25,0.25,0.5']
    for cell_durs in cells_durs:
        for rhys in id_rhythms:
            if rhys in strNum(cell_durs):
                id_cell_rhythms.append(cell_durs)
                break
    return id_cell_rhythms
            

def randomMeasure():
    one_prob_dict = {'1.0': 0.4, '0.5 0.5': 0.53, '0.75 0.25':0.02, '0.5 0.25 0.25':0.02, '0.25 0.25 0.25 0.25':0.02}
    two_prob_dict = {}
    prob_dict_keys = list(prob_dict.keys())
    for i in range(0, len(prob_dict_keys)):
        two_prob_dict[prob_dict_keys[i] + ' ' + prob_dict_keys[i]] = 0.5*prob_dict[prob_dict_keys[i]]
        for j in range(i + 1, len(prob_dict_keys)):
            two_prob_dict[prob_dict_keys[i] + ' ' + prob_dict_keys[j]] = ph.geometricMean([prob_dict[prob_dict_keys[i]], prob_dict[prob_dict_keys[j]]])
            two_prob_dict[prob_dict_keys[j] + ' ' + prob_dict_keys[i]] = ph.geometricMean([prob_dict[prob_dict_keys[i]], prob_dict[prob_dict_keys[j]]])
    two_prob_dict['1.5 0.5'] = 0.5
    two_prob_dict['1.5 0.25 0.25'] = 0.1
    two_prob_dict['2.0'] = 0.5
    four_prob_dict = {}
    two_prob_dict_keys = list(two_prob_dict.keys())
    for i in range(0, len(prob_dict_keys)):
        four_prob_dict[two_prob_dict_keys[i] + ' ' + two_prob_dict_keys[i]] = 3*two_prob_dict[two_prob_dict_keys[i]]
        for j in range(i + 1, len(prob_dict_keys)):
            four_prob_dict[two_prob_dict_keys[i] + ' ' + two_prob_dict_keys[j]] = ph.geometricMean([two_prob_dict[two_prob_dict_keys[i]], two_prob_dict[two_prob_dict_keys[j]]])
            four_prob_dict[two_prob_dict_keys[j] + ' ' + two_prob_dict_keys[i]] = ph.geometricMean([two_prob_dict[two_prob_dict_keys[i]], two_prob_dict[two_prob_dict_keys[j]]])
    for key in prob_dict.keys():
        four_prob_dict['3.0 ' + key] = 0.2 + prob_dict[key]
    return strToRhy(ph.probDictToChoice(four_prob_dict))

#get rhythm for fragmentation section
def getFragmentedRhythm(chunk):
    memorable = []
    smallest = 4.0
    beat_durs = chunk.beat_durs
    for beat in beat_durs:
        if any([i in beat for i in [0.75,1.5]]):
            memorable = beat
        if len(set(beat)) == 1:
            if beat[0] < smallest:
                smallest = beat[0]
    return []