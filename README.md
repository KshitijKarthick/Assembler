## ASSEMBLER - Proof of Concept :

### Basic Introduction of the SIC [Simplified Instruction Computer] Assembler :
* The Assembler is based on a Hypothetical Machine predefined in the book System Software by Leland L.Beck.
* The Assembler is a Two Pass Assembler.
* The Assembler is written in Python.
* Seperate External input for Op Table is provided for customizing the Assembler to suit the user needs.

### Program Details :
* The File symtable.dat is a dynamically created file which represents the symbol table for the input Program.
* The File optable.dat is a static file which should always be present with the Assembler code, it contains the machine code for the respective system and  the corresponding Op code.
* The File optable.dat is open for customization and can be changed based on the System requirements, but should follow the same format of storage of data.
