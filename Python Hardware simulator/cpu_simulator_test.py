import typing
import cpu_simulator
import pytest

############### event tests ###############
def test_event_eventFiresCorrectly():
    class eventRaiser():
        """This class will expose an event and fire it."""
        def __init__(self):
            self.theEvent:cpu_simulator.event = cpu_simulator.event()
        def fireTheEvent(self,*args, **kwArgs):
            self.theEvent.fire(*args, **kwArgs)

    class eventSubscriber():
        """This class will subscribe to an event and react to it."""
        def __init__(self):
            self.state=False
            self.myReaction:callable = self.setState # some callable
        def setState(self, *args, **kwArgs):
            self.state=True
        def subscribeToEvent(self,theEvent:cpu_simulator.event):
            theEvent.setReaction(self,self.myReaction)
    
    event_raiser = eventRaiser() # will fire the event
    event_listener = eventSubscriber() # will react to the event being fired
    event_listener.subscribeToEvent(event_raiser.theEvent)

    assert event_listener.state==False # make sure that the listener's state is unset
    event_raiser.fireTheEvent() # fire the event
    assert event_listener.state==True # the listener should have responded to the event by setting it's state

def test_multipleListeners_eventFiresCorrectly():
    class eventRaiser():
        """This class will expose an event and fire it."""
        def __init__(self):
            self.theEvent:cpu_simulator.event = cpu_simulator.event()
        def fireTheEvent(self,*args, **kwArgs):
            self.theEvent.fire(*args, **kwArgs)

    class eventSubscriber():
        """This class will subscribe to an event and react to it."""
        def __init__(self):
            self.state=False
            self.myReactedState=True
            self.myReaction:callable = self.setState # some callable
        def setState(self, *args, **kwArgs): # the function that gets called to react
            self.state = self.myReactedState
        def subscribeToEvent(self,theEvent:cpu_simulator.event):
            theEvent.setReaction(self,self.myReaction)
    
    event_raiser = eventRaiser() # will fire the event
    event_listener1 = eventSubscriber() # will react to the event being fired
    event_listener1.subscribeToEvent(event_raiser.theEvent)

    event_listener2 = eventSubscriber() # will react to the event being fired
    event_listener2.state=True
    event_listener2.myReactedState=False
    event_listener2.subscribeToEvent(event_raiser.theEvent)

    assert event_listener1.state==False # make sure that the listener's state is unset
    assert event_listener2.state==True # make sure that the listener's state is unset
    event_raiser.fireTheEvent() # fire the event
    assert event_listener1.state==True # the listener should have responded to the event by setting it's state
    assert event_listener2.state==False # the listener should have responded to the event by setting it's state

def test_multipleEventRaisers_singleEventFiresCorrectly():
    class eventRaiser():
        """This class will expose an event and fire it."""
        def __init__(self):
            self.theEvent:cpu_simulator.event = cpu_simulator.event()
        def fireTheEvent(self,*args, **kwArgs):
            self.theEvent.fire(*args, **kwArgs)

    class eventSubscriber():
        """This class will subscribe to an event and react to it."""
        def __init__(self):
            self.state=False
            self.myReaction:callable = self.setState # some callable
        def setState(self, *args, **kwArgs):
            self.state=True
        def subscribeToEvent(self,theEvent:cpu_simulator.event):
            theEvent.setReaction(self,self.myReaction)
    
    event_raiser1 = eventRaiser() # will fire the event
    event_raiser2 = eventRaiser() # will not fire the event
    event_listener = eventSubscriber() # will react to the event being fired
    event_listener.subscribeToEvent(event_raiser1.theEvent)

    assert event_listener.state==False # make sure that the listener's state is unset
    event_raiser2.fireTheEvent() # fire the event that no-one's listening to
    assert event_listener.state==False # make sure that the listener's state is still unset
    event_raiser1.fireTheEvent() # fire the event
    assert event_listener.state==True # the listener should have responded to the event by setting it's state


############### cpuByte tests ###############

