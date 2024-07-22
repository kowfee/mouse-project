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


def addDPI(*args):
    print(f"DPi Anzahl {numberOfDPIs.get()}")
    n = numberOfDPIs.get()

    if n == 1:
        ent1.config(state="normal")
        ent2.delete(0, END)
        ent2.insert(0, "")
        ent2.config(state="disabled")
        ent3.delete(0, END)
        ent3.insert(0, "")
        ent3.config(state="disabled")
        ent4.delete(0, END)
        ent4.insert(0, "")
        ent4.config(state="disabled")
        ent5.delete(0, END)
        ent5.insert(0, "")
        ent5.config(state="disabled")
    elif n == 2: 
        ent1.config(state="normal")
        ent2.config(state="normal")
        ent3.delete(0, END)
        ent3.insert(0, "")
        ent3.config(state="disabled")
        ent4.delete(0, END)
        ent4.insert(0, "")
        ent4.config(state="disabled")
        ent5.delete(0, END)
        ent5.insert(0, "")
        ent5.config(state="disabled")
    elif n == 3:
        ent1.config(state="normal")
        ent2.config(state="normal")
        ent3.config(state="normal")
        ent4.delete(0, END)
        ent4.insert(0, "")
        ent4.config(state="disabled")
        ent5.delete(0, END)
        ent5.insert(0, "")
        ent5.config(state="disabled")
    elif n == 4:
        ent1.config(state="normal")
        ent2.config(state="normal")
        ent3.config(state="normal")
        ent4.config(state="normal")
        ent5.delete(0, END)
        ent5.insert(0, "")
        ent5.config(state="disabled")
    elif n == 5: 
        ent1.config(state="normal")
        ent2.config(state="normal")
        ent3.config(state="normal")
        ent4.config(state="normal")
        ent5.config(state="normal")
    else:
        ent1.delete(0, END)
        ent1.insert(0, "")
        ent1.config(state="disabled")
        ent2.delete(0, END)
        ent2.insert(0, "")
        ent2.config(state="disabled")
        ent3.delete(0, END)
        ent3.insert(0, "")
        ent3.config(state="disabled")
        ent4.delete(0, END)
        ent4.insert(0, "")
        ent4.config(state="disabled")
        ent5.delete(0, END)
        ent5.insert(0, "")
        ent5.config(state="disabled")


    # number = 0
    # for x in range(0, numberOfDPIs.get()):
    #     number += 1
    #     numberString = str(number)
    #     lab = Label(root, text="DPI " + numberString + " :")
    #     lab.pack()
    #     ent = Entry(root,)
    #     ent.pack()


root = Tk()

root.title("Test")
root.minsize(300, 200)
#root.maxsize(500, 400)
root.geometry("500x600+700+200")

DPIamountOptions = [
    1,
    2,
    3,
    4,
    5
]

numberOfDPIs = IntVar()
numberOfDPIs.set("Bitte Auswählen")


dropDownLabel = Label(root, text="Wie viele DPI Einstellungen?").pack(pady=5)
dropDown = OptionMenu(root, numberOfDPIs, *DPIamountOptions, command=addDPI).pack(pady=5)


lab1 = Label(root, text="DPI 1:")
lab1.pack()
ent1 = Entry(root, state="disabled")
ent1.pack()

lab2 = Label(root, text="DPI 2:")
lab2.pack()
ent2 = Entry(root, state="disabled")
ent2.pack()

lab3 = Label(root, text="DPI 3:")
lab3.pack()
ent3 = Entry(root, state="disabled")
ent3.pack()

lab4 = Label(root, text="DPI 4:")
lab4.pack()
ent4 = Entry(root, state="disabled")
ent4.pack()

lab5 = Label(root, text="DPI 5:")
lab5.pack()
ent5 = Entry(root, state="disabled")
ent5.pack()


saveSettings = Button(root, text="Einstellungen speichern", command=getValues).pack(pady=5)
exitWindow = Button(root, text="Schließen", command=root.destroy).pack(pady=5)


root.mainloop()


