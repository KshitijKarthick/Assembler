#!/bin/env/python2
import sys
def createSymbolTable(optable,filename):
  loc_Ctr=0
  symtable=dict()
  errorFlags=0
  errors=list()
  fp=open(filename,'r')
  data=fp.readlines()
  fp.close()
  line=0
  firstLine=data[0]
  firstLine=(firstLine.strip()).split()
  args=data.__len__()
  if args==3:
    label,opcode,operand=data
    if (opcode=='START' or opcode=='start'):
      try:
        loc_Ctr=int(operand)
        data=data[1:]
      except:
        print "Error! Syntax Error at Line:"+str(line)+" no\nPlease enter a valid address"
        exit(-1)

  for x in data:
    line=line+1
    inputLine=((x.strip()).split())
    args=x.__len__()
    if(args==3):
      label,opcode,operand=inputLine
      if(errors.count(operand)==0):
        errors.append(operand)
    elif(args==2):
      opcode,operand=inputLine
      if(errors.count(operand)==0):
        errors.append(operand)
    elif(args==1):
      opcode=inputLine
      if opcode=='//':
        continue
      elif(opcode == 'END' or opcode == 'end'):
        break

    elif(args==0):
        continue
    else:
      print "Error! Syntax Error at Line No:",line,"\n",inputLine," is not valid Assembly Code"
      exit(-1)
    try:
      if(opcode=='WORD' or opcode=='word'):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+3
        if(errors.count(operand)==1):
          errors.remove(operand)

      elif(opcode=='RESW' or opcode=='resw'):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+(3*int(operand))
        if(errors.count(operand)==1):
          errors.remove(operand)

      elif(opcode=='RESB' or opcode=='resb'):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+int(operand)
        if(errors.count(operand)==1):
          errors.remove(operand)

      elif(opcode=='BYTE'or opcode=='byte'):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+(operand.__len__())
        if(errors.count(operand)==1):
          errors.remove(operand)

      elif((optable[opcode])[2] and args==3):
        symtable[label]=[loc_Ctr,errorFlags]
        loc_Ctr=loc_Ctr+((optable[symbol][2]))

      elif((optable[opcode])[2]):
        loc_Ctr=loc_Ctr+((optable[symbol][2]))

    except:
      print "Error! Syntax Error at Line:"+str(line)+" no\n"+inputLine+" is not valid Assembly Code"
      exit(-1)
  if(errors.__len__()!=0):
    for x in errors:
      print "Error! Syntax Error Operand "+x+" is Undeclared in the Assembly Code\n"
    exit(-1)
  return symtable

def assemble(filename):
  optable=loadOpTable()
  symtable=pass1(filename,optable)
  pass2(filename,symtable,optable)

def pass1(filename,optable):
  symtable=createSymbolTable(optable,filename)
  fp=open('symtable.dat','w')
  symbol=symtable.keys()
  address=[hex(int(x)) for x in symtable.values()]
  for x in symbol and y in address:
    fp.write(x+" "+y)
  fp.close()
  return symtable

def pass2(filename,symtable,optable):
  fp=open(filename,'r')
  data=fp.readlines()
  fp.close()
  fp=open('ObjectFile.dat','w')
  firstLine=data[0]
  firstLine=(firstLine.strip()).split()
  args=data.__len__()
  if args==3:
    label,opcode,operand=data
    if (opcode=='START' or opcode=='start'):
        data=data[1:]

  for x in data:
    inputLine=((x.strip()).split()).strip()
    args=x.__len__()
    if(args==3):
      label,opcode,operand=inputLine
      fp.write(optable[opcode]+''+symtable[operand])
    elif(args==2):
      opcode,operand=inputLine
      fp.write(optable[opcode]+''+symtable[operand])
    elif(args==1):
      opcode=inputLine
      if opcode=='//':
        continue
      elif(opcode == 'END' or opcode == 'end'):
        break
      fp.write(optable[opcode])
    elif(args==0):
        continue


def loadOpTable():
  optable=dict()
  fp=open('optable.dat','r')
  data=fp.readlines()
  for x in data:
    x=x.strip()
    opcode,bincode,instr_Format,instr_length = x.split()
    optable[opcode]=[bincode,instr_Format,instr_length]
  fp.close()
  return optable

if len(sys.argv)<2:
  print "Error! no Input file detected"
else:
  filename=sys.argv[1]
  try:
    fp=open('optable.dat','r')
    fp.close()
  except (OSError,IOError) as e:
    print 'Op Code Table Missing, Please Store the Op Code Table for the Assembler\nError! File: optable.dat Missing'
  assemble(filename)
