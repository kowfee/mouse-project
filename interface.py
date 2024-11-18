import subprocess
import threading
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from sys import platform
import serial.tools.list_ports

def getValues():
    with open("./mouse-diy.ino", "r") as ino_read:
        inoLines = ino_read.readlines()

    nDPI = numberOfDPIs.get()
    s1 = ent1.get()
    s2 = ent2.get()
    s3 = ent3.get()
    s4 = ent4.get()
    s5 = ent5.get()

    if s1 != '' :
        i1 = int(s1)
        nDPI1 = int((i1/100)-1)
    if s2 != '' :
        i2 = int(s2)
        nDPI2 = int((i2/100)-1)
    if s3 != '' :
        i3 = int(s3)
        nDPI3 = int((i3/100)-1)
    if s4 != '' :
        i4 = int(s4)
        nDPI4 = int((i4/100)-1)
    if s5 != '' :
        i5 = int(s5)
        nDPI5 = int((i5/100)-1)

    with open("./mouse-diy.ino", "w") as ino_write:
        rgb_mode = modeRGBbox.get()
        rgb_color = colorRGB
        brightness = brightnessValue.get()

        red: int
        green: int
        blue: int

        if rgb_mode != 'Static':
            red = 0
            green = 0
            blue = 0
        else:
            red = rgb_color[0]
            green = rgb_color[1]
            blue = rgb_color[2]

        inoLines[184] = f"#define GLOBAL_BRIGHTNESS {brightness}\n"

        if nDPI == 1:
            inoLines[180] = f"int dpi_values[] = {{{nDPI1}}};\n"
        elif nDPI == 2:
            inoLines[180] = f"int dpi_values[] = {{{nDPI1}, {nDPI2}}};\n"
        elif nDPI == 3:
            inoLines[180] = f"int dpi_values[] = {{{nDPI1}, {nDPI2}, {nDPI3}}};\n"
        elif nDPI == 4:
            inoLines[180] = f"int dpi_values[] = {{{nDPI1}, {nDPI2}, {nDPI3}, {nDPI4}}};\n"
        elif nDPI == 5:
            inoLines[180] = f"int dpi_values[] = {{{nDPI1}, {nDPI2}, {nDPI3}, {nDPI4}, {nDPI5}}};\n"

        if rgb_mode == "Off":
            inoLines[188] = f"int rgb_selector = 0;\n"
        elif rgb_mode == "Static":
            inoLines[188] = f"int rgb_selector = 1;\n"
            inoLines[364] = f"\tstrip.setPixelColor(i, {red}, {green}, {blue});\n"
        elif rgb_mode == "Rainbow":
            inoLines[188] = f"int rgb_selector = 2;\n"
        elif rgb_mode == "Police":
            inoLines[188] = f"int rgb_selector = 3;\n"
        elif rgb_mode == "Breathing":
            inoLines[188] = f"int rgb_selector = 4;\n"

        ino_write.writelines(inoLines)

    uploadToBoard()

def uploadToBoard():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "2E8A:00C0" in p.hwid:
            arduino_port = p.device
    if checkBoardConnection():
        if platform == "win32" or platform == "win64":
            subprocess.run(["arduino-cli.exe", "compile", "--fqbn", "arduino:mbed_rp2040:pico",  "--port", arduino_port, "--upload", "./mouse-diy.ino"])
        elif platform == "linux" or platform == "linux2":
            subprocess.run(["./bin/arduino-cli", "compile", "--fqbn", "arduino:mbed_rp2040:pico",  "--port", arduino_port, "--upload", "./mouse-diy.ino"])
    else:
        ErrorWindow()

