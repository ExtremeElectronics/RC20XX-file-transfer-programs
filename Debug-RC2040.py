#pip3 install tkinterdnd2
#pip3 install pyserial

from tkinter import *
from tkinterdnd2 import *
from tkinter import messagebox
from tkinter import filedialog
import os
import ctypes
import pathlib
import RCxxSerial
import base64
import time
import argparse
import serial

serialPortNotSelectedTxt="Select Port"
serialport=serialPortNotSelectedTxt
Speed=115200
StartToken = "&&&-magic-XXX"

crlf='\n';
buffer=""

#     __________________________
#    /                          |
#   /   RC2040 DEBUG tools      |
#  /      Derek Woodroffe       |
# |  O     Extreme Kits         |
# |   Kits at extkits.uk/RC2040 |
# |            2022             |
# |_____________________________|
#   | | | | | | | | | | | | | |  

# https://github.com/ExtremeElectronics/RC20XX-file-transfer-programs

debug=0
RCxxSerial.debug=debug

who=""

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] ",
        description="Debug tool on RC2040"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    
    
    parser.add_argument('-port', help="Com or TTY port with an RC20XX attached")
 
    return parser

#Get Command line
parser = init_argparse()
args = parser.parse_args()

# Increase Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

#create root 
root=TkinterDnD.Tk()

# set a title for our file explorer main window
root.title('RC2040 - DEBUG TOOL')

root.geometry("1024x800")
root.resizable(1, 1)

#root.grid_columnconfigure(0, weight=10)
root.grid_columnconfigure(2, weight=20)

root.grid_rowconfigure(9, weight=3)

drivescrollbar = Scrollbar(root)
dirfilenames=[]
def initterm():
    list2["state"]="normal"
    list2.delete(0, END)
    list2.insert(0,"")
    list2.insert(1,"    ________________________")
    list2.insert(2,"   /                        |")
    list2.insert(3,"  /   RC2040 DEBUG tools    |")
    list2.insert(4," /     Derek Woodroffe      |")
    list2.insert(5,"|  O    Extreme Kits        |")
    list2.insert(6,"| Kits at extkits.uk/RC2040 |")
    list2.insert(7,"|            2022           |")
    list2.insert(8,"|___________________________|")
    list2.insert(9," | | | | | | | | | | | | | | | ")
    list2["state"]="disabled"    



def controls(enable):
    if enable: state="normal"
    else: state="disabled"

    WatchBut["state"]=state
    TraceBut["state"]=state
    DisBut["state"]=state
    DumpBut["state"]=state
    ExitBut["state"]=state
    list2["state"]=state
    
def chooseCommPort(choice):
    global serialport,Status,spdm,ser
    spvar.set(choice)
    serialport = choice
    serialab.configure(state='normal')
    serialab.delete('0', END)
    Stat.configure(state='normal')
    Stat.delete('1.0', END)

    if serialport==serialPortNotSelectedTxt:
        controls(False)
        Stat.insert('end',"Disconnected")
        serialab.insert('end',"Connect to RC20XX on ")
        
    else:
        sp=serialport.split("|")
        serialport=sp[0].strip()
        
        controls(True)
        
        Stat.insert('end',"Connected")
        
        
        ser=RCxxSerial.OpenSerial(serialport,Speed)
        RCxxSerial.WriteOnly(ser,"sdf45"+crlf,"crlf")
        RCxxSerial.WriteOnly(ser,crlf,"crlf")
        commtimer()
        
    Stat.configure(state='disabled')
    Stat.configure(state='disabled')
    spdm.configure(state='disabled')
    




    
def DoDisconnect(event=None):
    global spdm
    #RCxxSerial.DoExit(serialport,Speed)
    RCxxSerial.WriteCrLf(ser)

    RCxxSerial.FlushOutput(ser)
    RCxxSerial.WriteCrLf(ser)

    RCxxSerial.WriteRead(ser,"EXIT","Start")
    RCxxSerial.WriteCrLf(ser)
    #spdm.configure(state='normal')
    #chooseCommPort(serialPortNotSelectedTxt)   
    #spdm.configure(state='normal')
    

def commtimer():
    global ser,buffer,DoRx
    
    cw=ser.inWaiting()
    if cw>0:
       buffer+=ser.read(cw).decode()
       
    if crlf in buffer:
         line,buffer=buffer.split('\n',1)
         islist=True
         print ("!"+line+"!")
         if 'Start?:' in line: islist=False
         if 'EXIT FILE MODE' in line: islist=False
           
         if islist:
             list2.insert(END, line)
             list2.yview(END)

    root.after(10, commtimer)


    

#def DoCr():
#    RCxxSerial.WriteOnly(ser,"test"+crlf,"crlf")

def DoExit():
    RCxxSerial.WriteCrLf(ser)

    RCxxSerial.FlushOutput(ser)
    RCxxSerial.WriteCrLf(ser)

    RCxxSerial.WriteRead(ser,"EXIT","Start")
    RCxxSerial.WriteCrLf(ser)


def GetAddress():
    
    Address=AddressBox.get()
    ad=-1
    try:
       ad=int(Address, base=16)
    except:
        ok=False
    
    if ad<0 or ad>0xffff:
        ad=-1
    if ad==-1 :
        messagebox.showwarning(title="Address/Number", message="Address/Number out of range 0-0xffff")
        
    return ad
    
