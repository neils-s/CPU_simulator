import typing # used to type the returned groups of regular expressions and lists
import numpy # used for sized arrays
import re # used to match to machine language commands
import random # used to randomly assign the starting state of bytes

class event():
    """A convenient shim class for event management."""

    def __init__(self) -> None:
        self._dictionaryOfReactions:dict[object,callable]=dict()
    
    def setReaction(self,reactingObject,reaction:callable) -> None:
        self._dictionaryOfReactions[reactingObject]=reaction # we only allow one reaction per event
    
    def removeReaction(self,reactingObject) -> None:
        self._dictionaryOfReactions[reactingObject] = None
    
    def clear(self) -> None:
        self._dictionaryOfReactions.clear()

    def fire(self,*args,**kwArgs) -> None:
        for reactingObject in self._dictionaryOfReactions.keys():
            reaction:callable = self._dictionaryOfReactions[reactingObject]
            if reaction != None:
                reaction(*args,**kwArgs)


class cpuByte:
    """The data type to hold a single byte in the simulated hardware. Note that the contents start in an undefined state."""

    # shared class variables
    _size:int = 16 # The number of bits in a byte
    _maxVal:int = (2**_size) - 1 # The maximum unsigned integer value we can store in one of these bytes

    @staticmethod
    def isValidBinaryString(val:str) -> bool:
        if len(val)!=cpuByte._size:
            return False
        pattern:str ="[01]{"+str(cpuByte._size)+"}"
        return re.match(pattern,val) != None

    @staticmethod
    def bitStringToUnsignedInt(val:str)->int:
        valAsInt:int=0
        multiplier:int=1
        for position in range(cpuByte._size):
            reversePos:int = cpuByte._size-position-1 # we have to reverse the order (endianness)
            aChar:str = val[reversePos]
            valAsInt = valAsInt+ multiplier if aChar=="1" else 0
            multiplier = multiplier*2
        return valAsInt
    
    @staticmethod
    def unsignedIntegerToBitString(val:int)->str:
        output:str=""
        for position in range(cpuByte._size):
            output= ("1" if val%2==1 else "0")+output
            val=val//2
        return output

    def __init__(self,randomize:bool=None):
        self._state:numpy.ndarray=numpy.empty(self._size, dtype=bool)
        self.onChangeEvent:event=event()
        if randomize==None:
            return
        for i in range(self._size):
            if not randomize:
                self._state[i]=False
            else:
                self._state[i]=(random.getrandbits(1)==1)

    def getBit(self,whichBit:int) -> bool:
        """Retrieves the specified bit from this byte"""
        return (self.toString()[whichBit]=="1")

    def setBit(self,whichBit:int,val:bool) -> None:
        """Sets the specified bit from this byte"""
        self.setBitsFromString(whichBit,"1" if val else "0")
    
    def setBitsFromString(self,offset:int,bitString:str) -> None:
        """Sets a collection of bits in the cpuByte to match the specified string.  If the bit string is too long or offset is too large, this will (rightly) throw an error."""
        span:tuple[int,int] = re.search("[01].*",bitString).span()
        if len(bitString) != (span[1]-span[0]):
            raise Exception("(Partial) bitstrings need to be composed of only 0 and 1.  Incorrect value: "+bitString)
        oldValue:str = self.toString()
        newValue:str = oldValue[0:offset]+bitString
        newValue=newValue+oldValue[len(newValue):self._size] # this will rightly throw an error if the size of old value was somehow wrong
        self.fromString(newValue)

    def asUnsignedInteger(self) -> int:
        returnable:int=0
        position:int=0
        for aBool in self._state:
            if aBool==True:
                returnable = returnable + 2**position
            position += 1
        return returnable
    
    def asSignedInteger(self) -> int:
        returnable:int=0
        for position in range(cpuByte._size-1):
            aBool=self._state[position]
            if aBool==True:
                returnable = returnable + 2**position
        if self._state[cpuByte._size-1]:
            returnable=returnable*(-1)
        return returnable
    
    def setFromUnsignedInteger(self,value:int) -> None:
        """Resets the value of this byte so it matches the unsigned value of the integer."""
        oldValue:str = self.toString()
        for position in range(cpuByte._size):
            self._state[position]=(value % 2 == 1)
            value=value//2
        newValue:str = self.toString()
        self.onChangeEvent.fire(oldValue,newValue) # alert other interested parties to the change in this byte
    
    def setFromSignedInteger(self,value:int) -> None:
        """Resets the value of this byte so it matches the (signed) value of the integer."""
        oldValue:str = self.toString()
        for position in range(cpuByte._size-1):
            self._state=(value % 2 == 1)
            value=value//2
        if value<0:
            self._state[cpuByte._size-1]=True
        else:
            self._state[cpuByte._size-1]=False
        newValue:str = self.toString()
        self.onChangeEvent.fire(oldValue,newValue) # alert other interested parties to the change in this byte

    def toString(self) -> str:
        """Returns the contents of a byte as a string of 1s and 0s."""
        returnable:str=""
        for position in range(cpuByte._size):
            thisBit:str
            if self._state[position]:
                thisBit="1"
            else:
                thisBit="0"
            returnable=thisBit+returnable # this reverses the order (endianness)
        return returnable
    
    def fromString(self,val:str) -> None:
        """Converts a string of 0s and 1s into a byte."""
        oldValue:str = self.toString()
        for position in range(cpuByte._size):
            reversePos:int = cpuByte._size-position-1 # we have to reverse the order (endianness)
            aChar:str = val[reversePos]
            self._state[position]=(aChar=="1")
        newValue:str = self.toString()
        self.onChangeEvent.fire(oldValue,newValue) # alert other interested parties to the change in this byte


