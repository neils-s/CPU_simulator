# This is an assembler program to take a simple assembly language and convert it into binary code.

import cpu_simulator as cpu
import re # used to match to assembly language commands


class assemblyLanguageCommand:
    """A class to contain assembly language commands for this CPU.  It holds a regular-expression matcher for human-readable Assembly language and convert it to the binary representation."""

    def __init__(self)->None:
        self.reMatch:str="" # A regular expression representing the assembly language command.  Example is "STORE"
        self.description:str="" # A human-readable description of this assembly language command
        self.convertToBinary:callable[list[str],str] = (lambda unused : "1111111111111111") # default to converting every input string to a No-Op

    def tryStringMatchesCommand(self,assemblyLanguageString:str) -> tuple[list[str],str]:
        """If the string matches this assembly language instruction, the binary arguments from the command and the byte string for the machine language command will be returned."""
        reResult=re.fullmatch(self.reMatch,assemblyLanguageString)
        if reResult==None:
            return None,None
        commandParams:list[str] = reResult.groups()
        return commandParams,self.convertToBinary(commandParams)


class assemblyLanguage:
    """A class to hold the entire assembly language for this CPU, as well methods to match a string to an assembly language command."""

    def __init__(self)->None:
        self.commands:list[assemblyLanguageCommand] = self.setupAL()

    def findAndParseAssemblyCommand(self,commandString:str) -> tuple[assemblyLanguageCommand,list[str],str]:
        """Given an input string, this finds the matching assembly language command and returns the command, the arguments parsed out of the string, and the binary string."""
        matchedCommand:assemblyLanguageCommand = None
        parsedCommandParams:list[str] = []
        binaryRepresentation:str=""
        for command in self.commands:
            parsedCommandParams,binaryRepresentation=command.tryStringMatchesCommand(commandString)
            if binaryRepresentation==None:
                continue
            matchedCommand=command
            break
        if matchedCommand == None:
            return None,None,None
        return matchedCommand,parsedCommandParams,binaryRepresentation

    def setupAL(self) -> list[assemblyLanguageCommand]:
        returnList:list[assemblyLanguageCommand] = []

        storeCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        storeCommand.reMatch="STORE"
        storeCommand.description="Stores the contents of register7 into the RAM address specified by register5."
        storeCommand.convertToBinary = lambda unused : "0000000000000000" # The easiest bytecode for the 
        returnList.append(storeCommand)

        loadCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        loadCommand.reMatch="LOAD"
        loadCommand.description="Load into register6 the contents of the RAM address specified by register5.  Will error if the RAM is unset."
        loadCommand.convertToBinary = lambda unused : "0000000000000001" # The easiest bytecode for the 
        returnList.append(loadCommand)

        setlowCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        setlowCommand.reMatch="SETLOWBITS ([01]{8})"
        setlowCommand.description="Set the low 8 (rightmost) 8 bits of register7 to the literal value supplied as the argument for this command."
        setlowCommand.convertToBinary = lambda stringList : "00000"+stringList[0]+"010"
        returnList.append(setlowCommand)

        settopCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        settopCommand.reMatch="SETTOPBITS ([01]{8})"
        settopCommand.description="Set the hi 8 (leftmost) 8 bits of register7 to the literal value supplied as the argument for this command."
        settopCommand.convertToBinary = lambda stringList : "00000"+stringList[0]+"011"
        returnList.append(settopCommand)

        copyCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        copyCommand.reMatch="COPY ([01]{3}) ([01]{3})"
        copyCommand.description="Copy the value of the register indicated by the 1st argument into the register indicated by the 2nd argument (except register1)."
        copyCommand.convertToBinary = lambda stringList : "0000000"+stringList[1]+stringList[0]+"100"
        returnList.append(copyCommand)

        aluCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        aluCommand.reMatch="ALU ([01]{6})"
        aluCommand.description="Performs the ALU command indicated by the 6 bits given in the first argument.  The inputs to the command are register2 and register4.  The output is placed in register4."
        aluCommand.convertToBinary = lambda stringList : "00"+"00"+stringList[0]+"000"+"101"
        returnList.append(aluCommand)

        aluWithJumpCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        aluWithJumpCommand.reMatch="ALU ([01]{6}) IF ([01]{2}) JUMP ([01]{3})"
        aluWithJumpCommand.description="Performs that ALU command indicated by the 6 bits given in the first argument.  The inputs to the command are register2 and register4.  The output is placed in register4.  If the output of the ALU operation is negative or zero (depending on the 2nd argument), then the value of the register indicated by the 3rd argument will be copied to register0.  This will cause code flow to 'jump'."
        aluWithJumpCommand.convertToBinary = lambda stringList : "00"+stringList[1]+stringList[0]+stringList[2]+"101"
        returnList.append(aluWithJumpCommand)
        
        andCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        andCommand.reMatch="AND"
        andCommand.description="Bitwise 'AND' operation.  Puts (register2 AND register3) into register4."
        andCommand.convertToBinary = lambda stringList : "0000000000000101"
        returnList.append(andCommand)
        
        andJumpIfFalseCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        andJumpIfFalseCommand.reMatch="AND IF FALSE JUMP ([01]{3})"
        andJumpIfFalseCommand.description="Bitwise 'AND' operation.  Puts (register2 AND register3) into register4.  If the value placed in register4 is all zeros, the contents of the register indicated by the 1st argument is placed in register0; causing the code flow to 'jump'."
        andJumpIfFalseCommand.convertToBinary = lambda stringList : "0010000000"+stringList[0]+"101"
        returnList.append(andJumpIfFalseCommand)

        andJumpIfTrueCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        andJumpIfTrueCommand.reMatch="AND IF TRUE JUMP ([01]{3})"
        andJumpIfTrueCommand.description="Bitwise 'AND' operation.  Puts (register2 AND register3) into register4.  If the any of the bits placed in register4 is TRUE, the contents of the register indicated by the 1st argument is placed in register0; causing the code flow to 'jump'."
        andJumpIfTrueCommand.convertToBinary = lambda stringList : "0001000000"+stringList[0]+"101"
        returnList.append(andJumpIfTrueCommand)

        orCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        orCommand.reMatch="OR"
        orCommand.description="Bitwise 'OR' operation.  Puts (register2 OR register3) into register4."
        orCommand.convertToBinary = lambda stringList : "0000010101000101"
        returnList.append(orCommand)
        
        ofJumpIfFalseCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        ofJumpIfFalseCommand.reMatch="OR IF FALSE JUMP ([01]{3})"
        ofJumpIfFalseCommand.description="Bitwise 'OR' operation.  Puts (register2 OR register3) into register4.  If the value placed in register4 is all zeros, the contents of the register indicated by the 1st argument is placed in register0; causing the code flow to 'jump'."
        ofJumpIfFalseCommand.convertToBinary = lambda stringList : "0010010101"+stringList[0]+"101"
        returnList.append(ofJumpIfFalseCommand)

        ofJumpIfTrueCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        ofJumpIfTrueCommand.reMatch="OR IF TRUE JUMP ([01]{3})"
        ofJumpIfTrueCommand.description="Bitwise 'OR' operation.  Puts (register2 OR register3) into register4.  If the any of the bits placed in register4 is TRUE, the contents of the register indicated by the 1st argument is placed in register0; causing the code flow to 'jump'."
        ofJumpIfTrueCommand.convertToBinary = lambda stringList : "0001010101"+stringList[0]+"101"
        returnList.append(ofJumpIfTrueCommand)

        zeroCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        zeroCommand.reMatch="ZERO"
        zeroCommand.description="Places all zeros in register4."
        zeroCommand.convertToBinary = lambda stringList : "0000101010000101"
        returnList.append(zeroCommand)

        zeroJumpCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        zeroJumpCommand.reMatch="ZERO JMP ([01]{3})"
        zeroJumpCommand.description="Places all zeros in register4 and sets register0 to the value in whatever register is indicated by the argument.  This 'jumps' the code flow."
        zeroJumpCommand.convertToBinary = lambda stringList : "0000101010"+stringList[0]+"101"
        returnList.append(zeroJumpCommand)

        oneCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        oneCommand.reMatch="ONE"
        oneCommand.description="Places the binary value for '1' in register4."
        oneCommand.convertToBinary = lambda stringList : "0000111111000101"
        returnList.append(oneCommand)

        notR2Command:assemblyLanguageCommand=assemblyLanguageCommand()
        notR2Command.reMatch="NOT R2"
        notR2Command.description="Places the bitwise NOT of register2 into register4."
        notR2Command.convertToBinary = lambda stringList : "0000001101000101"
        returnList.append(notR2Command)

        notR3Command:assemblyLanguageCommand=assemblyLanguageCommand()
        notR3Command.reMatch="NOT R3"
        notR3Command.description="Places the bitwise NOT of register3 into register4."
        notR3Command.convertToBinary = lambda stringList : "0000110001000101"
        returnList.append(notR3Command)

        ndegR2Command:assemblyLanguageCommand=assemblyLanguageCommand()
        ndegR2Command.reMatch="NEG R2"
        ndegR2Command.description="Places the negative of the binary number from register2 into register4."
        ndegR2Command.convertToBinary = lambda stringList : "0000001111000101"
        returnList.append(ndegR2Command)

        negR3Command:assemblyLanguageCommand=assemblyLanguageCommand()
        negR3Command.reMatch="NEG R3"
        negR3Command.description="Places the negative of the binary number from register3 into register4."
        negR3Command.convertToBinary = lambda stringList : "0000110011000101"
        returnList.append(negR3Command)

        r2PlusR3Command:assemblyLanguageCommand=assemblyLanguageCommand()
        r2PlusR3Command.reMatch="R2+R3"
        r2PlusR3Command.description="Places the value of register2 + register3 into register4."
        r2PlusR3Command.convertToBinary = lambda stringList : "0000000010000101"
        returnList.append(r2PlusR3Command)

        sumCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        sumCommand.reMatch="SUM"
        sumCommand.description="Places register2 + register3 into register4."
        sumCommand.convertToBinary = lambda stringList : "0000000010000101"
        returnList.append(sumCommand)

        sumCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        sumCommand.reMatch="ADD"
        sumCommand.description="Places register2 + register3 into register4."
        sumCommand.convertToBinary = lambda stringList : "0000000010000101"
        returnList.append(sumCommand)

        sumCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        sumCommand.reMatch="SUM IF NEG JUMP ([01]{3})"
        sumCommand.description="Places register2 + register3 into register4.  If the value placed into register4 is negative (has a leading bit of 1), then the value in the register given by the argument will be copied to register0, causing the code flow to 'jump'."
        sumCommand.convertToBinary = lambda stringList : "0001"+"000010"+stringList[0]+"101"
        returnList.append(sumCommand)

        r2MinusR3Command:assemblyLanguageCommand=assemblyLanguageCommand()
        r2MinusR3Command.reMatch="R2-R3"
        r2MinusR3Command.description="Places the value of register2-register3 into register4."
        r2MinusR3Command.convertToBinary = lambda stringList : "0000010011000101"
        returnList.append(r2MinusR3Command)

        r2MinusR3JumpIfNegCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        r2MinusR3JumpIfNegCommand.reMatch="R2-R3 IF NEG JUMP ([01]{3})"
        r2MinusR3JumpIfNegCommand.description="Places the value of register2-register3 into register4.  If the value placed in register4 is negative, the value from the register in the given argument will be copied into register0, causing code flow to 'jump'."
        r2MinusR3JumpIfNegCommand.convertToBinary = lambda stringList : "0001010011"+stringList[0]+"101"
        returnList.append(r2MinusR3JumpIfNegCommand)

        r2MinusR3JumpIfZeroCommand:assemblyLanguageCommand=assemblyLanguageCommand()
        r2MinusR3JumpIfZeroCommand.reMatch="R2-R3 IF ZERO JUMP ([01]{3})"
        r2MinusR3JumpIfZeroCommand.description="Places the value of register2-register3 into register4.  If the value placed in register4 is negative, the value from the register in the given argument will be copied into register0, causing code flow to 'jump'."
        r2MinusR3JumpIfZeroCommand.convertToBinary = lambda stringList : "0010010011"+stringList[0]+"101"
        returnList.append(r2MinusR3JumpIfZeroCommand)

        return returnList