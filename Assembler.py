#!/bin/env/python2
import sys
def createSymbolTable(optable,filename):
  loc_Ctr=0
  symtable=dict()
  errorFlags=0
  fp=open(filename,'r')
  data=fp.readLines()
  fp.close()
  line=0
  firstLine=data[0]
  firstLine=(firstLine.strip()).split()
  args=data.__len__()
  if args==3:
    label,opcode,operand=data
    if (opcode=='START' or opcode=='start'):
      try:
        loc_Ctr=(int)operand
        data=data[1:]
      except:
        print "Error! Syntax Error at Line:"+str(line)+" no\nPlease enter a valid address"

  for x in data:
    line=line+1
    inputLine=((x.strip()).split()).strip()
    args=x.__len__()
    if(args==3):
      label,opcode,operand=inputLine

    else if (args==2):
      opcode,operand=inputLine

    else if (args==1):
      opcode=inputLine
      if opcode=='//':
        continue
      else if opcode == 'END' or opcode == 'end':
        break

    else if (args==0):
        continue
    else
      print "Error! Syntax Error at Line:"+str(line)+" no\n"+inputLine+" is not valid Assembly Code"
      exit(-1)

    try:
      if(opcode=='WORD' or opcode=='word'):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+3

      else if(opcode=='RESW' or opcode=='resw'):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+(3*int(operand))

      else if(opcode=='RESB' or opcode=='resb'):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+int(operand)

      else if(opcode=='BYTE'or opcode=='byte'):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+(operand.__len__())

      else if((optable[opcode])[2] && args==3):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+((optable[symbol][2]))

      else if((optable[opcode])[2]):
        loc_Ctr=loc_Ctr+((optable[symbol][2]))

    except:
      print "Error! Syntax Error at Line:"+str(line)+" no\n"+inputLine+" is not valid Assembly Code"
  return symtable

def assemble(filename):
  symtable=pass1(filename)
  pass2(filename)

def pass1(filename):
  optable=loadOpTable()
  symtable=createSymbolTable(optable,filename)
  symtable=validateSymbolTable(symtable)
  fp=open('symtable.dat','w')
  symbol=symtable.keys()
  address=[hex(int(x)) for x in symtable.values()]
  for x in symbol and y in address:
    fp.write(x+"-"+y)
  fp.close()
  return symtable
  
def pass2(filename):
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
