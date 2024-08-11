import os 
import subprocess
from tkinter import * 
from tkinter import ttk 
from tkinter import colorchooser

#subprocess.run(["arduino-cli"])

def getValues():
    values = []
    nDPI = numberOfDPIs.get()
    nDPI1 = ent1.get()
    nDPI2 = ent2.get()
    nDPI3 = ent3.get()
    nDPI4 = ent4.get()
    nDPI5 = ent5.get()
    rgb_mode = modeRGBbox.get()
    rgb_color = colorRGB
    brightness = brightnessValue.get()
    
    red = 1
    green = 1
    blue = 1

    values = [nDPI,nDPI1,nDPI2,nDPI3,nDPI4,nDPI5,rgb_mode,red,green,blue,brightness]


    #f = open("3360_Mouse_pico.ino", "r")

    if values[6] == 'Off':
        values[7] = 0
        values[8] = 0
        values[9] = 0
    else:
        values[7] = rgb_color[0]
        values[8] = rgb_color[1]
        values[9] = rgb_color[2]
    
    print(values)

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


    if mode == 'Off':
        dummyBG = lab1
        colorFrame.config(bg=dummyBG['bg'])
        brightnessValue.config(from_=0)
        brightnessValue.set(0)
        brightnessValue.config(state=DISABLED)
    else: 
        brightnessValue.config(state="normal", from_=30)
        colorFrame.config(bg=('#%02x%02x%02x' % colorRGB))
        if scale != 0:
            brightnessValue.set(scale)
        else:
            brightnessValue.set(200)

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

root = Tk()
style = ttk.Style()

colorRGB = ()

style.map("whiteBG.TCombobox", fieldbackground=[("readonly", "white")])

root.title("Settings")
root.minsize(500, 600)
#root.maxsize(500, 400)
root.geometry("500x800+700+100")

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
dropDownLabel = Label(root, text="Wie viele DPI Einstellungen?").pack(pady=5)
dropDown = OptionMenu(root, numberOfDPIs, *DPIamountOptions, command=addDPI).pack(pady=5)

#comboboxes with labels
lab1 = Label(root, text="DPI 1:")
lab1.pack(pady=5)
ent1 = ttk.Combobox(root, width=7, textvariable=n1, state="readonly", style="whiteBG.TCombobox")
ent1["values"] = chkboxvalues
ent1.set("")
ent1.pack(pady=5)

lab2 = Label(root, text="DPI 2:")
lab2.pack(pady=5)
ent2 = ttk.Combobox(root, width=7, textvariable=n2, state=DISABLED)
ent2["values"] = chkboxvalues
ent2.set("")
ent2.pack(pady=5)

lab3 = Label(root, text="DPI 3:")
lab3.pack(pady=5)
ent3 = ttk.Combobox(root, width=7, textvariable=n3, state=DISABLED)
ent3["values"] = chkboxvalues
ent3.set("")
ent3.pack(pady=5)

lab4 = Label(root, text="DPI 4:")
lab4.pack(pady=5)
ent4 = ttk.Combobox(root, width=7, textvariable=n4, state=DISABLED)
ent4["values"] = chkboxvalues
ent4.set("")
ent4.pack(pady=5)

lab5 = Label(root, text="DPI 5:")
lab5.pack(pady=5)
ent5 = ttk.Combobox(root, width=7, textvariable=n5, state=DISABLED)
ent5["values"] = chkboxvalues
ent5.set("")
ent5.pack(pady=5)

#check for changed DPI
n1.trace_add("write", checkValues)
n2.trace_add("write", checkValues)
n3.trace_add("write", checkValues)
n4.trace_add("write", checkValues)
n5.trace_add("write", checkValues)
numberOfDPIs.trace_add("write", checkValues)

#choose RGB mode
mode = StringVar()
modeRGBlabel = Label(root, text="RBG:")
modeRGBlabel.pack(pady=5)
modeRGBbox = ttk.Combobox(root, width=9, textvariable=mode, state="readonly", style="whiteBG.TCombobox")
modeRGBbox["values"] = modeRGB
modeRGBbox.set("Static")
modeRGBbox.pack(pady=5)

#check for changed RGB mode
mode.trace_add("write", checkModeRGB)

#RGB colorwheel
colorLabel = Label(root, text="RGB Farbe:")
colorLabel.pack(pady=5)
colorFrame = Frame(root, highlightbackground="black", highlightthickness=2, width=50, height=20)
colorFrame.pack(pady=5)
colorwheel = Button(root, text="Farbe auswählen", command=selectColor)
colorwheel.pack(pady=5)

#brightness
brightnessLabel = Label(root, text="Helligkeit:")
brightnessLabel.pack(pady=5)
brightnessValue = Scale(root, from_=30, to=255, length=255, orient=HORIZONTAL)
brightnessValue.set(200)
brightnessValue.pack()

#save etc
saveSettings = Button(root, text="Einstellungen speichern", command=getValues, state=DISABLED)
saveSettings.pack(pady=5)
exitWindow = Button(root, text="Schließen", command=root.destroy)
exitWindow.pack(pady=5)


root.mainloop()