def checkValues(*args):
    dpi1 = ent1.get()
    dpi2 = ent2.get()
    dpi3 = ent3.get()
    dpi4 = ent4.get()
    dpi5 = ent5.get()
    nDPI = numberOfDPIs.get()
    color = colorRGB
    mode = modeRGBbox.get()
    scale = brightnessValue.get()

    saveSettings.config(state=DISABLED)

    rgbValidation = (mode != "Static" and color == ()) or (mode == "Static" and color != ()) or (mode != "Static" and color != ())
    dpiValidation = ((nDPI == 5 and dpi1 != "" and dpi2 != "" and dpi3 != "" and dpi4 != "" and dpi5 != "")
                        or (nDPI == 4 and dpi1 != "" and dpi2 != "" and dpi3 != "" and dpi4 != "")
                            or (nDPI == 3 and dpi1 != "" and dpi2 != "" and dpi3 != "")
                                or (nDPI == 2 and dpi1 != "" and dpi2 != "")
                                    or (nDPI == 1 and dpi1 != "") )

    if dpiValidation and rgbValidation:
        saveSettings.config(state="normal")
    else:
        saveSettings.config(state=DISABLED)

    if mode == 'Off' or mode == 'Breathing':
        brightnessValue.config(from_=0)
        brightnessValue.set(0)
        brightnessValue.config(state=DISABLED)
    else:
        brightnessValue.config(state="normal", from_=10)
        if scale != 0:
            brightnessValue.set(scale)
        else:
            brightnessValue.set(100)

    if mode == "Static" and colorRGB != ():
        colorFrame.config(bg=('#%02x%02x%02x' % (colorRGB)))
    else:
        colorFrame.config(bg=lab1['bg'])

def addDPI(*args):
    n = numberOfDPIs.get()

    if n == 1:
        ent1.config(state="readonly", style= "whiteBG.TCombobox")
        ent2.set("")
        ent2.config(state="disabled", style="TCombobox")
        ent3.set("")
        ent3.config(state="disabled", style="TCombobox")
        ent4.set("")
        ent4.config(state="disabled", style="TCombobox")
        ent5.set("")
        ent5.config(state="disabled", style="TCombobox")
    elif n == 2:
        ent1.config(state="readonly", style= "whiteBG.TCombobox")
        ent2.config(state="readonly", style= "whiteBG.TCombobox")
        ent3.set("")
        ent3.config(state="disabled", style="TCombobox")
        ent4.set("")
        ent4.config(state="disabled", style="TCombobox")
        ent5.set("")
        ent5.config(state="disabled", style="TCombobox")
    elif n == 3:
        ent1.config(state="readonly", style= "whiteBG.TCombobox")
        ent2.config(state="readonly", style= "whiteBG.TCombobox")
        ent3.config(state="readonly", style= "whiteBG.TCombobox")
        ent4.set("")
        ent4.config(state="disabled", style="TCombobox")
        ent5.set("")
        ent5.config(state="disabled", style="TCombobox")
    elif n == 4:
        ent1.config(state="readonly", style= "whiteBG.TCombobox")
        ent2.config(state="readonly", style= "whiteBG.TCombobox")
        ent3.config(state="readonly", style= "whiteBG.TCombobox")
        ent4.config(state="readonly", style= "whiteBG.TCombobox")
        ent5.set("")
        ent5.config(state="disabled", style="TCombobox")
    elif n == 5:
        ent1.config(state="readonly", style= "whiteBG.TCombobox")
        ent2.config(state="readonly", style= "whiteBG.TCombobox")
        ent3.config(state="readonly", style= "whiteBG.TCombobox")
        ent4.config(state="readonly", style= "whiteBG.TCombobox")
        ent5.config(state="readonly", style= "whiteBG.TCombobox")
    else:
        ent1.set("")
        ent1.config(state="disabled", style="TCombobox")
        ent2.set("")
        ent2.config(state="disabled", style="TCombobox")
        ent3.set("")
        ent3.config(state="disabled", style="TCombobox")
        ent4.set("")
        ent4.config(state="disabled", style="TCombobox")
        ent5.set("")
        ent5.config(state="disabled", style="TCombobox")