def test_isValidByte_1010_returnFalse():
    bits:str="1010"
    assert cpu_simulator.cpuByte.isValidBinaryString(bits)==False

def test_isValidByte_1010000011110101_returnTrue():
    bits:str="1010000011110101"
    assert cpu_simulator.cpuByte.isValidBinaryString(bits)==True

def test_isValidByte_101000001111010100000_returnFalse():
    bits:str="101000001111010100000"
    assert cpu_simulator.cpuByte.isValidBinaryString(bits)==False

def test_unsignedIntegerToBitString_65535_returns1111111111111111():
    assert cpu_simulator.cpuByte.unsignedIntegerToBitString(65535)=="1111111111111111"

def test_unsignedIntegerToBitString_17_returns0000000000010001():
    assert cpu_simulator.cpuByte.unsignedIntegerToBitString(17)=="0000000000010001"

def test_cpuByte_0101010101010101_FromStringToString_givesSameString():
    startingString:str="0101010101010101"
    aByte:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    aByte.fromString(startingString)
    endingString:str=aByte.toString()
    assert startingString==endingString

def test_cpuByte_0000000011111111_FromStringToString_givesSameString():
    startingString:str="0000000011111111"
    aByte:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    aByte.fromString(startingString)
    endingString:str=aByte.toString()
    assert startingString==endingString

def test_cpuByte_0000111111110000_FromStringToString_givesSameString():
    startingString:str="0000111111110000"
    aByte:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    aByte.fromString(startingString)
    endingString:str=aByte.toString()
    assert startingString==endingString

def test_cpuByte_0000000000000000_asSignedInteger_isZero():
    byteString:str="0000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert aByte.asSignedInteger()==0

def test_cpuByte_0000000000000100_asSignedInteger_isFour():
    byteString:str="0000000000000100"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert aByte.asSignedInteger()==4

def test_cpuByte_1000000000001000_asSignedInteger_isNegEight():
    byteString:str="1000000000001000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert aByte.asSignedInteger()==-8

def test_cpuByte_1000000000000000_asSignedInteger_isZero():
    byteString:str="1000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert aByte.asSignedInteger()==0

def test_cpuByte_1000000000000000_asUnsignedInteger_is32768():
    byteString:str="1000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert aByte.asUnsignedInteger()==32768

def test_cpuByte_1_setFromUnsignedInteger_is0000000000000001():
    uint:int = 1
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.setFromUnsignedInteger(uint)
    assert aByte.toString()=="0000000000000001"

def test_cpuByte_32770_setFromUnsignedInteger_is1000000000000010():
    uint:int = 32770
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.setFromUnsignedInteger(uint)
    assert aByte.toString()=="1000000000000010"

def test_cpuByte_65536_setFromUnsignedInteger_is0000000000000000():
    uint:int = 65536
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.setFromUnsignedInteger(uint)
    assert aByte.toString()=="0000000000000000"

def test_cpuByte_0000000000000000_setLeftmostBitTrue_bitSetCorrectly():
    byteString:str="0000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    aByte.setBit(0,True)
    assert aByte.toString() == "1000000000000000"

def test_cpuByte_0000000000000100_setLeftmostBitTrue_bitSetCorrectly():
    byteString:str="0000000000000100"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    aByte.setBit(0,True)
    assert aByte.toString() == "1000000000000100"

def test_cpuByte_0000000000000000_setRightmostmostBitTrue_bitSetCorrectly():
    byteString:str="0000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    aByte.setBit(15,True)
    assert aByte.toString() == "0000000000000001"

def test_cpuByte_0000000000000100_setRightmostBitTrue_bitSetCorrectly():
    byteString:str="0000000000000100"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    aByte.setBit(15,True)
    assert aByte.toString() == "0000000000000101"

def test_cpuByte_0000000000000100_setLeft6bits_bitSetCorrectly():
    byteString:str="0000000000000100"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    aByte.setBitsFromString(0,"111111")
    assert aByte.toString() == "1111110000000100"

