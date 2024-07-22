import os 
import subprocess
from tkinter import * 
from tkinter import ttk 

#subprocess.run(["arduino-cli"])

def getValues():
    values = []
    nDPI = numberOfDPIs.get()
    nDPI1 = ent1.get()
    nDPI2 = ent2.get()
    nDPI3 = ent3.get()
    nDPI4 = ent4.get()
    nDPI5 = ent5.get()

    values.append([nDPI,nDPI1,nDPI2,nDPI3,nDPI4,nDPI5])
    print(values)
    return values


def checkValues(*args):
    dpi1 = ent1.get()
    dpi2 = ent2.get()
    dpi3 = ent3.get()
    dpi4 = ent4.get()
    dpi5 = ent5.get()
    nDPI = numberOfDPIs.get()
    
    saveSettings.config(state=DISABLED)

    if nDPI == 5 and dpi1 != "" and dpi2 != "" and dpi3 != "" and dpi4 != "" and dpi5 != "":
        saveSettings.config(state="normal")  
    elif nDPI == 4 and dpi1 != "" and dpi2 != "" and dpi3 != "" and dpi4 != "":
        saveSettings.config(state="normal")
    elif nDPI == 3 and dpi1 != "" and dpi2 != "" and dpi3 != "":
        saveSettings.config(state="normal")
    elif nDPI == 2 and dpi1 != "" and dpi2 != "":
        saveSettings.config(state="normal")
    elif nDPI == 1 and dpi1 != "":
        saveSettings.config(state="normal")
    else:
        saveSettings.config(state=DISABLED)  


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

root = Tk()
style = ttk.Style()

style.map("whiteBG.TCombobox", fieldbackground=[("readonly", "white")])

root.title("Settings")
root.minsize(500, 600)
#root.maxsize(500, 400)
root.geometry("500x600+700+200")

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

#variables for comboboxes
n1 = IntVar()
n2 = IntVar()
n3 = IntVar()
n4 = IntVar()
n5 = IntVar()

#variable for numberofdpis
numberOfDPIs = IntVar()
numberOfDPIs.set("Bitte Auswählen")

#dropdown label + menu
dropDownLabel = Label(root, text="Wie viele DPI Einstellungen?").pack(pady=5)
dropDown = OptionMenu(root, numberOfDPIs, *DPIamountOptions, command=addDPI).pack(pady=5)

#comboboxes with labels
lab1 = Label(root, text="DPI 1:")
lab1.pack()
ent1 = ttk.Combobox(root, width=7, textvariable=n1, state=DISABLED)
ent1["values"] = chkboxvalues
ent1.set("")
ent1.pack()

lab2 = Label(root, text="DPI 2:")
lab2.pack()
ent2 = ttk.Combobox(root, width=7, textvariable=n2, state=DISABLED)
ent2["values"] = chkboxvalues
ent2.set("")
ent2.pack()

lab3 = Label(root, text="DPI 3:")
lab3.pack()
ent3 = ttk.Combobox(root, width=7, textvariable=n3, state=DISABLED)
ent3["values"] = chkboxvalues
ent3.set("")
ent3.pack()

lab4 = Label(root, text="DPI 4:")
lab4.pack()
ent4 = ttk.Combobox(root, width=7, textvariable=n4, state=DISABLED)
ent4["values"] = chkboxvalues
ent4.set("")
ent4.pack()

lab5 = Label(root, text="DPI 5:")
lab5.pack()
ent5 = ttk.Combobox(root, width=7, textvariable=n5, state=DISABLED)
ent5["values"] = chkboxvalues
ent5.set("")
ent5.pack()

#check for changed 
n1.trace_add("write", checkValues)
n2.trace_add("write", checkValues)
n3.trace_add("write", checkValues)
n4.trace_add("write", checkValues)
n5.trace_add("write", checkValues)
numberOfDPIs.trace_add("write", checkValues)

saveSettings = ttk.Button(root, text="Einstellungen speichern", command=getValues, state=DISABLED)
saveSettings.pack(pady=5)
exitWindow = ttk.Button(root, text="Schließen", command=root.destroy)
exitWindow.pack(pady=5)


root.mainloop()