def selectColor():
    global colorRGB
    color=colorchooser.askcolor(title="Farbe auswählen")
    colorHex = color[1]
    colorRGB = color[0]
    colorFrame.config(background=colorHex)
    checkValues()

def checkModeRGB(*args):
    mode = modeRGBbox.get()

    if mode != "Static":
        colorwheel.config(state=DISABLED)
    else:
        colorwheel.config(state="normal")

    checkValues()

def checkBoardConnection():
    if platform == "win32" or platform == "win64":
        board_list = str(subprocess.run(["arduino-cli.exe","board", "list"], capture_output=True))
    elif platform == "linux" or platform == "linux2":
        board_list = str(subprocess.run(["bin/arduino-cli","board", "list"], capture_output=True))

    if "arduino:mbed_rp2040:pico" in board_list:
        return True
    else:
        return False

root = Tk()
style = ttk.Style()

colorRGB = ()

style.map("whiteBG.TCombobox", fieldbackground=[("readonly", "white")])

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def ErrorWindow():
    errorWindow = Toplevel(root)
    errorWindow.title("Error")
    errorWindow.geometry("300x90")
    errorWindow.minsize(300, 90)
    errorWindow.maxsize(300, 90)
    Label(errorWindow, text="\nThere seems to be no device connected.\nPlease connect the device and try again!").pack()
    Button(errorWindow, text="OK", command=errorWindow.destroy).pack()
    center_window(errorWindow)

root.title("Settings")
root.minsize(500, 300)
root.maxsize(500, 300)
root.geometry("500x300")
center_window(root)

#dropdown menu option
DPIamountOptions = [
    1,
    2,
    3,
    4,
    5
]

#combobox menu options
chkboxvalues = [
    100,
    200,
    300,
    400,
    500,
    600,
    700,
    800,
    900,
    1000,
    1100,
    1200,
    1300,
    1400,
    1500,
    1600,
    1700,
    1800,
    1900,
    2000,
    2100,
    2200,
    2300,
    2400,
    2500,
    2600,
    2700,
    2800,
    2900,
    3000,
    3100,
    3200,
    3300,
    3400,
    3500,
    3600,
    3700,
    3800,
    3900,
    4000,
    4100,
    4200,
    4300,
    4400,
    4500,
    4600,
    4700,
    4800,
    4900,
    5000,
    5100,
    5200,
    5300,
    5400,
    5500,
    5600,
    5700,
    5800,
    5900,
    6000,
    6100,
    6200,
    6300,
    6400,
    6500,
    6600,
    6700,
    6800,
    6900,
    7000,
    7100,
    7200,
    7300,
    7400,
    7500,
    7600,
    7700,
    7800,
    7900,
    8000,
    8100,
    8200,
    8300,
    8400,
    8500,
    8600,
    8700,
    8800,
    8900,
    9000,
    9100,
    9200,
    9300,
    9400,
    9500,
    9600,
    9700,
    9800,
    9900,
    10000,
    10100,
    10200,
    10300,
    10400,
    10500,
    10600,
    10700,
    10800,
    10900,
    11000,
    11100,
    11200,
    11300,
    11400,
    11500,
    11600,
    11700,
    11800,
    11900,
    12000]

#RGB mode menu options
modeRGB = [
    "Off",
    "Static",
    "Rainbow",
    "Police",
    "Breathing"
]

#variables for comboboxes
n1 = IntVar()
n2 = IntVar()
n3 = IntVar()
n4 = IntVar()
n5 = IntVar()

#variable for numberofdpis
numberOfDPIs = IntVar()
numberOfDPIs.set(1)

#dropdown label + menu
dropDownLabel = Label(root, text="# of DPIs:").grid(row = 0, column = 0, pady=5, padx=5 )
dropDown = OptionMenu(root, numberOfDPIs, *DPIamountOptions, command=addDPI).grid(row = 0, column = 1, pady=5, padx=5 )

