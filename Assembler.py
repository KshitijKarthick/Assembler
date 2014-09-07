#!/bin/env/python2
import sys
import os
def createSymbolTable():
	print "test"
def pass1():
	print "test"
def pass2():
	print "test"
def loadOpTable():
	fp=open('optable.dat','r')
	
def loadSymbolTable():
	print "test"
if len(sys.argv)<2:
	print "Error! no Input file detected"
else:
	filename=sys.argv[1]
	try:
		fp=open('optable.dat','r')
		fp.close()
	except (OSError,IOError) as e:
		print 'Op Code Table Missing, Please Store the Op Code Table for the Assembler\nError! File: optable.dat Missing'
	pass1(filename)
