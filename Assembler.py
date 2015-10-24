#!/usr/bin/env python2
import sys
class Assembler:
  """
    A two Pass Assembler, which receives source code filename as input,
    Data Members
      program_length -> Program Length based on generated object Code
      optable        -> Opcode Table [Dictionary]
      symtab         -> Symbol Table [Dictionary]
      filename       -> Source code filename
      assembly_code  -> Source code Data
  """

  program_length = 0
  optable = None
  symtable = None
  filename = None
  assembly_code = None

  def __init__(self, filename):
    """
      Constructor initialised, which starts the assembling process
      Source File -> filename
    """

    self.filename = filename
    try:
      fp = open(filename,'r')
      self.assembly_code = fp.readlines()                                    #Read Source File.
      fp.close()
      self.assemble()
    except (OSError,IOError) as err:
      print 'file: '+self.filename+' not found'

  def createSymbolTable(self):
    """
      Creates Symbol Table using statically defined optable and source code.
      symtable stores the Symbol Table created
    """

    loc_Ctr = 0                                                           #Linear Addres Generated.
    self.symtable = dict()
    errors = []                                                           #List of undeclared operands.
    errors.append("END")                                                  #Make Sure and end statement is present in the Program.
    program_name = ""
    line_no = 0
    assembly_code = self.assembly_code
    first_line = self.assembly_code[0].strip().split()
    args = first_line.__len__()
    if args==3:
      label, opcode, operand = first_line
      opcode = opcode.upper()
      if (opcode == 'START'):                                             #Check for Start Instruction.
        program_name = label
        try:
          loc_Ctr = int(operand)                                          #Different Linear Start Address.
          assembly_code = assembly_code[1:]                               #Delete Start instruction.
        except:
          print "Error! Syntax Error at Line:"+str(line)+" no\nPlease enter a valid address"
          exit(-1)
                                                                          #Creation of Symbol Table
    for line in assembly_code:
      line_no += 1                                                        #Line Count in Source Code.
      input_line = ((line.strip()).split())
      args = input_line.__len__()

      if(args==3):                                                        #Contains label,opcode,operand
        label, opcode, operand = input_line
        opcode=opcode.upper()
        if(opcode != 'RESB' and opcode != 'BYTE' and opcode != 'WORD' and opcode != 'RESW'):
          if(errors.count(operand) == 0):
            errors.append(operand)

      elif(args==2):                                                      #Contains opcode,operand.
        opcode, operand = input_line
        opcode = opcode.upper()
        if(opcode == 'END' and operand == program_name):
          errors.remove("END")
          break;
        if(errors.count(operand == 0)):
          errors.append(operand)

      elif(args == 1):                                                    #Contains operand.
        opcode = input_line[0]
        opcode = opcode.upper()
        if(opcode == '//' or opcode == '#'):                              #Skip Comment Lines.
          continue
        elif(opcode == 'END'):                                            #Indicates end of Source File.
          errors.remove("END")
          break

      elif(args==0):                                                      #Skip Blank Lines.
        continue

      else:                                                               #Should contain only maximum 3 arguments.
        print "Error! Syntax Error at Line No:",line_no,"\n",input_line," is not valid Assembly Code"
        exit(-1)

      try:
        opcode = opcode.upper()
        if(opcode == 'WORD'):                                             #Word Declaration.
          self.symtable[label] = loc_Ctr
          loc_Ctr = loc_Ctr+3                                             #Linear Address + 3.
          if(errors.count(label) > 0):
              errors.remove(label)                                        #Operand is Missing.

        elif(opcode == 'RESW'):                                           #Reserve a Word.
          self.symtable[label] = loc_Ctr
          loc_Ctr += (3*int(operand))                                     #Linear Address + (3 * operand).
          if(errors.count(label) > 0):
            errors.remove(label)                                          #Operand is Missing.

        elif(opcode == 'RESB'):                                           #Reserve a Byte.
          self.symtable[label] = loc_Ctr
          loc_Ctr += int(operand)                                         #Linear Address + 3.
          if(errors.count(label) > 0):
            errors.remove(label)                                          #Operand is Missing.

        elif(opcode == 'BYTE'):                                           #Byte Declaration.
          self.symtable[label] = loc_Ctr
          loc_Ctr += (operand.__len__())                                  #Linear Address + Length of Operand.
          if(errors.count(label)>0):
            errors.remove(label)                                          #Operand is Missing.

        elif((self.optable[opcode])[1] and args==3):                      #Check if opcode is Declared in Optable.
          self.symtable[label] = loc_Ctr                                  #Store Linear Address with Operation.
          loc_Ctr += int((self.optable[opcode])[1])                       #Linear Address + Length of Operation.

        elif((self.optable[opcode])[1]):
          loc_Ctr += int((self.optable[opcode])[1])                       #Linear Address + Length of Operation

      except KeyError:                                                    #Opcode is Missing.
        print "Error! Syntax Error at Line:",str(line_no)," no\n",input_line," is not valid Assembly Code"
        exit(-1)

      self.program_length = loc_Ctr

    if(errors.__len__()!=0):                                              #Variables Undeclared.
      for error in errors:
        print "Error! Syntax Error Operand "+error+" is Undeclared in the Assembly Code\n"
      exit(-1)

  def assemble(self):
    """
      Assembling Process ->
        Loading optable
        Pass 1 execution
        Pass 2 execution
    """

    self.loadOpTable()                                                    #Load OpTable from optable.dat.
    print "\nSuccessfully Loaded OpCode Table for the Machine : optable.dat\n"
    self.pass1()                                                          #Create Symbol Table and Validate Source Code.
    print "Successfully created Symbol Table for the input program : symtable.dat\n"
    self.pass2()                                                          #Map Linear Address with required Opcode from Optable.
    print "Successfully created Object Code for the input program : ObjectFile\n"

  def pass1(self):
    """
      Pass 1 ->
        Create Symbol Table based on source code
        Conversion of all address to Hex Values
    """

    self.createSymbolTable()                                              #Create Symbol Table.
    fp = open('symtable.dat','w')
    symbol = self.symtable.keys()

  def pass2(self):
    """
      Conversion to Machine Code based on the Symbol Table constructed
      from the source filename
      Writing of the Generated Machine code into ObjectFile
    """

    assembly_code = self.assembly_code
    program_name = "Program"
    start_address = 0
    fp = open('ObjectFile','w')
    first_line = assembly_code[0]                                         #Check of first Line is Start operation.
    first_line = (first_line.strip()).split()
    args = first_line.__len__()

    if args==3:
      label, opcode, operand = first_line
      opcode = opcode.upper()
      if (opcode == 'START'):
        program_name = label
        start_address = hex(int(operand))
        assembly_code = assembly_code[1:]                                 #Delete operation.

    self.program_length -= int(start_address,16)
    self.program_length = hex(self.program_length)
    fp.write('H'+'^'+program_name[0:5]+'^'+str(start_address)+'^'+str(self.program_length)+'\n')
    fp.write('T')
    for line in assembly_code:
      input_line = ((line.strip()).split())
      args = input_line.__len__()

      if(args == 3):                                                      #Contains label,opcode,operand.
        label, opcode, operand = input_line
        opcode = opcode.upper()
        if(opcode!='RESB' and opcode!='BYTE' and opcode!='WORD' and opcode!='RESW'):
          fp.write('^'+hex((self.optable[opcode])[0]+int(self.symtable[operand])))

      elif(args==2):                                                      #Contains opcode,operand.
        opcode,operand=input_line
        if((opcode == 'END' or opcode == 'end') and operand == program_name):
          fp.write('\nE'+'^'+start_address)
          fp.close()
          break
        fp.write('^'+hex(self.optable[opcode][0]+self.symtable[operand]))

      elif(args==1):                                                      #Contains opcode
        opcode=input_line[0]

        if opcode=='//':                                                  #skip comment.
          continue

        elif(opcode == 'END' or opcode == 'end'):                         #Terminatation of Source Code.
          fp.write('\nE'+'^'+start_address)
          fp.close()
          break
        fp.write(optable[opcode])

      elif(args==0):                                                      #Blank Line Skip.
        continue

  def loadOpTable(self):
    """
      Optable Loaded from a Static File optable.dat
      and stored as a Dictionary
    """

    self.optable = {}
    fp = open('optable.dat','r')
    data = fp.readlines()
    for line in data:
      line = line.strip()
      opcode, bincode, instr_length = line.split()                        #Read File and Store assembly_code in optable dictionary.
      shift = ( int(instr_length) - 1 ) * 8                               #right shift required of opcode to start from msb
      self.optable[opcode] = [int(bincode,16)<<shift , instr_length]
    fp.close()

if __name__ == '__main__':

  if len(sys.argv)<2:
    print "Error! no Input file detected"                                 #Input File Missing.
  else:
    filename=sys.argv[1]
    try:
      fp=open('optable.dat','r')
      fp.close()
    except (OSError,IOError) as e:
      print 'Op Code Table Missing, Please Store the Op Code Table for the Assembler\nError! File: optable.dat Missing'
    assembler = Assembler(filename)