class RAM:
    """This class will hold the RAM for the simulated hardware"""
    _addressCount:int=2**cpuByte._size # the number of addresses in the RAM

    def __init__(self,randomize:bool=None):
        self._state:numpy.ndarray=numpy.empty(self._addressCount, dtype=cpuByte) # the array of bytes in the RAM
        self.onChangeEvent:event=event() # we'll fire this event whenever the RAM is changed.
        self._randomizeInitialBytes:bool=randomize # whether we randomize the values of RAM on construction
        if randomize==None:
            return # if we're not explicitly told to randomize or not, then we won't set the initial state of the RAM.  This can lead to exciting errors later.
        for address in range(self._addressCount):
            self.initializeRamByteIfNecessary(address,randomize)

    def SET(self,address:cpuByte,data:cpuByte) -> None:
        addressAsInt:int = address.asUnsignedInteger()
        self.setUsingUnsignedIntAsAddress(addressAsInt,data)
    
    def GET(self,address:cpuByte) -> cpuByte:
        addressAsInt:int = address.asUnsignedInteger()
        return self.getUsingIntegerAddress(addressAsInt)

    def getUsingIntegerAddress(self,addressAsInt:int) ->cpuByte:
        self.initializeRamByteIfNecessary(addressAsInt)
        return self._state[addressAsInt]

    def setUsingUnsignedIntAsAddress(self,addressAsInt:int,data:cpuByte) -> None:
        valAsStr:str = data.toString()
        self.setUsingUnsignedIntegerAddressAndBitStringValue(addressAsInt,valAsStr)

    def setUsingBitStringAddressAndValue(self,addressAsStr:str,valAsStr:str) -> None:
        addressAsInt:int=cpuByte.bitStringToUnsignedInt(addressAsStr)
        self.setUsingUnsignedIntegerAddressAndBitStringValue(addressAsInt,valAsStr)

    def setUsingUnsignedIntegerAddressAndBitStringValue(self,addressAsInt:int,valAsStr:str) -> None:
        self.initializeRamByteIfNecessary(addressAsInt)
        oldValueByte:cpuByte = self._state[addressAsInt]
        oldValue:str = None if oldValueByte==None else oldValueByte.toString()
        self._state[addressAsInt].fromString(valAsStr)
        newValue:str = self._state[addressAsInt].toString()
        self.onChangeEvent.fire(addressAsInt,oldValue,newValue) # alert other interested parties to the change in this byte

    @staticmethod
    def unsignedIntegerToBitString(value:int) -> str:
        returnString=""
        for position in range(cpuByte._size):
            returnString=("1" if value%2==1 else "0") + returnString
            value = value // 2 #integer division
        return returnString

    def initializeRamByteIfNecessary(self,addressAsInt:int) -> None:
        if self._state[addressAsInt] == None:
            self._state[addressAsInt] = cpuByte(self._randomizeInitialBytes)
    
    def allRAM(self) -> typing.List[str]:
        """Returns a list of all of the RAM values."""
        returnList:typing.List[str] = []
        for address in range(self._addressCount):
            returnList.append(self.getUsingIntegerAddress(address).toString())
        return returnList

    def ramTable(self,starting_address:int=None,how_many_addresses:int=None) -> typing.List[typing.List[str]]:
        """Returns a table of binary string RAM addresses and binary string values.
        starting_address = starting address of the RAM addresses to return.
        how_many_addresses = the number of RAM addresses and values to return.
        If starting_address isn't specified, then all RAM addresses will be returned.
        If starting_address is specified, the a missing how_many_addresses will be treated as 1."""
        if starting_address==None:
            starting_address=0
            how_many_addresses=self._addressCount
        elif how_many_addresses==None:
            how_many_addresses=1
        endAddress:int=min(self._addressCount,starting_address+how_many_addresses)
        returnTable:typing.List[typing.List[str]]=[]
        for address in range(starting_address,endAddress):
            thisRow:typing.List[str]=[]
            thisRow.append(self.unsignedIntegerToBitString(address))
            thisRow.append(self.getUsingIntegerAddress(address).toString())
            returnTable.append(thisRow)
        return returnTable


