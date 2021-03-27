import typing
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Button, Column, Text, ThisRow # used to draw the cpu simulator GUI
import cpu_simulator as sim # used to simulate hardware

# A GUI front-end for a cpu simulator.
# Based on PySimpleGUI, which is found on the web here:  https://pysimplegui.readthedocs.io/en/latest/
# A quick tutorial is here:  https://realpython.com/pysimplegui-python/#installing-pysimplegui

verbose_window_events:bool = True
verbose_cpu_events:bool = True

theCPU:sim.CPU = sim.CPU()
theCPU.tick() # Make sure we start at tick 0

clockTickDisplay=sg.Text(theCPU.theClock)
register0_display = sg.In(size=(20,1),key="REG0",enable_events=True) #,default_text=theCPU.register0.toString()
register1_display = sg.In(size=(20,1),key="REG1",enable_events=True) #,default_text=theCPU.register1.toString()
register2_display = sg.In(size=(20,1),key="REG2",enable_events=True) #,default_text=theCPU.register2.toString()
register3_display = sg.In(size=(20,1),key="REG3",enable_events=True) #,default_text=theCPU.register3.toString()
register4_display = sg.In(size=(20,1),key="REG4",enable_events=True) #,default_text=theCPU.register4.toString()
register5_display = sg.In(size=(20,1),key="REG5",enable_events=True) #,default_text=theCPU.register5.toString()
register6_display = sg.In(size=(20,1),key="REG6",enable_events=True) #,default_text=theCPU.register6.toString()
register7_display = sg.In(size=(20,1),key="REG7",enable_events=True) #,default_text=theCPU.register7.toString()
register0_ok = sg.Button("Set",key="R0_OK")
register1_ok = sg.Button("Set",key="R1_OK")
register2_ok = sg.Button("Set",key="R2_OK")
register3_ok = sg.Button("Set",key="R3_OK")
register4_ok = sg.Button("Set",key="R4_OK")
register5_ok = sg.Button("Set",key="R5_OK")
register6_ok = sg.Button("Set",key="R6_OK")
register7_ok = sg.Button("Set",key="R7_OK")

def toggle_reg0_modifier() -> None:
    toggle_byte_and_button_settable(register0_display,register0_ok,theCPU.register0.toString)

def toggle_reg1_modifier() -> None:
    toggle_byte_and_button_settable(register1_display,register1_ok,theCPU.register1.toString)

def toggle_reg2_modifier() -> None:
    toggle_byte_and_button_settable(register2_display,register2_ok,theCPU.register2.toString)

def toggle_reg3_modifier() -> None:
    toggle_byte_and_button_settable(register3_display,register3_ok,theCPU.register3.toString)

def toggle_reg4_modifier() -> None:
    toggle_byte_and_button_settable(register4_display,register4_ok,theCPU.register4.toString)

def toggle_reg5_modifier() -> None:
    toggle_byte_and_button_settable(register5_display,register5_ok,theCPU.register5.toString)

def toggle_reg6_modifier() -> None:
    toggle_byte_and_button_settable(register6_display,register6_ok,theCPU.register6.toString)

def toggle_reg7_modifier() -> None:
    toggle_byte_and_button_settable(register7_display,register7_ok,theCPU.register7.toString)

def update_reg0_display() -> None:
    register0_display.update(theCPU.register0.toString())
    toggle_reg0_modifier()

def update_reg1_display() -> None:
    register1_display.update(theCPU.register1.toString())
    toggle_reg1_modifier() 

def update_reg2_display() -> None:
    register2_display.update(theCPU.register2.toString())
    toggle_reg2_modifier() 

def update_reg3_display() -> None:
    register3_display.update(theCPU.register3.toString())
    toggle_reg3_modifier() 

def update_reg4_display() -> None:
    register4_display.update(theCPU.register4.toString())
    toggle_reg4_modifier() 

def update_reg5_display() -> None:
    register5_display.update(theCPU.register5.toString())
    toggle_reg5_modifier() 

def update_reg6_display() -> None:
    register6_display.update(theCPU.register6.toString())
    toggle_reg6_modifier() 

def update_reg7_display() -> None:
    register7_display.update(theCPU.register7.toString())
    toggle_reg7_modifier() 

def update_registers_column_display()->None:
    clockTickDisplay.update(str(theCPU.theClock))
    update_reg0_display()
    update_reg1_display()
    update_reg2_display()
    update_reg3_display()
    update_reg4_display()
    update_reg5_display()
    update_reg6_display()
    update_reg7_display()

ram_address_and_values:typing.List[typing.List[str]]=[["address","value"]]
ram_table_headings = ["Binary address      ","Binary value      "]
ram_states_display_table:sg.Table=sg.Table(display_row_numbers=True,values=ram_address_and_values,headings=ram_table_headings,enable_events=True,key="RAM_TABLE",select_mode="browse")

ram_last_user_address:int=None
ram_address_display:sg.Text=sg.Text(size=(22,1)) 
ram_update_box:sg.In=sg.In(size=(18,1),default_text="",key="EDITABLE_RAM_VALUE",enable_events=True)
ram_update_ok_button = sg.Button("Set",key="RAM_OK",enable_events=True)

