#!/bin/env/python2
import sys

def createSymbolTable():
	loc_Ctr=0
	optable=loadOpTable()
	symtable=dict()
	fp=open('symtable.dat','w')
	fp1=open(filename,'r')
	data=fp1.readLines()
	line=0
	for x in data:
		line=line+1
		data=(data.strip()).split()
		symbol=data[0]
		try:
			if((optable[symbol])[2])
				loc_Ctr=loc_Ctr+((optable[symbol][2]))
		except:
			print "Error! Syntax Error at Line:"+str(line)+" no\n"+symbol+" is not a valid Assembly Code"
		if(data.__len__()==3):
			symbol,address,error=data
			symtable[symbol]=[address,error]
		
def pass1():
	print "test"
def pass2():
	print "test"

def loadOpTable():
	optable=dict()
	fp=open('optable.dat','r')
	data=fp.readLines()
	for x in data:
		data=data.strip()
		opcode,bincode,instr_Format,instr_length = data.split()
		optable[opcode]=[bincode,instr_Format,instr_length]
	fp.close()
	return optable

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