class ALU:
    @staticmethod
    def AND(X:cpuByte,Y:cpuByte) -> cpuByte:
        """Takes the bitwise AND of two bytes."""
        returnable:cpuByte=cpuByte()
        for position in range(cpuByte._size):
            returnable._state[position] = X._state[position] & Y._state[position]
        return returnable

    @staticmethod
    def addOneDigit(X:bool,Y:bool,c:bool) -> tuple[bool,bool]:
        countOfTrue:int=0
        if X:
            countOfTrue=countOfTrue+1
        if Y:
            countOfTrue=countOfTrue+1
        if c:
            countOfTrue=countOfTrue+1
        result:bool = (countOfTrue%2==1)
        carry:bool = (countOfTrue>1)
        return result,carry

    @staticmethod
    def ADD(X:cpuByte,Y:cpuByte) -> cpuByte:
        """Adds two bytes and returns the results."""
        returnable:cpuByte=cpuByte()
        carry:bool=False
        result:bool
        for position in range(cpuByte._size): # -1,-1,-1
            xDigit:bool=X._state[position]
            yDigit:bool=Y._state[position]
            result,carry = ALU.addOneDigit(xDigit,yDigit,carry)
            returnable._state[position]=result
        return returnable

    @staticmethod
    def negation(X:cpuByte) -> cpuByte:
        """Bitwise negation of a cpuByte"""
        returnable:cpuByte=cpuByte()
        for position in range(cpuByte._size):
            returnable._state[position] = not(X._state[position])
        return returnable

    @staticmethod
    def zero() -> cpuByte:
        """Returns the 'zero byte'.  That is to say, it returns the byte that is false in all bits."""
        returnable:cpuByte=cpuByte()
        for position in range(cpuByte._size):
            returnable._state[position] = False
        return returnable

    @staticmethod
    def isZero(X:cpuByte)->bool:
        """Checks if X represents 0 or -0 by checking if all of the bits except the highest bit are FALSE."""
        for position in range (cpuByte._size-1):
            if X._state[position]:
                return False # we've found a single bit where X deviates from 0
        return True

    @staticmethod
    def isNegative(X:cpuByte) -> bool:
        """Checks if the leading (sign) bit is true (making a negative number) or false (making a positive number)."""
        return X._state[cpuByte._size-1]

    @staticmethod
    def preprocessor(X:cpuByte,zeroX:bool,negateX:bool) -> cpuByte:
        internalX:cpuByte = X
        if zeroX:
            internalX=ALU.zero()
        if negateX:
            internalX=ALU.negation(internalX)
        return internalX

    @staticmethod
    def evaluate(X:cpuByte,Y:cpuByte,zeroX:bool,negateX:bool,zeroY:bool,negateY:bool,addOrAnd:bool,negateOut:bool) -> tuple[cpuByte,bool,bool]:
        """Simulates the operation of the ALU given the inputs.  Returns a tuple with the following information:
                1) A byte containing the result of the evaluation
                2) A bool that copies the highest bit of the result (the "2's complement sign" of the result)
                3) A bool that says if all of the bits except the highest are FALSE."""
        internalX:cpuByte = ALU.preprocessor(X,zeroX,negateX)
        internalY:cpuByte = ALU.preprocessor(Y,zeroY,negateY)
        out:cpuByte
        if addOrAnd:
            out=ALU.ADD(internalX,internalY)
        else:
            out=ALU.AND(internalX,internalY)
        if negateOut:
            out=ALU.negation(out)
        outIsNegative:bool = ALU.isNegative(out)
        outIsZero:bool = ALU.isZero(out)
        return out,outIsNegative,outIsZero


