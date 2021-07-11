import ml_assembler as assemb
import cpu_simulator
import pytest

############### assembly language tests ###############
def test_assemblyLanguage_initializeWithoutError():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    assert thisAssemblyLanguageInstance != None

def test_findAndParseAssemblyCommand_mathesSTORE():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="STORE"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="0000000000000000"

def test_findAndParseAssemblyCommand_mathesLOAD():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="LOAD"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="0000000000000001"

def test_findAndParseAssemblyCommand_all0_mathesSETLOWBITS():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="SETLOWBITS 00000000"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="0000000000000010"

def test_executeAssemblyCommand_all0_SETLOWBITS():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="SETLOWBITS 00000000"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    theCpu:cpu_simulator.CPU = cpu_simulator.CPU()
    theCpu.theClock=1 # The next tick of the CPU will execute the command in register1
    theCpu.register1.fromString(binaryRepresentation) # Store the command in register1
    
    # Set up conditions to test the CPU command
    reg7="1111111111111111"
    theCpu.register7.fromString(reg7) # set register7 so we can verify that its overwritten
    assert theCpu.register7.toString()=="1111111111111111"

    # Test that the command does what it's supposed to
    theCpu.tick() # let the CPU execute the specified command in register1
    assert theCpu.register7.toString()=="1111111100000000" # verify that the RAM address is properly set

def test_findAndParseAssemblyCommand_int1_matchesSETLOWBITS():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="SETLOWBITS 00000001"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="0000000000001010"

def test_executeAssemblyCommand_ADD_register4Set():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="ADD"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    theCpu:cpu_simulator.CPU = cpu_simulator.CPU()
    theCpu.theClock=1 # The next tick of the CPU will execute the command in register1
    theCpu.register1.fromString(binaryRepresentation) # Store the command in register1
    
    # Set up conditions to test the CPU command
    reg2="1111111100000000"
    theCpu.register2.fromString(reg2) # set register7 so we can verify that its overwritten
    assert theCpu.register2.toString()==reg2
    reg3="0000000001010101"
    theCpu.register3.fromString(reg3) # set register7 so we can verify that its overwritten
    assert theCpu.register3.toString()==reg3
    
    # Test that the command does what it's supposed to
    theCpu.tick() # let the CPU execute the specified command in register1
    assert theCpu.register4.toString()=="1111111101010101" # verify that output register

def test_executeAssemblyCommand_ADD_withOverlappingBits_register4Set():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="ADD"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    theCpu:cpu_simulator.CPU = cpu_simulator.CPU()
    theCpu.theClock=1 # The next tick of the CPU will execute the command in register1
    theCpu.register1.fromString(binaryRepresentation) # Store the command in register1
    
    # Set up conditions to test the CPU command
    reg2="0000000011111111"
    theCpu.register2.fromString(reg2) # set register7 so we can verify that its overwritten
    assert theCpu.register2.toString()==reg2
    reg3="0110000000000001"
    theCpu.register3.fromString(reg3) # set register7 so we can verify that its overwritten
    assert theCpu.register3.toString()==reg3
    
    # Test that the command does what it's supposed to
    theCpu.tick() # let the CPU execute the specified command in register1
    assert theCpu.register4.toString()=="0110000100000000" # verify that output register

def test_ADD_withJUMP_100_matchesExpectedBinary():
    commandString="SUM IF NEG JUMP 100"
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="00"+"01"+"000010"+"100"+"101"

