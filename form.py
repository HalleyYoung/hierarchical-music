# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:31:14 2015

@author: halley
"""

"""
Things we need our object to address

Forms contain sections, which are forms

Forms specify harmonic context
Forms specify specific harmonic content
	Harmony object
		contains what key/mode each measure
		can contain more specific harmonies, with wild cards or either/or's

Forms specify how one instrument should relate to another instrument
Forms should specify how instruments share themes
	Config object
		function which takes in the motifs

Forms specify how many different motifs there are

Forms specify how sections should be related

Forms specify how motives should be distributed
	Map

Forms specify manner of choosing transformations of notes
	change which combinations are tried first

Forms specify preferences for sounds
	preference functions that act on forms/pitches
	can include specifying for rhythmic complexity

Forms must store individual voices
Forms must store individual motives






How this happens:

Solo
To create completely new material (say the antecedent), a random seed two beats are chosen (but with the ideal harmony in mind).  These are recursively transformed or new material is added to make the basic idea (again, keeping harmony in mind - looking for transformations that fit the harmony, or adding things that fit the harmony).
We go on to the next basic unit (the consequent), and see that it is not pointing to the first unit.  We therefore create it like we created the first unit.
 We go on to the next unit (the antecedent #2).  This has a function of how to generate it from the first antecedent.

Poly
We start with the grand picture of the form - how many motifs we need, and from where they are coming.
Once we have the motifs, we distribute them to the different voices.
Finally, we come up with voicings for each part.
So we need x functions:
A list that specifies the functions used to produce each chunk or chunks (so whether taken in a certain form from previous material, or created from previous motif, or created as amalgamation between other parts, or created when other parts are
	needs to be able to take in previous parts *FROM A PREVIOUS FORM*
	needs to be able to take in parts that are being produced now
	needs to be able to take in multiple parts, and produce multiple parts
A function that maps motifs to individual parts (orchestration)
A function that specifies requirements for voicing of parts

structures filled form has:

Chunk corresponding
pitches dict
durs dict

notable motifs
notable harmony
notable rhythms
codes representing instrumental configuration


start with what the sentence structure needs to contain:
	how to orchestrate each piece - inherits functions
		probabilistic?
	bi bi cadential continuation
		preferences ascending/descending
	harmony - key 0
	bi - inherits


make it easy now!


class Form():
	def __init__(prefs, transform, key = 0, harmony = [])
		self.prefs = prefs

	def fill(self, motifs)
		if motifs == []:
			genChunk()
		if ‘transform’ in motifs:
		return transformToKey(motifs)


(‘transform’, piece)
(‘repeat’, piece)

class Chunk()
"""


def simple():
	return None


class Form():
	def __init__(self, name = ''):
		self.buildWithArgs = simple
		self.filterWithArgs = simple
		self.genWithArgs = simple
		self.name = name
	def fill(self, args):
		return self.genWithArgs(args)




"""
def Sentence(form):
	self.fillWithArgs(args) =
		‘variation’
			self.addForm(BasicIdea(‘variation-instrument’, x), major = True)
			self.addForm(BasicIdea(‘repeat-instrument’, self.forms[-1])
			self.addForm(Fragmentation(‘of’, self.forms[0]))
			self.addForm(Cadential(args[Cadence]))


def Ternary()
	self.fillWithArgs(args) =
	if random.uniform()
	switch args
		self.addForm(Sentence([args )
		else:
			self.addForm(Period([args)
	self.addForm(Loose[(args)] - ‘start’
	self.addForm(Sentence[‘repeat-vary’]

self.addForm(transition)

def exposition()
	self.fillWithArgs(args)
	def self.fillWithArgs(args):
		self.addForm(ternary, subset_args)
		self.addForm(transition, subset_args)
		self.addForm(complex_period, subset_args)
"""