def test_cpuByte_0010000000000101_setMiddle5bits_bitSetCorrectly():
    byteString:str="0010000000000101"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    aByte.setBitsFromString(8,"11111")
    assert aByte.toString() == "0010000011111101"


############### RAM tests ###############

def test_ram_getFromEmpty_rightSizeString():
    theRAM:cpu_simulator.RAM = cpu_simulator.RAM()
    ramAddressString:str = "0010101010111001"
    ramAddressByte:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    ramAddressByte.fromString(ramAddressString)
    ramContentByte:cpu_simulator.cpuByte = theRAM.GET(ramAddressByte)
    ramContentString:str = ramContentByte.toString()

    assert len(ramContentString)==cpu_simulator.cpuByte._size

def test_ram_setAndGet_correctData():
    theRAM:cpu_simulator.RAM = cpu_simulator.RAM()
    ramAddressString:str = "0010101010111001"
    ramAddressByte:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    ramAddressByte.fromString(ramAddressString)

    dataString="1111000011110000"
    dataByte:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    dataByte.fromString(dataString)
    theRAM.SET(ramAddressByte,dataByte)

    ramContentByte:cpu_simulator.cpuByte = theRAM.GET(ramAddressByte)
    ramContentString:str = ramContentByte.toString()

    assert ramContentString==dataString

def test_ram_setAndGetDifferentBytes_correctData():
    theRAM:cpu_simulator.RAM = cpu_simulator.RAM()

    ramAddressString1:str = "0010101010111001"
    ramAddressByte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    ramAddressByte1.fromString(ramAddressString1)
    
    ramAddressString2:str = "0010111010011000"
    ramAddressByte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    ramAddressByte2.fromString(ramAddressString2)

    dataString1="0011110000111100"
    dataByte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    dataByte1.fromString(dataString1)
    theRAM.SET(ramAddressByte1,dataByte1)

    dataString2="1111000011110000"
    dataByte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    dataByte2.fromString(dataString2)
    theRAM.SET(ramAddressByte2,dataByte2)

    ramContentByte1:cpu_simulator.cpuByte = theRAM.GET(ramAddressByte1)
    ramContentString1:str = ramContentByte1.toString()

    ramContentByte2:cpu_simulator.cpuByte = theRAM.GET(ramAddressByte2)
    ramContentString2:str = ramContentByte2.toString()

    assert ramContentString1==dataString1
    assert ramContentString2==dataString2

def test_ram_getAll_allRamReturned():
    theRAM:cpu_simulator.RAM = cpu_simulator.RAM()
    returnList:typing.List[str] = theRAM.allRAM()
    assert len(returnList)==cpu_simulator.RAM._addressCount
    for val in returnList:
        assert len(val)==16

def test_ram_unsignedIntegerToBitString_convertsNumbers():
    assert cpu_simulator.RAM.unsignedIntegerToBitString(0)=="0000000000000000"
    assert cpu_simulator.RAM.unsignedIntegerToBitString(4)=="0000000000000100"
    assert cpu_simulator.RAM.unsignedIntegerToBitString(65535)=="1111111111111111"
    

############### ALU tests ###############

def test_alu_0000000000000000_isZero():
    byteString:str="0000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert cpu_simulator.ALU.isZero(aByte)

def test_alu_1000000000000000_isZero():
    byteString:str="1000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert cpu_simulator.ALU.isZero(aByte)

def test_alu_0000000000000000_isNotNegative():
    byteString:str="0000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert not cpu_simulator.ALU.isNegative(aByte)

def test_alu_1000000000000000_isNegative():
    byteString:str="1000000000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert cpu_simulator.ALU.isNegative(aByte)

def test_alu_0000001000000000_isNotZero():
    byteString:str="0000001000000000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert not cpu_simulator.ALU.isZero(aByte)

def test_alu_1000000000001000_isNotZero():
    byteString:str="1000000000001000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    assert not cpu_simulator.ALU.isZero(aByte)