def test_executeAssemblyCommand_ADD_withJUMP_register0ResetAndJump():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="SUM IF NEG JUMP 100"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    theCpu:cpu_simulator.CPU = cpu_simulator.CPU()
    theCpu.theClock=1 # The next tick of the CPU will execute the command in register1
    theCpu.register1.fromString(binaryRepresentation) # Store the command in register1
    
    # Set up conditions to test the CPU command
    reg0="0000000000000000"
    theCpu.register0.fromString(reg0)
    assert theCpu.register0.toString()==reg0
    reg2="0100000011111111"
    theCpu.register2.fromString(reg2) # set register7 so we can verify that its overwritten
    assert theCpu.register2.toString()==reg2
    reg3="0110000000000001"
    theCpu.register3.fromString(reg3) # set register7 so we can verify that its overwritten
    assert theCpu.register3.toString()==reg3
    
    # Test that the command does what it's supposed to
    theCpu.tick() # let the CPU execute the specified command in register1
    assert theCpu.register4.toString()=="1010000100000000" # verify that output register

    # Test that register0 got properly reset
    assert theCpu.register0.toString()=="1010000100000000" # verify the jump target

def test_executeAssemblyCommand_ADD_withJUMP_register0ResetAndNoJump():
    thisAssemblyLanguageInstance:assemb.assemblyLanguage = assemb.assemblyLanguage()
    commandString="SUM IF NEG JUMP 100"
    binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    theCpu:cpu_simulator.CPU = cpu_simulator.CPU()
    theCpu.theClock=1 # The next tick of the CPU will execute the command in register1
    theCpu.register1.fromString(binaryRepresentation) # Store the command in register1
    
    # Set up conditions to test the CPU command
    reg0="0000000000000000"
    theCpu.register0.fromString(reg0)
    assert theCpu.register0.toString()==reg0
    reg2="0000000011111111"
    theCpu.register2.fromString(reg2) # set register7 so we can verify that its overwritten
    assert theCpu.register2.toString()==reg2
    reg3="0110000000000001"
    theCpu.register3.fromString(reg3) # set register7 so we can verify that its overwritten
    assert theCpu.register3.toString()==reg3
    
    # Test that the command does what it's supposed to
    theCpu.tick() # let the CPU execute the specified command in register1
    assert theCpu.register4.toString()=="0110000100000000" # verify that output register

    # Test that register0 got properly reset
    assert theCpu.register0.toString()==reg0 # verify that there was no jump


############### assembler tests ###############
def test_parseExplicitLabel_notLabel_returnsFalse():
    codeLine="SUM"
    thisAssembler:assemb.assembler = assemb.assembler()
    assert len(thisAssembler.symbolTable.keys())==0 # there shouldn't be anything in the symbol table yet
    assert thisAssembler.parseExplicitLabel(codeLine)==False # the codeLine should not be recognized as an explicit label
    assert len(thisAssembler.symbolTable.keys())==0 # there still shouldn't be anything in the symbol table

def test_parseExplicitLabel_8bitLabel_returnsTrue():
    codeLine=r"{foo}:10101010"
    thisAssembler:assemb.assembler = assemb.assembler()
    assert len(thisAssembler.symbolTable.keys())==0 # there shouldn't be anything in the symbol table yet
    assert thisAssembler.parseExplicitLabel(codeLine)==True # the codeLine should not be recognized as an explicit label
    assert len(thisAssembler.symbolTable.keys())==1 # the symbol table should now have an entry for {foo}
    assert thisAssembler.symbolTable[r"{foo}"]=="10101010"

def test_parseExplicitLabel_repeatedLabel_raiseError():
    codeLine1=r"{foo}:10101010"
    codeLine2=r"{foo}:00000000"
    thisAssembler:assemb.assembler = assemb.assembler()
    assert thisAssembler.parseExplicitLabel(codeLine1)==True # the codeLine should not be recognized as an explicit label
    with pytest.raises(RuntimeError):
        thisAssembler.parseExplicitLabel(codeLine2)

def test_parseExplicitLabel_16bitLabel_returnsTrue():
    codeLine=r"{foo}:1010101011111111"
    thisAssembler:assemb.assembler = assemb.assembler()
    assert len(thisAssembler.symbolTable.keys())==0 # there shouldn't be anything in the symbol table yet
    assert thisAssembler.parseExplicitLabel(codeLine)==True # the codeLine should not be recognized as an explicit label
    assert len(thisAssembler.symbolTable.keys())==1 # the symbol table should now have an entry for {foo}
    assert thisAssembler.symbolTable[r"{foo}"]=="1010101011111111"

