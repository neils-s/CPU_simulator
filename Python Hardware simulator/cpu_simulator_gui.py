import typing
import PySimpleGUI as sg
#from PySimpleGUI.PySimpleGUI import Button, Column, Text, ThisRow # used to draw the cpu simulator GUI
import cpu_simulator as sim # used to simulate hardware

# A GUI front-end for a cpu simulator.
# Based on PySimpleGUI, which is found on the web here:  https://pysimplegui.readthedocs.io/en/latest/
# A quick tutorial is here:  https://realpython.com/pysimplegui-python/#installing-pysimplegui

verbose_window_events:bool = False # True # 

# The data model and controller
theCPU:sim.CPU = sim.CPU()
theCPU.tick() # Make sure we start at tick 0

# This will be a convenient place to put output
terminal_ouput:sg.Multiline = sg.Multiline(autoscroll=True,size=(80,10),write_only=True,key="STDOUT")


############################## CPU Register ######################################

# Text fields and "set" buttons for the CPU registers
clockTickDisplay=sg.Text(theCPU.theClock)
register0_display = sg.In(size=(20,1),key="REG0",enable_events=True)
register1_display = sg.In(size=(20,1),key="REG1",enable_events=True)
register2_display = sg.In(size=(20,1),key="REG2",enable_events=True)
register3_display = sg.In(size=(20,1),key="REG3",enable_events=True)
register4_display = sg.In(size=(20,1),key="REG4",enable_events=True)
register5_display = sg.In(size=(20,1),key="REG5",enable_events=True)
register6_display = sg.In(size=(20,1),key="REG6",enable_events=True)
register7_display = sg.In(size=(20,1),key="REG7",enable_events=True)
setRegister0_Button = sg.Button("Set",key="R0_OK")
setRegister1_Button = sg.Button("Set",key="R1_OK")
setRegister2_Button = sg.Button("Set",key="R2_OK")
setRegister3_Button = sg.Button("Set",key="R3_OK")
setRegister4_Button = sg.Button("Set",key="R4_OK")
setRegister5_Button = sg.Button("Set",key="R5_OK")
setRegister6_Button = sg.Button("Set",key="R6_OK")
setRegister7_Button = sg.Button("Set",key="R7_OK")

# Functions that set the content of the register fields
def update_reg0_display() -> None:
    register0_display.update(theCPU.register0.toString())
    update_register0_appearance()

def update_reg1_display() -> None:
    register1_display.update(theCPU.register1.toString())
    update_register1_appearance() 

def update_reg2_display() -> None:
    register2_display.update(theCPU.register2.toString())
    update_register2_appearance() 

def update_reg3_display() -> None:
    register3_display.update(theCPU.register3.toString())
    update_register3_appearance() 

def update_reg4_display() -> None:
    register4_display.update(theCPU.register4.toString())
    update_register4_appearance() 

def update_reg5_display() -> None:
    register5_display.update(theCPU.register5.toString())
    update_register5_appearance() 

def update_reg6_display() -> None:
    register6_display.update(theCPU.register6.toString())
    update_register6_appearance() 

def update_reg7_display() -> None:
    register7_display.update(theCPU.register7.toString())
    update_register7_appearance() 

# Functions that set the color and responsivity of the register input fields
def update_register0_appearance() -> None:
    update_input_field_appearance(register0_display,setRegister0_Button,theCPU.register0.toString)

def update_register1_appearance() -> None:
    update_input_field_appearance(register1_display,setRegister1_Button,theCPU.register1.toString)

def update_register2_appearance() -> None:
    update_input_field_appearance(register2_display,setRegister2_Button,theCPU.register2.toString)

def update_register3_appearance() -> None:
    update_input_field_appearance(register3_display,setRegister3_Button,theCPU.register3.toString)

def update_register4_appearance() -> None:
    update_input_field_appearance(register4_display,setRegister4_Button,theCPU.register4.toString)

def update_register5_appearance() -> None:
    update_input_field_appearance(register5_display,setRegister5_Button,theCPU.register5.toString)

def update_register6_appearance() -> None:
    update_input_field_appearance(register6_display,setRegister6_Button,theCPU.register6.toString)

def update_register7_appearance() -> None:
    update_input_field_appearance(register7_display,setRegister7_Button,theCPU.register7.toString)


############################## RAM ######################################

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
    update_input_field_appearance(ram_update_box,ram_update_ok_button,ram_retriever)

def mark_ram_dirty(ram_is_dirty:list[bool])->None:
    ram_is_dirty.pop()
    ram_is_dirty.append(True)
    if verbose_window_events == True:
        print("\nRAM display is dirty: ",ram_is_dirty)

def update_ram_table(ram_is_dirty:list[bool])->None:
    if verbose_window_events == True:
        print("\nRAM display is dirty: ",ram_is_dirty)
    local_ram_is_dirty:bool = ram_is_dirty.pop()
    if local_ram_is_dirty:
        ram_states_display_table.update(values=theCPU.theRAM.ramTable())
    ram_is_dirty.append(False)


#################################### Utility Functions ######################################