def test_holdMultipleBytes_bytesStayDifferent():
    byteString1:str="0000000000000100"
    byte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte1.fromString(byteString1)
    byteString2:str="1111111011111111"
    byte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte2.fromString(byteString2)
    assert byte1.toString()==byteString1
    assert byte2.toString()==byteString2

def test_alu_0000000000000000_AND_1111111111111111_is0():
    byteString1:str="0000000000000000"
    byte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte1.fromString(byteString1)
    byteString2:str="1111111111111111"
    byte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte2.fromString(byteString2)
    andResult=cpu_simulator.ALU.AND(byte1,byte2)
    assert andResult.toString()=="0000000000000000"

def test_alu_1000000100001011_AND_1111111011111101_is1000000000001001():
    byteString1:str="1000000100001011"
    byte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte1.fromString(byteString1)
    byteString2:str="1111111011111101"
    byte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte2.fromString(byteString2)
    andResult=cpu_simulator.ALU.AND(byte1,byte2)
    assert andResult.toString()=="1000000000001001"

def test_alu_0000000000000000_ADD_0111111111111111_is0111111111111111():
    byteString1:str="0000000000000000"
    byte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte1.fromString(byteString1)
    byteString2:str="0111111111111111"
    byte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte2.fromString(byteString2)
    addResult=cpu_simulator.ALU.ADD(byte1,byte2)
    assert addResult.toString()=="0111111111111111"

def test_alu_0000000000000010_ADD_0111111111111111_is1000000000000001():
    byteString1:str="0000000000000010"
    byte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte1.fromString(byteString1)
    byteString2:str="0111111111111111"
    byte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte2.fromString(byteString2)
    addResult=cpu_simulator.ALU.ADD(byte1,byte2)
    assert addResult.toString()=="1000000000000001"

def test_alu_1000000000001000_negation_is0111111111110111():
    byteString:str="1000000000001000"
    aByte:cpu_simulator.cpuByte = cpu_simulator.cpuByte()
    aByte.fromString(byteString)
    negByte:cpu_simulator.cpuByte = cpu_simulator.ALU.negation(aByte)
    assert negByte.toString()=="0111111111110111"

def test_alu_canReturnOne():
    byteString1:str="0000000000000010"
    byte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte1.fromString(byteString1)
    byteString2:str="0111111111111111"
    byte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte2.fromString(byteString2)
    result:tuple[cpu_simulator.cpuByte,bool,bool] = cpu_simulator.ALU.evaluate(byte1,byte2,True,True,True,True,True,True)
    outByte:cpu_simulator.cpuByte=result[0]
    assert outByte.asSignedInteger()==1

def test_alu_1000000000000001_minus_0000000000000010_is0111111111111111():
    byteString1:str="1000000000000001"
    byte1:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte1.fromString(byteString1)
    byteString2:str="0000000000000010"
    byte2:cpu_simulator.cpuByte=cpu_simulator.cpuByte()
    byte2.fromString(byteString2)
    result:tuple[cpu_simulator.cpuByte,bool,bool] = cpu_simulator.ALU.evaluate(byte1,byte2,False,True,False,False,True,True)
    outByte:cpu_simulator.cpuByte=result[0]
    assert outByte.toString()=="0111111111111111"


############### machineLanguage tests ###############

def test_machineLanguage_create_noError():
    someData:str=""
    def setSomeData(s:str):
        someData=s

    mlCommand:cpu_simulator.machineLanguageCommand=cpu_simulator.machineLanguageCommand()
    mlCommand.reMatch=".{5}([01]{8})010"
    mlCommand.description="Does a thing with the middle 8 bits."
    mlCommand.action = lambda aSequence : setSomeData(aSequence[0])

    assert True # If we get this far, then there was no error

def test_machineLanguage_match_ignoresNonMatches():
    class tempContainer():
        def __init__(self):
            self.someData:str=""
        def setSomeData(self,s:str):
            self.someData=s
    aContainer = tempContainer()

    mlCommand:cpu_simulator.machineLanguageCommand=cpu_simulator.machineLanguageCommand()
    mlCommand.reMatch=".{5}([01]{8})010"
    mlCommand.description="Does a thing with the middle 8 bits."
    mlCommand.action = lambda aSequence : aContainer.setSomeData(aSequence[0])

    mlBinaryString:str="0000010100000011"
    parsedCommandParams:typing.Sequence[str]=mlCommand.tryStringMatchesCommand(mlBinaryString)
    assert parsedCommandParams == None # check that we got something back