def test_parseExplicitLabel_12bitLabel_returnsFalse():
    codeLine=r"{bar}:101010101111"
    thisAssembler:assemb.assembler = assemb.assembler()
    assert len(thisAssembler.symbolTable.keys())==0 # there shouldn't be anything in the symbol table yet
    assert thisAssembler.parseExplicitLabel(codeLine)==False # the codeLine should not be recognized as an explicit label
    assert len(thisAssembler.symbolTable.keys())==0 # the symbol table should now have an entry for {foo}

def test_parseExplicitLabel_nonlabelSymbol_returnsFalse():
    codeLine=r"SETTOPBITS {foo}"
    thisAssembler:assemb.assembler = assemb.assembler()
    assert len(thisAssembler.symbolTable.keys())==0 # there shouldn't be anything in the symbol table yet
    assert thisAssembler.parseExplicitLabel(codeLine)==False # the codeLine should not be recognized as an explicit label
    assert len(thisAssembler.symbolTable.keys())==0 # the symbol table should now have an entry for {foo}

def test_cleanWhitespace_noExtraneousWhitespace_linesUnchanged():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"{foo}:01010101")
    codeLines.append(r"{feep}:11111111")
    codeLines.append(r"R2+R3")
    codeLines.append(r"{zork}:")
    codeLines.append(r"COPY 100 111")
    codeLines.append(r"SETTOPBITS {foo}")

    # Clean those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    parsedLines:list[str]=thisAssembler.cleanWhiteSpace(codeLines)
    assert len(parsedLines)==len(codeLines) # no lines were blank, so none were removed
    for lineNum in range(len(parsedLines)):
        assert parsedLines[lineNum]==codeLines[lineNum]

def test_cleanWhitespace_removeRepeatedSpaces():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"COPY  100    111")
    codeLines.append(r" SETTOPBITS   {foo}  ")

    # Clean those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    parsedLines:list[str]=thisAssembler.cleanWhiteSpace(codeLines)
    assert parsedLines[0]==r"COPY 100 111"
    assert parsedLines[1]==r"SETTOPBITS {foo}"

def test_cleanWhitespace_removeBlankLines():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"COPY  100    111")
    codeLines.append("")
    codeLines.append(r" SETTOPBITS   {foo}  ")
    codeLines.append("")

    # Clean those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    parsedLines:list[str]=thisAssembler.cleanWhiteSpace(codeLines)
    assert len(parsedLines)==2
    assert parsedLines[0]==r"COPY 100 111"
    assert parsedLines[1]==r"SETTOPBITS {foo}"

def test_symbolHandler1_validLinesWithSymbols_noErrors():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"{foo}:01010101")
    codeLines.append(r"SETTOPBITS {foo}")

    # Parse those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    parsedLines:list[str]=thisAssembler.symbolHandler1_ExplicitLabels(codeLines)
    assert len(parsedLines)==1
    assert parsedLines[0]==codeLines[1] # We should have removed the line with the label declaration
    assert len(thisAssembler.symbolTable.keys())==1 # the symbol table should now have an entry for {foo}
    assert thisAssembler.symbolTable[r"{foo}"]=="01010101"

def test_symbolHandler1_validLinesWithOutLabels_noErrors():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"SUM")
    codeLines.append(r"SETTOPBITS {foo}")

    # Parse those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    parsedLines:list[str]=thisAssembler.symbolHandler1_ExplicitLabels(codeLines)
    assert len(parsedLines)==2
    assert parsedLines[0]==codeLines[0]
    assert parsedLines[1]==codeLines[1]
    assert len(thisAssembler.symbolTable.keys())==0 # the symbol table should have no entries

