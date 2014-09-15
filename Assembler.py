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
  args=firstLine.__len__()
  if args==3:
    label,opcode,operand=firstLine
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
    args=inputLine.__len__()
    if(args==3):
      label,opcode,operand=inputLine
      if(opcode!='resb' and opcode!='byte' and opcode!='word' and opcode!='resw' and opcode!='RESB' and opcode!='BYTE' and opcode!='WORD' and opcode!='RESW'):
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
        symtable[label]=loc_Ctr
        loc_Ctr=loc_Ctr+3
        if(errors.count(label)>0):
            errors.remove(label)

      elif(opcode=='RESW' or opcode=='resw'):
        symtable[label]=loc_Ctr
        loc_Ctr=loc_Ctr+(3*int(operand))
        if(errors.count(label)>0):
          errors.remove(label)

      elif(opcode=='RESB' or opcode=='resb'):
        symtable[label]=loc_Ctr
        loc_Ctr=loc_Ctr+int(operand)
        if(errors.count(label)>0):
          errors.remove(label)

      elif(opcode=='BYTE'or opcode=='byte'):
        symtable[label]=loc_Ctr
        loc_Ctr=loc_Ctr+(operand.__len__())
        if(errors.count(label)>0):
            errors.remove(label)

      elif((optable[opcode])[2] and args==3):
        symtable[label]=loc_Ctr
        loc_Ctr=loc_Ctr+int((optable[opcode])[2])

      elif((optable[opcode])[2]):
        loc_Ctr=loc_Ctr+int((optable[opcode])[2])

    except KeyError:
      print "Error! Syntax Error at Line:",str(line)," no\n",inputLine," is not valid Assembly Code"
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
  symtable_Hex=dict()
  address=[hex(int(x)) for x in symtable.values()]
  for x in range(symbol.__len__()):
    fp.write(symbol[x]+" "+address[x]+"\n")
    symtable_Hex[symbol[x]]=address[x]
  fp.close()
  return symtable_Hex

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
    inputLine=((x.strip()).split())
    args=inputLine.__len__()
    if(args==3):
      label,opcode,operand=inputLine
      if(opcode!='resb' and opcode!='byte' and opcode!='word' and opcode!='resw' and opcode!='RESB' and opcode!='BYTE' and opcode!='WORD' and opcode!='RESW'):
        fp.write(str((optable[opcode])[0])+''+str(symtable[label])+' ')
    elif(args==2):
      opcode,operand=inputLine
      print opcode,operand,optable[opcode],symtable[operand]
      fp.write(str((optable[opcode])[0])+''+str(symtable[operand])+' ')       # Error Gotta Fix, gotta compute all addresses and save, not just the ones with the label.
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