def test_machineLanguage_Invoke_parsedAndFiredCorrectly():
    class tempContainer():
        def __init__(self):
            self.someData:str=""
        def setSomeData(self,s:str):
            self.someData=s
    aContainer = tempContainer()

    mlCommand:cpu_simulator.machineLanguageCommand=cpu_simulator.machineLanguageCommand()
    mlCommand.reMatch=".{5}([01]{8})010"
    mlCommand.description="Does a thing with the middle 8 bits."
    mlCommand.action = lambda aSequence : aContainer.setSomeData(aSequence[0])

    mlBinaryString:str="0000010100000010"
    parsedCommandParams:typing.Sequence[str]=mlCommand.tryStringMatchesCommand(mlBinaryString)
    assert parsedCommandParams != None # check that we got something back

    assert aContainer.someData==""
    mlCommand.action(parsedCommandParams) # carry out the machine language command action
    assert aContainer.someData=="10100000"

def test_machineLanguage_multipleCommands_parsedAndFiredCorrectly():
    class tempContainer():
        def __init__(self):
            self.someData:str=""
        def setSomeData(self,s:str):
            self.someData=s
    aContainer = tempContainer()

    # this is the command that we don't want to accidentally run
    mlCommand1:cpu_simulator.machineLanguageCommand=cpu_simulator.machineLanguageCommand()
    mlCommand1.reMatch="([01]{8}).{5}011"
    mlCommand1.description="Stores the first 8 bits into aContainer."
    mlCommand1.action = lambda aSequence : aContainer.setSomeData(aSequence[0])

    # The command we want to run
    mlCommand2:cpu_simulator.machineLanguageCommand=cpu_simulator.machineLanguageCommand()
    mlCommand2.reMatch=".{5}([01]{8})010"
    mlCommand2.description="Stores the middle 8 bits into aContainer."
    mlCommand2.action = lambda aSequence : aContainer.setSomeData(aSequence[0])

    mlBinaryString:str="0000010100000010" # match to mlCommand2
    parsedCommandParams:typing.Sequence[str]=mlCommand2.tryStringMatchesCommand(mlBinaryString)
    assert parsedCommandParams != None # check that we got something back

    assert aContainer.someData=="" # make sure that aContainer isn't already set
    mlCommand2.action(parsedCommandParams) # carry out the machine language command action
    assert aContainer.someData=="10100000" # make sure that the command action set aContainer


############### CPU tests ###############

def test_cpu_initialize_noErrors():
    theCpu:cpu_simulator.CPU = cpu_simulator.CPU()
    theCpu.theClock=2
    theCpu.tick() # puts the clock at 0 and performs the correct 0-counter actions.
    assert True # if we get here, then initialization occurred without error.

def test_cpu_tick_R0updated():
    theCpu:cpu_simulator.CPU = cpu_simulator.CPU()
    theCpu.theClock=0
    assert theCpu.register0.asUnsignedInteger()==0
    theCpu.tick()
    assert theCpu.theClock==1
    assert theCpu.register0.asUnsignedInteger()==1
    theCpu.tick()
    assert theCpu.theClock==2
    assert theCpu.register0.asUnsignedInteger()==1
    theCpu.tick()
    assert theCpu.theClock==0
    assert theCpu.register0.asUnsignedInteger()==1
    theCpu.tick()
    assert theCpu.theClock==1
    assert theCpu.register0.asUnsignedInteger()==2
    theCpu.tick()
    assert theCpu.theClock==2
    assert theCpu.register0.asUnsignedInteger()==2
    theCpu.tick()
    assert theCpu.theClock==0
    assert theCpu.register0.asUnsignedInteger()==2