class machineLanguageCommand:
    """A convenient bucket to hold ML commands for this CPU."""

    def __init__(self) -> None:
        self.reMatch:str="" # regular expression matcher
        self.description:str="" # human readable description
        self.action:callable = (lambda aSequenceOfStrings : None) # default to doing no action

    def tryStringMatchesCommand(self,mlBinaryString:str) -> typing.Sequence[str]:
        """If the binary string matches this command, the parameter sequence parsed from the binary string will be returned."""
        reResult=re.search(self.reMatch,mlBinaryString)
        if reResult==None:
            return None
        return reResult.groups()


class CPU():

    def __init__(self) -> None:
        self.theClock:int=2
        self.theRAM:RAM = RAM()
        self.register0:cpuByte=cpuByte() # The RAM address to pull the next instruction from.  Incremented during clock tick 1
        self.register1:cpuByte=cpuByte() # The instruction we're currently working on.  *Only* set during clock tick 0
        self.register2:cpuByte=cpuByte() # Where the ALU will pull its X-input from
        self.register3:cpuByte=cpuByte() # Where the ALU will pull its Y-input from
        self.register4:cpuByte=cpuByte() # Where the ALU will put its output
        self.register5:cpuByte=cpuByte() # Holds a value typically used as a RAM address
        self.register6:cpuByte=cpuByte() # This register can be written to RAM
        self.register7:cpuByte=cpuByte() # This register can be copied from a RAM address
        self.mlCommandList:list[machineLanguageCommand]=self.setupML()

        self.register0_description:str="The RAM address to pull the next instruction from.  Incremented during clock tick 1."
        self.register1_description:str="The instruction we're currently working on.  *Only* set during clock tick 0."
        self.register2_description:str="Where the ALU will pull its X-input from"
        self.register3_description:str="Where the ALU will pull its Y-input from"
        self.register4_description:str="Where the ALU will put its output"
        self.register5_description:str="Holds a value typically used as a RAM address"
        self.register6_description:str="This register can be written to RAM"
        self.register7_description:str="This register can be copied from a RAM address"

        self.onAluCommand:event = event()
        self.onTick:event=event()
        self.onParseML:event=event()

        self.register0.fromString("0000000000000000") # We initialize the starting value of register 0 to point to RAM address 0

    def getRegister(self,threeBits:str) -> cpuByte:
        if threeBits=="000":
            return self.register0
        if threeBits=="001":
            return self.register1
        if threeBits=="010":
            return self.register2
        if threeBits=="011":
            return self.register3
        if threeBits=="100":
            return self.register4
        if threeBits=="101":
            return self.register5
        if threeBits=="110":
            return self.register6
        if threeBits=="111":
            return self.register7
        raise Exception("the bit string "+threeBits+" doesn't correspond to a register.")

    def aluCommand(self,conditionalFlags:str,aluDirectives:str,jumpRegisterDirective:str) -> None:
        """Carry out the ALU operation specified by the 6-bits in the aluDirective.  
        Register2 is used as the X-input, register3 is used as the Y-input, and the output will be stored to register4.  
        If the 2-bits of the conditionalFlags match the bool output of the ALU, then the contents of the register indicated by 
        the 3-bit jumpRegisterDirective will be copied to register0 (unless SSS=000), thereby causing program flow to 'jump'."""
        
        # parse the conditional flag bits and the ALU directive bits
        JumpIfOutIsZero:bool = (conditionalFlags[0]=="1")
        JumpIfOutIsNeg:bool = (conditionalFlags[1]=="1")
        setXtoZero:bool = (aluDirectives[0]=="1")
        negateX:bool = (aluDirectives[1]=="1")
        setYtoZero:bool = (aluDirectives[2]=="1")
        negateY:bool = (aluDirectives[3]=="1")
        addOrAnd:bool = (aluDirectives[4]=="1")
        negateOut:bool = (aluDirectives[5]=="1")
        jumpRegisterDirective = jumpRegisterDirective[0:3]

        self.onAluCommand.fire(conditionalFlags,aluDirectives,jumpRegisterDirective)

        # Carry out the ALU operation, using registers 2 and 3 as inputs and the ALU directives parsed above, storing the result to register 4
        aluOut:tuple[cpuByte,bool,bool] =  ALU.evaluate(self.register2,self.register3,setXtoZero,negateX,setYtoZero,negateY,addOrAnd,negateOut)
        self.register4=aluOut[0]

        # Use the conditional flags parsed above and the jumpRegisterDirective to decide if we're rewriting register0 (to jump the code flow)
        if (jumpRegisterDirective!="000") & (JumpIfOutIsNeg==aluOut[1]) & (JumpIfOutIsZero==aluOut[2]):
            sourceRegister:cpuByte = self.getRegister(jumpRegisterDirective)
            self.register0.fromString(sourceRegister.toString())

    def tick(self) -> None:
        """Causes the CPU clock to 'tick' forward to it's next state and perform the actions associated with that state."""
        self.theClock = (self.theClock+1)%3
        self.onTick.fire(self.theClock) # fire the events for the clock, passing in the current clock counter

        if self.theClock==0:
            # on tick 0 we copy the RAM addressed by the "code pointer" (register 0) into the "instruction register" (register 1).  This is the only time we write register 1.
            self.register1.fromString(self.theRAM.GET(self.register0).toString())
            return
        if self.theClock==1:
            # On tick 1 we'll increment register0 by 1.  This will move the instruction pointer it to the presumptive next instruction.
            reg0_uint:int=self.register0.asUnsignedInteger()
            reg0_uint=reg0_uint + 1
            self.register0.setFromUnsignedInteger(reg0_uint) # note that we don't handle instruction overflows on the CPU
            return
        if self.theClock==2:
            # On tick 2 we'll execute the ML instruction in register 1 to do the actual work
            matchedCommand, parsedCommandParams = self.findAndParseML(self.register1) # parse the ML binary
            matchedCommand.action(parsedCommandParams) # carry out the operation.  This will rightly throw an eror if the binary command didn't match an instruction
            return
        raise Exception("Undefined clock tick detected.") # this should never happen!

    def findAndParseML(self,mlByte:cpuByte) -> tuple[machineLanguageCommand,typing.Sequence[str]]:
        """Finds the machine language command from the list of ML commands and parses out the parameters from the binary string."""
        mlBinaryString:str = mlByte.toString()
        matchedCommand:machineLanguageCommand = None
        parsedCommandParams:typing.Sequence[str] = None
        for mlCommand in self.mlCommandList:
            parsedCommandParams=mlCommand.tryStringMatchesCommand(mlBinaryString)
            if parsedCommandParams==None:
                continue
            matchedCommand=mlCommand
            break
        self.onParseML.fire(mlBinaryString,matchedCommand,parsedCommandParams) # fire the event that alerts others that a ML command will be executed
        return matchedCommand,parsedCommandParams

    def setupML(self) -> list[machineLanguageCommand]:
        returnList:list[machineLanguageCommand] = []

        storeCommand:machineLanguageCommand=machineLanguageCommand()
        storeCommand.reMatch=".{13}000"
        storeCommand.description="Stores the contents of register7 into the RAM address specified by register5."
        storeCommand.action = lambda unused : self.theRAM.SET(self.register5,self.register7)
        returnList.append(storeCommand)

        loadCommand:machineLanguageCommand=machineLanguageCommand()
        loadCommand.reMatch=".{13}001"
        loadCommand.description="Load into register6 the contents of the RAM address specified by register5.  Will error if the RAM is unset."
        loadCommand.action = lambda unused : self.register6.setFromUnsignedInteger(self.theRAM.GET(self.register5).asUnsignedInteger())
        returnList.append(loadCommand)

        setlowCommand:machineLanguageCommand=machineLanguageCommand()
        setlowCommand.reMatch=".{5}([01]{8})010"
        setlowCommand.description="Commands of the form '.....dddddddd010' set the low (rightmost) 8 bits of register7 to the literal value specifed by the 'dddddddd' bits of this command."
        setlowCommand.action=lambda aSequence : self.register7.setBitsFromString(0,aSequence[0])
        returnList.append(setlowCommand)

        settopCommand:machineLanguageCommand=machineLanguageCommand()
        settopCommand.reMatch=".{5}([01]{8})011"
        settopCommand.description="Commands of the form '.....dddddddd011' set the high (leftmost) 8 bits of register7 to the literal value specifed by the 'dddddddd' bits of this command."
        settopCommand.action=lambda aSequence : self.register7.setBitsFromString(8,aSequence[0])
        returnList.append(settopCommand)

        copyCommand:machineLanguageCommand=machineLanguageCommand()
        copyCommand.reMatch=".{7}([01]{3})([01]{3})100"
        copyCommand.description="Commands of the form '.......TTTsss100' copy the contents of the register specified by the 'sss' bits into the register specified by the 'TTT' bits (unless TTT=001)."
        copyCommand.action=lambda aSequence : None if aSequence[0]=="001" else self.getRegister(aSequence[0]).fromString(self.getRegister(aSequence[1]).toString()) # copy to any register except register 1
        returnList.append(copyCommand)

        aluCommand:machineLanguageCommand=machineLanguageCommand()
        aluCommand.reMatch="..([01]{2})([01]{6})([01]{3})101"
        aluCommand.description="Commands of the form '..ccAAAAAAsss101' carry out the ALU operation specified by the 'AAAAAA' bits.  Register2 is used as the X-input, register3 is used as the Y-input, and the output will be stored to register4.  If the 'cc' bits match the output of the ALU, then the contents of the register indicated by SSS will be copied to register0 (unless SSS=000), thereby causing program flow to 'jump'."
        aluCommand.action=lambda aSequence : self.aluCommand(aSequence[0],aSequence[1],aSequence[2])
        returnList.append(aluCommand)

        noCommand1:machineLanguageCommand=machineLanguageCommand()
        noCommand1.reMatch=".{13}110"
        noCommand1.description="The CPU doesn't use this command, and no load bits will get set.  Essentially, this is a 'pass' directive."
        noCommand1.action = lambda aSequence : None
        returnList.append(noCommand1)

        noCommand2:machineLanguageCommand=machineLanguageCommand()
        noCommand2.reMatch=".{13}111"
        noCommand2.description="The CPU doesn't use this command, and no load bits will get set.  Essentially, this is a 'pass' directive."
        noCommand2.action = lambda aSequence : None
        returnList.append(noCommand2)

        return returnList

