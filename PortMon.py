from tkinter import *
from tkinterdnd2 import *
from tkinter import messagebox
from tkinter import filedialog

import ctypes
import serial.tools.list_ports


#     __________________________
#    /                          |
#   /    RC20xx  FFS tools      |
#  /      Derek Woodroffe       |
# |  O     Extreme Kits         |
# |   Kits at extkits.uk/RC2040 |
# |            2022             |
# |_____________________________|
#   | | | | | | | | | | | | | |  

# https://github.com/ExtremeElectronics/RC20XX-file-transfer-programs

root=TkinterDnD.Tk()
root.geometry("600x200")
root.title('COMM Port Monitor')
root.resizable(1, 1)


def ListCommPorts(withdesc=False):
    cp=[]
    ports = serial.tools.list_ports.comports()
    for p in ports:
        # print(p.device)
        if withdesc: 
            cp.append(p.device+" | "+ p.description)
        else:
            cp.append(p.device)
    return cp

def filllist():
    global oldsp
    sp = ListCommPorts(True)
    list1.delete(0, END)
    for i, s in enumerate(sp):
        list1.insert(i, s)
        if not s in oldsp:
            list1.itemconfig("end", bg="red")
        else:
            list1.itemconfig("end", bg="black")
        
    root.after(2000, filllist)
    oldsp=sp

oldsp=ListCommPorts(True)

list1 = Listbox(root)
list1.configure(background="black", foreground="green", selectforeground='Black', selectbackground='Green',
                activestyle='none', font='Courier 12', relief="solid", borderwidth="0", highlightcolor="black"
                ,highlightbackground="black")
list1.pack(anchor="nw", side=LEFT, expand=True, fill=BOTH)
filllist()


# run the main program
root.mainloop()  
