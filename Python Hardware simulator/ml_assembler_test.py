import ml_assembler as asssemb
import cpu_simulator
import pytest

def test_assemblyLanguage_initializeWithoutError():
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    assert thisAssemblyLanguageInstance != None

def test_findAndParseAssemblyCommand_mathesSTORE():
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="STORE"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="0000000000000000"

def test_findAndParseAssemblyCommand_mathesLOAD():
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="LOAD"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="0000000000000001"

def test_findAndParseAssemblyCommand_all0_mathesSETLOWBITS():
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="SETLOWBITS 00000000"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="0000000000000010"

def test_executeAssemblyCommand_all0_SETLOWBITS():
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="SETLOWBITS 00000000"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
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
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="SETLOWBITS 00000001"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="0000000000001010"

def test_executeAssemblyCommand_ADD_register4Set():
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="ADD"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
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
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="ADD"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
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
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
    assert binaryRepresentation=="00"+"01"+"000010"+"100"+"101"

def test_executeAssemblyCommand_ADD_withJUMP_register0ResetAndJump():
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="SUM IF NEG JUMP 100"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
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
    thisAssemblyLanguageInstance:asssemb.assemblyLanguage = asssemb.assemblyLanguage()
    commandString="SUM IF NEG JUMP 100"
    matchedCommand,parsedCommandParams,binaryRepresentation = thisAssemblyLanguageInstance.findAndParseAssemblyCommand(commandString)
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