#comboboxes with labels
lab1 = Label(root, text="DPI 1:")
lab1.grid(row = 1, column = 0, pady=5, padx=5 )
ent1 = ttk.Combobox(root, width=7, textvariable=n1, state="readonly", style="whiteBG.TCombobox")
ent1["values"] = chkboxvalues
ent1.set("")
ent1.grid(row = 1, column = 1, pady=5, padx=5 )

lab2 = Label(root, text="DPI 2:")
lab2.grid(row = 2, column = 0, pady=5, padx=5 )
ent2 = ttk.Combobox(root, width=7, textvariable=n2, state=DISABLED)
ent2["values"] = chkboxvalues
ent2.set("")
ent2.grid(row = 2, column = 1, pady=5, padx=5 )

lab3 = Label(root, text="DPI 3:")
lab3.grid(row = 3, column = 0, pady=5, padx=5 )
ent3 = ttk.Combobox(root, width=7, textvariable=n3, state=DISABLED)
ent3["values"] = chkboxvalues
ent3.set("")
ent3.grid(row = 3, column = 1, pady=5, padx=5 )

lab4 = Label(root, text="DPI 4:")
lab4.grid(row = 4, column = 0, pady=5, padx=5 )
ent4 = ttk.Combobox(root, width=7, textvariable=n4, state=DISABLED)
ent4["values"] = chkboxvalues
ent4.set("")
ent4.grid(row = 4, column = 1, pady=5, padx=5 )

lab5 = Label(root, text="DPI 5:")
lab5.grid(row = 5, column = 0, pady=5, padx=5 )
ent5 = ttk.Combobox(root, width=7, textvariable=n5, state=DISABLED)
ent5["values"] = chkboxvalues
ent5.set("")
ent5.grid(row = 5, column = 1, pady=5, padx=5 )

#check for changed DPI
n1.trace_add("write", checkValues)
n2.trace_add("write", checkValues)
n3.trace_add("write", checkValues)
n4.trace_add("write", checkValues)
n5.trace_add("write", checkValues)
numberOfDPIs.trace_add("write", checkValues)

#empty space
frame = ttk.Frame(root, width=50, height=300).grid(row = 0, rowspan = 6, column = 2)

#choose RGB mode
mode = StringVar()
modeRGBlabel = Label(root, text="RBG:")
modeRGBlabel.grid(row = 0, column = 3, pady=5, padx=5 )
modeRGBbox = ttk.Combobox(root, width=9, textvariable=mode, state="readonly", style="whiteBG.TCombobox")
modeRGBbox["values"] = modeRGB
modeRGBbox.set("Static")
modeRGBbox.grid(row = 0, column = 4, pady=5, padx=5 )

#check for changed RGB mode
mode.trace_add("write", checkModeRGB)

#RGB colorwheel
colorLabel = Label(root, text="RGB Color:")
colorLabel.grid(row = 1, column = 3, pady=5, padx=5 )
colorFrame = Frame(root, highlightbackground="black", highlightthickness=2, width=80, height=20)
colorFrame.grid(row = 1, column = 4, pady=5, padx=5 )
colorwheel = Button(root, text="Select", command=selectColor)
colorwheel.grid(row = 1, column = 5, pady=5, padx=5 )

#brightness
brightnessLabel = Label(root, text="Brightness:")
brightnessLabel.grid(row = 2, column = 3, pady=5, padx=5 )
brightnessValue = Scale(root, from_=10, to=255, length=80, showvalue=0, orient=HORIZONTAL)
brightnessValue.set(100)
brightnessValue.grid(row = 2, column = 4, pady=5, padx=5 )

#save etc
saveSettings = Button(root, text="Upload", command=getValues, state=DISABLED)
saveSettings.grid(row = 5, column = 4, pady=5, padx=5 )
exitWindow = Button(root, text="Close", command=root.destroy)
exitWindow.grid(row = 5, column = 5, pady=5, padx=5 )

root.mainloop()