from form import *
import transform as tf
import gencell as gc
import probabilityhelpers as ph
import transforms as tfs
from chunk import *
import closenessdistribution as cd
import random


def genBasicWithHarm(harmony):
    return []

def genRepeat(harmony):
    return []

#generate a basic idea
def genBasic(args):
    if args == {}:
        harmony = random.choice([[0,2,4],[0,2,4],[4,6,8],[0,2,4]], [[0,2,4],[4,6,8],[0,2,4],[0,2,4]])
        return genBasicWithHarm(harmony)
    elif 'harm' in args:
        harmony = args['harm']
        return genBasicWithHarm(harmony)
    else:
        if 'repeat' in args:
            if harm in args:
                return genRepeat(args['repeat'], args['harmony'])
            else:
                return genRepeat(args['repeat'], random.choice([[0,2,4],[0,2,4],[4,6,8],[0,2,4]], [[0,2,4],[4,6,8],[0,2,4],[0,2,4]]))


class BasicIdea(Form):

    def __init__(self):
        Form.__init__(self, 'basic idea')
        self.genWithArgs = genBasic



