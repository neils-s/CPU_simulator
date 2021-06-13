# This is an assembler program to take a simple assembly language and convert it into binary code.

import cpu_simulator as cpu
import re # used to match to assembly language commands


class assemblyLanguageCommand:
    """A class to contain assembly language commands for this CPU.  It holds a regular-expression matcher for human-readable Assembly language and convert it to the binary representation."""

    def __init__(self)->None:
        self.reMatch:str="" # A regular expression to.  Example is "STORE"
        self.description:str="" # A human-readable description of this assembly language command
        self.convertToBinary:callable[list[str],str] = (lambda unused : "1111111111111111") # default to converting every input string to a No-Op

    def tryStringMatchesCommand(self,assemblyLanguageString:str) -> str:
        """If the string matches this assembly language instruction, the matching byte string for the command will be returned."""
        reResult=re.search(self.reMatch,assemblyLanguageString)
        if reResult==None:
            return None
        return self.convertToBinary(assemblyLanguageString)


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
            parsedCommandParams=command.tryStringMatchesCommand(commandString)
            if parsedCommandParams==None:
                continue
            matchedCommand=command
            break
        if matchedCommand != None:
            binaryRepresentation=matchedCommand.convertToBinary(parsedCommandParams)
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