def update_input_field_appearance(byteField:sg.In,theButton:sg.Button,dataBinding:callable=None) -> None:
    """If the given byte field doesn't have a properly formatted byte string, then deactivate the button and turn the field red.
    If the optional data binding function is given, then the button will be disabled if the field value matches the data returned by the dataBinding."""
    val:str = byteField.get() # Intentionally don't handle the case when byteField isn't passed in

    # Check if the value in the bytefield is valid
    val_is_invalid:bool=False
    if sim.cpuByte.isValidBinaryString(val) != True:
        val_is_invalid=True
    
    # If possible, we check if the value has actually changed
    val_is_old:bool = False
    if dataBinding!=None:
        storedVal=dataBinding()
        val_is_old=(val==storedVal)

    # Choose the correct color for the field and button based on whether it should be disabled
    color:str="green"
    if val_is_invalid==True:
        color="red"
    
    # Recolor and enable/disable the button and data field
    byteField.update(background_color=color)
    if theButton != None:
        theButton.update(disabled=(val_is_old or val_is_invalid),button_color=color)

def update_full_display() -> None:
    """Updates the display of all of the elements in the window."""
    clockTickDisplay.update(str(theCPU.theClock))
    update_reg0_display()
    update_reg1_display()
    update_reg2_display()
    update_reg3_display()
    update_reg4_display()
    update_reg5_display()
    update_reg6_display()
    update_reg7_display()
    update_ram_modifier()
    toggle_ram_modifier()

#################################### Display and Layout ######################################

registers_column = [
    [sg.Text("Clock Counter: "),clockTickDisplay],
    [sg.HorizontalSeparator()],
    [
        sg.Text("Registers")
    ],
    [
        sg.Text("Register0 (000): ",tooltip=theCPU.register0_description),
        register0_display,
        setRegister0_Button
    ],
    [
        sg.Text("Register1 (001): ",tooltip=theCPU.register1_description),
        register1_display,
        setRegister1_Button
    ],
    [
        sg.Text("Register2 (010): ",tooltip=theCPU.register2_description),
        register2_display,
        setRegister2_Button
    ],
    [
        sg.Text("Register3 (011): ",tooltip=theCPU.register3_description),
        register3_display,
        setRegister3_Button
    ],
    [
        sg.Text("Register4 (100): ",tooltip=theCPU.register4_description),
        register4_display,
        setRegister4_Button
    ],
    [
        sg.Text("Register5 (101): ",tooltip=theCPU.register5_description),
        register5_display,
        setRegister5_Button
    ],
    [
        sg.Text("Register6 (110): ",tooltip=theCPU.register6_description),
        register6_display,
        setRegister6_Button
    ],
    [
        sg.Text("Register7 (111): ",tooltip=theCPU.register7_description),
        register7_display,
        setRegister7_Button
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

def reactToRAM(ram_is_dirty:list[bool],addressAsInt:int,oldValue:str,newValue:str)->None:
    addressAsByteString:str=sim.cpuByte.unsignedIntegerToBitString(addressAsInt)
    print("\nThe RAM at location ",addressAsByteString," (",str(addressAsInt),") was changed")
    print("Old value: ",oldValue)
    print("New value: ",newValue)
    if oldValue!=newValue:
        mark_ram_dirty(ram_is_dirty)


########################### Window Creation and Event Handling #########################

# Create the Window
window = sg.Window("CPU Simulator", layout,finalize=True)
terminal_ouput.reroute_stdout_to_here() # we dump stdout here so print commands from the CPU simulator show up nicely.
ram_is_dirty:list[bool] = [True]

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
theCPU.theRAM.onChangeEvent.setReaction(window,lambda a,b,c: reactToRAM(ram_is_dirty,a,b,c))

update_ram_table(ram_is_dirty)
update_full_display()

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
        update_ram_table(ram_is_dirty)
        update_ram_modifier()
        toggle_ram_modifier()
    if windowEvent == "REG0":
        update_register0_appearance()
    if windowEvent == "R0_OK":
        theCPU.register0.fromString(register0_display.get())
        update_reg0_display()
    if windowEvent == "REG1":
        update_register1_appearance()
    if windowEvent == "R1_OK":
        theCPU.register1.fromString(register1_display.get())
        update_reg1_display()
    if windowEvent == "REG2":
        update_register2_appearance()
    if windowEvent == "R2_OK":
        theCPU.register2.fromString(register2_display.get())
        update_reg2_display()
    if windowEvent == "REG3":
        update_register3_appearance()
    if windowEvent == "R3_OK":
        theCPU.register3.fromString(register3_display.get())
        update_reg3_display()
    if windowEvent == "REG4":
        update_register4_appearance()
    if windowEvent == "R4_OK":
        theCPU.register4.fromString(register4_display.get())
        update_reg4_display()
    if windowEvent == "REG5":
        update_register5_appearance()
    if windowEvent == "R5_OK":
        theCPU.register5.fromString(register5_display.get())
        update_reg5_display()
    if windowEvent == "REG6":
        update_register6_appearance()
    if windowEvent == "R6_OK":
        theCPU.register6.fromString(register6_display.get())
        update_reg6_display()
    if windowEvent == "REG7":
        update_register7_appearance()
    if windowEvent == "R7_OK":
        theCPU.register7.fromString(register7_display.get())
        update_reg7_display()
    if windowEvent == "TICK":
        theCPU.tick()
        update_full_display()
        update_ram_table(ram_is_dirty)

window.close()