def test_symbolHandler2_validLinesWithLabels_noErrors():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"{foo}:01010101")
    codeLines.append(r"{feep}:11111111")
    codeLines.append(r"R2+R3")
    codeLines.append(r"{zork}:")
    codeLines.append(r"COPY 100 111")
    codeLines.append(r"SETTOPBITS {feep}")

    # parse those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    parsedLines1:list[str]=thisAssembler.symbolHandler1_ExplicitLabels(codeLines)
    parsedLines2:list[str]=thisAssembler.symbolHandler2_LinesLabels(parsedLines1)
    assert len(parsedLines2)==3
    assert parsedLines2[0]==codeLines[2] # R2+R3
    assert parsedLines2[1]==codeLines[4] # COPY 100 111
    assert parsedLines2[2]==codeLines[5] # SETTOPBITS {feep}
    assert thisAssembler.symbolTable[r"{foo}"]=="01010101"
    assert thisAssembler.symbolTable[r"{feep}"]=="11111111"
    assert thisAssembler.symbolTable[r"{zork}"]=="0000000000000001"
    
def test_symbolHandler3_validLinesWithLabels_noErrors():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"{foo}:01010101")
    codeLines.append(r"{feep}:11111111")
    codeLines.append(r"R2+R3")
    codeLines.append(r"{zork}:")
    codeLines.append(r"COPY 100 111")
    codeLines.append(r"SETTOPBITS {feep}")
    codeLines.append(r"UNDEF {foo} {feep} JUMP {zork}") # not actually valid assembly language

    # parse those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    parsedLines1:list[str]=thisAssembler.symbolHandler1_ExplicitLabels(codeLines)
    parsedLines2:list[str]=thisAssembler.symbolHandler2_LinesLabels(parsedLines1)
    parsedLines3:list[str]=thisAssembler.symbolHandler3_ReplaceSymbols(parsedLines2)
    assert len(parsedLines3)==4
    assert parsedLines3[0]=="R2+R3"
    assert parsedLines3[1]=="COPY 100 111"
    assert parsedLines3[2]=="SETTOPBITS 11111111"
    assert parsedLines3[3]=="UNDEF 01010101 11111111 JUMP 0000000000000001"

def test_parseToBinary():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"{foo}:01010101")
    codeLines.append(r"{feep}:11111111")
    codeLines.append(r"R2+R3")
    codeLines.append(r"{zork}:")
    codeLines.append(r"COPY 100 111")
    codeLines.append(r"SETTOPBITS {feep}")

    # parse and compile those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    parsedLines1:list[str]=thisAssembler.symbolHandler1_ExplicitLabels(codeLines)
    parsedLines2:list[str]=thisAssembler.symbolHandler2_LinesLabels(parsedLines1)
    parsedLines3:list[str]=thisAssembler.symbolHandler3_ReplaceSymbols(parsedLines2)
    binaryLines:list[str]=thisAssembler.parseToBinary(parsedLines3)

    # check that the lines of binary are as expected
    assert len(binaryLines)==3
    assert binaryLines[0]=="0000000010000101" # R2+R3 as binary
    assert binaryLines[1]=="0000000"+"111"+"100"+"100"
    assert binaryLines[2]=="00000"+"11111111"+"011"

def test_compile():
    # Set up the lines of code to parse
    codeLines:list[str]=[]
    codeLines.append(r"{foo}:01010101")
    codeLines.append(r"{feep}:11111111")
    codeLines.append(r"R2+R3")
    codeLines.append(r"{zork}:")
    codeLines.append(r"COPY 100 111")
    codeLines.append(r"SETTOPBITS {feep}")

    # parse and compile those lines of code
    thisAssembler:assemb.assembler = assemb.assembler() # set up the assembler
    binaryLines:list[str]=thisAssembler.compile(codeLines)

    # check that the lines of binary are as expected
    assert len(binaryLines)==3
    assert binaryLines[0]=="0000000010000101" # R2+R3 as binary
    assert binaryLines[1]=="0000000"+"111"+"100"+"100"
    assert binaryLines[2]=="00000"+"11111111"+"011"