def update_ram_modifier()->None:
    address:int=ram_last_user_address
    address_display_string:str=""
    value_string:str=""
    value_visible:bool = False
    if address==None:
        address_display_string="Select a row of RAM from the table above..."
        value_string=None
    else:
        value_visible=True
        address_display_string="RAM "+theCPU.theRAM.unsignedIntegerToBitString(address)+": "
        value_string=theCPU.theRAM.getUsingIntegerAddress(address).toString()
    ram_address_display.Size=(len(address_display_string),1)
    ram_address_display.set_size(size=(len(address_display_string),None))
    ram_address_display.update(value=address_display_string)
    ram_update_box.update(value=value_string,visible=value_visible)
    ram_update_ok_button.update(visible=value_visible)

def toggle_ram_modifier()->None:
    """Makes sure that the RAM modifier field is properly colored and the OK button is properly disabled."""
    def ram_retriever() -> str:
        if ram_last_user_address==None:
            return ""
        return theCPU.theRAM.getUsingIntegerAddress(ram_last_user_address).toString()
    toggle_byte_and_button_settable(ram_update_box,ram_update_ok_button,ram_retriever)

def toggle_byte_and_button_settable(byteField:sg.In,theButton:sg.Button,dataBinding:callable=None) -> None:
    """If the given byte field doesn't have a properly formatted byte string, then deactivate the button and turn the field red.
    If the optional data binding function is given, then the button will be disabled if the field value matches the data returned by the dataBinding."""
    val:str = byteField.get()
    disable_button:bool=False
    if dataBinding!=None:
        storedVal=dataBinding()
        disable_button=(val==storedVal)
    if sim.cpuByte.isValidBinaryString(val):
        byteField.update(background_color="green")
        if theButton != None:
            theButton.update(disabled=disable_button,button_color="green")
    else:
        byteField.update(background_color="red")
        if theButton != None:
            theButton.update(disabled=True,button_color="red")

def update_ram_table()->None:
    ram_states_display_table.update(values=theCPU.theRAM.ramTable())

# This will be a convenient place to put output
terminal_ouput:sg.Multiline = sg.Multiline(autoscroll=True,size=(80,10),write_only=True,key="STDOUT") #,reroute_stdout=True

registers_column = [
    [sg.Text("Clock Counter: "),clockTickDisplay],
    [sg.HorizontalSeparator()],
    [
        sg.Text("Registers")
    ],
    [
        sg.Text("Register0 (000): "),
        register0_display,
        register0_ok
    ],
    [
        sg.Text("Register1 (001): "),
        register1_display,
        register1_ok
    ],
    [
        sg.Text("Register2 (010): "),
        register2_display,
        register2_ok
    ],
    [
        sg.Text("Register3 (011): "),
        register3_display,
        register3_ok
    ],
    [
        sg.Text("Register4 (100): "),
        register4_display,
        register4_ok
    ],
    [
        sg.Text("Register5 (101): "),
        register5_display,
        register5_ok
    ],
    [
        sg.Text("Register6 (110): "),
        register6_display,
        register6_ok
    ],
    [
        sg.Text("Register7 (111): "),
        register7_display,
        register7_ok
    ]

]
ram_column = [
    [
        sg.Text("RAM")
    ],
    [
        ram_states_display_table
    ],
    [
        ram_address_display,
        ram_update_box,
        ram_update_ok_button
    ]
]
terminal_section = [
    [sg.Text("CPU Action Log")],
    [terminal_ouput] 
]
layout = [
    [
        sg.Column(registers_column),
        sg.VSeperator(),
        sg.Column(ram_column) #size in pixels ,size=(600,300)
    ],
    [
        sg.Column(terminal_section, element_justification="center",justification="center")
    ],
    [
        sg.Button(button_text="CPU Tick",key="TICK"), sg.Button(key="CLOSE_BUTTON",button_text="Close")
    ]
]

# Create the Window
window = sg.Window("CPU Simulator", layout,finalize=True)
terminal_ouput.reroute_stdout_to_here() # we dump stdout here so print commands from the CPU simulator show up nicely.
update_ram_modifier()
update_registers_column_display()
update_ram_table()
update_ram_modifier()
toggle_ram_modifier()

# Wire up the RAM and CPU events for display
def reactToParseML(mlBinaryString:str,matchedCommand:sim.machineLanguageCommand,parsedCommandParams:typing.Sequence)->None:
    print("\nMachine language directive encountered by the CPU: "+str(mlBinaryString))
    if matchedCommand==None:
        print("Binary string could not be interpreted by the CPU.")
    else:
        print("Binary string matches to the machine language directive:")
        print(matchedCommand.description)
    if (parsedCommandParams!=None) & (len(parsedCommandParams)>0):
        print("The following data was parsed out of the binary: ")
        for i in range(len(parsedCommandParams)):
            print(parsedCommandParams[i])

