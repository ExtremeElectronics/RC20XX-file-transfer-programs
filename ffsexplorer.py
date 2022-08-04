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

serialPortNotSelectedTxt="Select Port"
serialport=serialPortNotSelectedTxt
Speed=115200
StartToken = "&&&-magic-XXX"
DrivesMax=15 #A-O



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

debug=0
RCxxSerial.debug=debug

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] ",
        description="List CPM Drive on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    
    parser.add_argument('--port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('--drive', help="CPM Drive on the Attached RC20XX")
   
    return parser

#Get Command line
parser = init_argparse()
args = parser.parse_args()

# Increase Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

#create root 
root=TkinterDnD.Tk()

# set a title for our file explorer main window
root.title('RC20XX - FFS CPM Explorer')

root.geometry("500x800")
root.resizable(0, 1)

root.grid_columnconfigure(0, weight=10)
root.grid_columnconfigure(2, weight=20)

root.grid_rowconfigure(9, weight=3)

drivescrollbar = Scrollbar(root)
dirfilenames=[]
def initdirectory():
    list2["state"]="normal"
    list2.delete(0, END)
    list2.insert(0,"")
    list2.insert(1,"    ________________________")
    list2.insert(2,"   /                        |")
    list2.insert(3,"  /   RC20xx  FFS tools     |")
    list2.insert(4," /     Derek Woodroffe      |")
    list2.insert(5,"|  O    Extreme Kits        |")
    list2.insert(6,"| Kits at extkits.uk/RC2040 |")
    list2.insert(7,"|            2022           |")
    list2.insert(8,"|___________________________|")
    list2.insert(9," | | | | | | | | | | | | | | | ")
    list2["state"]="disabled"    

def driveChange(cpmdrive):
    global dirfilenames
    if serialport!=serialPortNotSelectedTxt:
        # Get all Files  from the given CPMDirectory
        # Clearing the list
        list2.delete(0, END)
        # Inserting the files and directories into the list
        #for file in cpmdrive:
        #    list2.insert(1, file)
        currentDrive.set(cpmdrive)
        b64ls=RCxxSerial.DoLS(serialport,Speed,StartToken,cpmdrive)
        if debug :print("b64",b64ls)
        #decode message
        try:
            message_bytes = base64.b64decode(b64ls)
        except:
            print("decode failed ",b64ls)
            sys.exit(1)
        directory=message_bytes.decode('utf_8')
        dirfilenames=RCxxSerial.DirectoryToFilenames(directory)
        for i,fn in enumerate(dirfilenames):
            list2.insert(i,fn)

    #remove selection
    state="disabled"
    b3["state"]=state
    b4["state"]=state
        
def driveSelect(cd):
     print("Drive ",currentDrive.get())
     driveChange(currentDrive.get())   

def controls(enable):
    if enable: state="normal"
    else: state="disabled"

    cpmdrive["state"]=state
    b5["state"]=state
    b10["state"]=state
    list2["state"]=state
    
def chooseCommPort(choice):
    global serialport,Status,spdm
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
        who=RCxxSerial.DoWho(serialport,Speed,StartToken)
        controls(True)
        driveChange(currentDrive.get())
        Stat.insert('end',"Connected")
        #serialab.insert('end',"Connected to RC20XX on ")
        serialab.insert('end',"Connected to "+who+" on ")
        
    Stat.configure(state='disabled')
    Stat.configure(state='disabled')
    spdm.configure(state='disabled')
    
def cpmFileExists(filename):
    fne=False
    if filename in dirfilenames:fne=True
    return fne

def rmFile():
     if serialport==serialPortNotSelectedTxt:
        messagebox.showerror('Serial Error', 'Not Connected')
     else:
        for i in list2.curselection():
            print(list2.get(i))
            filename=list2.get(i)
            if cpmFileExists(filename):
                #filename=list2.get(list2.curselection())
                print(filename)
                cpmdrive=currentDrive.get()
                RCxxSerial.DoRM(serialport,Speed,StartToken,cpmdrive,filename)
                time.sleep(0.5)
            else:
                messagebox.showerror('File Error', 'Filename doesnt exist')
        driveChange(cpmdrive)
    
def refreshDrive():
    cpmdrive=currentDrive.get()
    driveChange(cpmdrive)

def CopyTo(event):
    if serialport==serialPortNotSelectedTxt:
        messagebox.showerror('Serial Error', 'Not Connected')
    else:
        
        cpmdrive=currentDrive.get()
        print(event.data)
        files = root.tk.splitlist(event.data)
        for filepath in files:
            print(filepath)
           
            filename=os.path.basename(filepath)
            if not cpmFileExists(filename):
                if RCxxSerial.CheckFilename(filename)==False:
                   messagebox.showerror('File Error', 'Filename incompatible with CPM 8.3 format')
                else:   
                   RCxxSerial.DoCopyTo(serialport,Speed,StartToken,cpmdrive,filepath,filename,4096)
                   time.sleep(0.5)
            else:
                messagebox.showerror('File Error', 'Filename exists')
        driveChange(cpmdrive)

def CopyFrom():
    if serialport==serialPortNotSelectedTxt:
        messagebox.showerror('Serial Error', 'Not Connected')
    else:
        #get destination directory
        path = filedialog.askdirectory()
        print (path)
        #get list of file names
        for i in list2.curselection():
            print(list2.get(i))
            filename=list2.get(i)
            filepath=os.path.join(path,filename)
            #call Copy From
            cpmdrive=currentDrive.get()
            print(serialport,Speed,StartToken,cpmdrive,filename)
            b64from=RCxxSerial.DoCopyFrom(serialport,Speed,StartToken,cpmdrive,filename)
            try:
                message_bytes = base64.b64decode(b64from)
            except:
                print("base 64 decode failed ",b64from,filename)
                sys.exit(1)
            if len(message_bytes)<2:
                print ("File empty Save aborted",filepath)
            else:
                localfile = open(filepath, "wb")
                localfile.write(message_bytes)
                localfile.close()

        driveChange(cpmdrive)

def FilesSelected(event):
    state="normal"
    b3["state"]=state
    b4["state"]=state

def DoReconnect(event=None):
    global spdm
    RCxxSerial.DoExit(serialport,Speed)
    spdm.configure(state='normal')
    chooseCommPort(serialPortNotSelectedTxt)   
    spdm.configure(state='normal')
    
def DoDisconnect(event=None):
    global spdm
    RCxxSerial.DoExit(serialport,Speed)
    spdm.configure(state='normal')
    chooseCommPort(serialPortNotSelectedTxt)   
    spdm.configure(state='normal')

    
    
top = ''
cpmDrive="A"

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
#spdm.pack(side=LEFT,expand=True,fill=BOTH)
spdm.grid(row=0,column=1,sticky="NESW",columnspan=5)



#create dropdown for drive letter
driveframe=Frame(root,bg="black",borderwidth="0")
driveframe.grid(row=1,column=1,sticky="NESW",columnspan=5)
drivelab=Label(driveframe,text="CPM Drive",fg="GREEN",bg="black",font='Helvetica 14 bold'
               ,relief="solid",borderwidth="0",highlightcolor="black",highlightbackground="black")
drivelab.pack(side=LEFT,expand=True,fill=BOTH)

Drives=[]
for d in range(0,DrivesMax):
    #print(d,chr(d+ord('A')))
    Drives.append(chr(d+ord('A')))
currentDrive=StringVar()
currentDrive.set(cpmDrive)
cpmdrive = OptionMenu(driveframe, currentDrive,*Drives,command=driveSelect)
cpmdrive.config(fg="GREEN",bg="black", font='Helvetica 14 bold',relief="solid"
                ,borderwidth="0",highlightcolor="black",highlightbackground="black")
cpmdrive["menu"].config(fg="GREEN",bg="black")
cpmdrive.pack(side=LEFT,expand=True,fill=BOTH)


#seperator
Frame(root,background="green",highlightcolor="green",highlightbackground="green").grid(sticky='NWSE', column=1, row=3, columnspan=5)

 
#buttons
b3=Button(root, text='Erase', command=rmFile,width=1,state='disabled')
b3.grid(sticky='NWE', column=0, row=4,padx=5,pady=5)

b4=Button(root, text='Copy Selected', command=CopyFrom,width=1,state='disabled')
b4.grid(sticky='NWE', column=0, row=5,padx=5,pady=5)

b5=Button(root, text='Refresh', command=refreshDrive,width=1)
b5.grid(sticky='NWE', column=0, row=6,padx=5,pady=5)

#b6=Button(root, text='Reconnect', command=DoReconnect,width=1)
#b6.grid(sticky='NWE', column=0, row=7,padx=5,pady=5)
 
b10=Button(root, text='Disconnect', command=DoDisconnect,width=1)
b10.grid(sticky='NWE', column=0, row=10,padx=5,pady=5)


#footer
Stat=Text(root,height=1,width=100) 
Stat.insert('end',"Disconnected - Select a serial port to connect")
Stat.grid(row=12,column=0,columnspan=10)
Stat.configure(state='disabled')



#drive scrollbar
list2 = Listbox(root) 
drivescrollbar = Scrollbar(list2)
drivescrollbar.pack( side = RIGHT, fill = Y )

list2.config(yscrollcommand = drivescrollbar.set, selectmode = "multiple")
drivescrollbar.config(command = list2.yview)

list2.grid(sticky='NSEW', column=1, row=4, rowspan=8, ipady=10, ipadx=10, columnspan=5)
list2.configure(background="black", foreground="green",selectforeground='Black',selectbackground='Green',
                activestyle='none',font='Courier 12',relief="solid",borderwidth="0",highlightcolor="black"
                ,highlightbackground="black")

list2.drop_target_register(DND_FILES)
list2.dnd_bind('<<Drop>>', CopyTo)
list2.bind('<Button-1>', FilesSelected)

controls(False)

initdirectory()


if not isinstance(args.port, type(None)):
    chooseCommPort(args.port)

if not isinstance(args.drive, type(None)):
    driveChange(args.drive.upper())

# run the main program
root.mainloop()