def DoWatch():
    Address=GetAddress()
    adh=f'{Address:X}'
    if Address>=0:
        #send initial string
        RCxxSerial.WriteRead(ser,StartToken,"Start Ok")
        #send command
        RCxxSerial.WriteRead(ser,"WATCH","WATCH")
        time.sleep(0.1)
        if b"OK" not in RCxxSerial.WriteRead(ser,adh,adh):
            print ("No OK returned")
        else :
            print ("Watch address set to ",adh)
            list2.insert(END, "Watch address set to ",adh)
            list2.yview(END)
        DoExit()
   
def DoTrace():
    Address=GetAddress()
    adh=f'{Address:X}'
    if Address>=0:
        #send initial string
        RCxxSerial.WriteRead(ser,StartToken,"Start Ok")
        #send command
        RCxxSerial.WriteRead(ser,"TRACE","TRACE")
        time.sleep(0.1)
        if b"OK" not in RCxxSerial.WriteRead(ser,adh,adh):
            print ("No OK returned")
        else :
            print ("Trace set to ",adh)
            list2.insert(END, "Trace set to ",adh)
            list2.yview(END)
        DoExit()

def DoMDump():
    
    Address=GetAddress()
    adh=f'{Address:X}'
    if Address>=0:
        #commTimerStop()
        #send initial string
        RCxxSerial.WriteRead(ser,StartToken,"Start Ok")
        #send command
        RCxxSerial.WriteRead(ser,"DUMP","DUMP")
        time.sleep(0.1)
        
        if b"OK" not in RCxxSerial.WriteRead(ser,adh,adh):
            print ("No OK returned")
        else :
            print ("DUMPING ",adh)
            list2.insert(END, "DUMPING ")
            list2.yview(END)
        
        
def DoDis():
    Address=GetAddress()
    adh=f'{Address:X}'
    if Address>=0:
        #send initial string
        RCxxSerial.WriteRead(ser,StartToken,"Start Ok")
        #send command
        RCxxSerial.WriteRead(ser,"DISSEMBLE","DISSEMBLE")
        time.sleep(0.1)
        if b"OK" not in RCxxSerial.WriteRead(ser,adh,adh):
            print ("No OK returned")
        else :
            print ("DISSEMBLE ",adh)
            list2.insert(END, "DISSEMBLE ")
            list2.yview(END)
       
def setAddress(text):
    AddressBox.delete(0,END)
    AddressBox.insert(0,text)
    return        

    
top = ''



#serialport selection
serialab=Entry(root,width=1,justify='right',relief="flat",disabledforeground="BLACK",font='Helvetica 10 bold')
serialab.insert('end',"Connect to RC20XX on ")
serialab.grid(row=0,column=0,sticky="NESW")
serialab.config(state="disabled")

sp=RCxxSerial.ListCommPorts(True)
sp.append(serialPortNotSelectedTxt)
spvar = StringVar()
spvar.set(serialport)
spdm = OptionMenu(root, spvar,*sp,command=chooseCommPort)
spdm.config(font='Helvetica 10 bold')
spdm.grid(row=0,column=1,sticky="NESW",columnspan=5)

#frame  for address box and label
AddrFr=Frame(root,borderwidth="0",padx=5,pady=5)
AddrFr.grid(row=5,column=0,sticky="NESW")

#Address box Label
Addrlab=Label(AddrFr,text="Addr/Num Hex ")
Addrlab.pack(side=LEFT,expand=True,fill=BOTH)

#Address Box
AddressBox=Entry(AddrFr,width=10,)
AddressBox.pack(side=LEFT,expand=True,fill=BOTH)


WatchBut=Button(root, text='Watch', command=DoWatch,width=1,state='disabled')
WatchBut.grid(sticky='NWE', column=0, row=6,padx=5,pady=5)

TraceBut=Button(root, text='Trace', command=DoTrace,width=1,state='disabled')
TraceBut.grid(sticky='NWE', column=0, row=7,padx=5,pady=5)

DumpBut=Button(root, text='Mem Dump', command=DoMDump,width=1,state='disabled')
DumpBut.grid(sticky='NWE', column=0, row=8,padx=5,pady=5)

DisBut=Button(root, text='Mem Dis', command=DoDis,width=1,state='disabled')
DisBut.grid(sticky='NWE', column=0, row=9,padx=5,pady=5)
 
ExitBut=Button(root, text='EXIT', command=DoDisconnect,width=1,state='disabled')
ExitBut.grid(sticky='NWE', column=0, row=10,padx=5,pady=5)


#footer
Stat=Text(root,height=1,width=100) 
Stat.insert('end',"Disconnected - Select a serial port to connect")
Stat.grid(row=12,column=0,columnspan=10)
Stat.configure(state='disabled')


#terminal scrollbar
list2 = Listbox(root) 
drivescrollbar = Scrollbar(list2)
drivescrollbar.pack( side = RIGHT, fill = Y )

list2.config(yscrollcommand = drivescrollbar.set, selectmode = "multiple")
drivescrollbar.config(command = list2.yview)

list2.grid(sticky='NSEW', column=1, row=4, rowspan=8, ipady=10, ipadx=10, columnspan=5)
list2.configure(background="black", foreground="green",selectforeground='Black',selectbackground='Green',
                activestyle='none',font='Courier 12',relief="solid",borderwidth="0",highlightcolor="black"
                ,highlightbackground="black")


controls(False)
setAddress("0x0000")

initterm()

if not isinstance(args.port, type(None)):
    chooseCommPort(args.port)

# run the main program
root.mainloop()
RCxxSerial.Close(ser)     
