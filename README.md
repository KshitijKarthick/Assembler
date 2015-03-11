# SIC ASSEMBLER - Proof of Concept :

## Basic Introduction of the SIC Assembler :
* SIC refers to Simplified Instruction Computer.
* The Assembler is based on a Hypothetical Machine predefined in the book System Software by Leland L.Beck.
* The Assembler is a Two Pass Assembler.
* Seperate External input for Op Table is provided for customizing the Assembler to suit the user needs.

## Program Details :
* The Assembler is written in Python.
* The File symtable.dat is a dynamically created file which represents the symbol table for the input Program.
* The File optable.dat is a static file which should always be present with the Assembler code, it contains the machine code for the respective system and  the corresponding Op code.
* The File optable.dat is open for customization and can be changed based on the Machine requirements, but should follow the same format of storage of data.
* The File ObjectFile is Created after both passes are completed Successfully.

### OpCode Table [ optable.dat ] :
* Storage Format : Mnemonic Machine-Code Format Length-of-Code
* Mnemonic entered in optable is matched with the source code for performing specified operation.
* Machine-Code matches the Mnemonic to the Instruction Set for the respective system
* Length-of-Code the respective Mnemonic Instruction Length is recorded here.
* Format [Unnecessary for SIC Assembler] Stores Instruction Format.

### Symbol Table [ symtable.dat ] :
* Storage Format : Label-Name Linear-Address-Generated[HexaDecimal]
* Label-Name: Instruction having Labels
* Linear Address Generated.

### Object Code [ ObjectFile ] :
* Head Record : H^Program-Name[2-7]^Start-Address^Length-Of-Object-Program
* Text Record : T^MachineInstruction^MachineInstruction^.....
* End Record : E^Address-of-First-Executable

### Usage Instruction in Command Line :

#### Execution :
```
  >> python2 Assembler.py [source-file]
```

#### To Do :
* Pass 2 Functionality needs to be validated.
* Support for SIC/XE [Extended] needs to be incorporated.