def reactToALU(conditionalFlags:str,aluDirectives:str,jumpRegisterDirective:str) ->None:
    print("\nThe ALU was invoked with the 6 ALU command bits of "+aluDirectives)
    print("The two jump-condition bits were "+conditionalFlags+", and the jump register to copy to register0 was "+jumpRegisterDirective)

def reactToRegister0(oldValue,newValue)->None:
    print("\nRegister 0 has changed value from "+oldValue+" to "+newValue)
def reactToRegister1(oldValue,newValue)->None:
    print("\nRegister 1 has changed value from "+oldValue+" to "+newValue)
def reactToRegister2(oldValue,newValue)->None:
    print("\nRegister 2 has changed value from "+oldValue+" to "+newValue)
def reactToRegister3(oldValue,newValue)->None:
    print("\nRegister 3 has changed value from "+oldValue+" to "+newValue)
def reactToRegister4(oldValue,newValue)->None:
    print("\nRegister 4 has changed value from "+oldValue+" to "+newValue)
def reactToRegister5(oldValue,newValue)->None:
    print("\nRegister 5 has changed value from "+oldValue+" to "+newValue)
def reactToRegister6(oldValue,newValue)->None:
    print("\nRegister 6 has changed value from "+oldValue+" to "+newValue)
def reactToRegister7(oldValue,newValue)->None:
    print("\nRegister 7 has changed value from "+oldValue+" to "+newValue)

def reactToRAM(addressAsInt:int,oldValue:str,newValue:str)->None:
    addressAsByteString:str=sim.cpuByte.unsignedIntegerToBitString(addressAsInt)
    print("\nThe RAM at location ",addressAsByteString," (",str(addressAsInt),") was changed")
    print("Old value: ",oldValue)
    print("New value: ",newValue)

theCPU.onParseML.setReaction(window,reactToParseML)
theCPU.onAluCommand.setReaction(window,reactToALU)
theCPU.register0.onChangeEvent.setReaction(window,reactToRegister0)
theCPU.register1.onChangeEvent.setReaction(window,reactToRegister1)
theCPU.register2.onChangeEvent.setReaction(window,reactToRegister2)
theCPU.register3.onChangeEvent.setReaction(window,reactToRegister3)
theCPU.register4.onChangeEvent.setReaction(window,reactToRegister4)
theCPU.register5.onChangeEvent.setReaction(window,reactToRegister5)
theCPU.register6.onChangeEvent.setReaction(window,reactToRegister6)
theCPU.register7.onChangeEvent.setReaction(window,reactToRegister7)
theCPU.theRAM.onChangeEvent.setReaction(window,reactToRAM)

# Create an event loop to catch events raised by the window itself
while True:
    windowEvent,values = window.read() # returns any events, and also the state of the entire window along with that event.
    if verbose_window_events == True:
        print("\nWindow event: ",windowEvent,values)
    if windowEvent == "CLOSE_BUTTON" or windowEvent == sg.WIN_CLOSED:
        break # end the program if the user closes the window or clicks the OK button
    if windowEvent == "RAM_TABLE":
        ram_last_user_address=values["RAM_TABLE"][0]
        update_ram_modifier()
        toggle_ram_modifier()
    if windowEvent == "EDITABLE_RAM_VALUE":
        toggle_ram_modifier()
    if windowEvent == "RAM_OK":
        theCPU.theRAM.setUsingUnsignedIntegerAddressAndBitStringValue(ram_last_user_address,ram_update_box.get())
        update_ram_table()
        update_ram_modifier()
        toggle_ram_modifier()
    if windowEvent == "REG0":
        toggle_reg0_modifier()
    if windowEvent == "R0_OK":
        theCPU.register0.fromString(register0_display.get())
        update_reg0_display()
    if windowEvent == "REG1":
        toggle_reg1_modifier()
    if windowEvent == "R1_OK":
        theCPU.register1.fromString(register1_display.get())
        update_reg1_display()
    if windowEvent == "REG2":
        toggle_reg2_modifier()
    if windowEvent == "R2_OK":
        theCPU.register2.fromString(register2_display.get())
        update_reg2_display()
    if windowEvent == "REG3":
        toggle_reg3_modifier()
    if windowEvent == "R3_OK":
        theCPU.register3.fromString(register3_display.get())
        update_reg3_display()
    if windowEvent == "REG4":
        toggle_reg4_modifier()
    if windowEvent == "R4_OK":
        theCPU.register4.fromString(register4_display.get())
        update_reg4_display()
    if windowEvent == "REG5":
        toggle_reg5_modifier()
    if windowEvent == "R5_OK":
        theCPU.register5.fromString(register5_display.get())
        update_reg5_display()
    if windowEvent == "REG6":
        toggle_reg6_modifier()
    if windowEvent == "R6_OK":
        theCPU.register6.fromString(register6_display.get())
        update_reg6_display()
    if windowEvent == "REG7":
        toggle_reg7_modifier()
    if windowEvent == "R7_OK":
        theCPU.register7.fromString(register7_display.get())
        update_reg7_display()
    if windowEvent == "TICK":
        theCPU.tick()
        update_registers_column_display()
        update_ram_table()
        update_ram_modifier()
        toggle_ram_modifier()

window.close()
