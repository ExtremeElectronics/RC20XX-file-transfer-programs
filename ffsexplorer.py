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

serialport="-"
Speed=115200
StartToken = "&&&-magic-XXX"
DrivesMax=15 #A-O

debug=0
RCxxSerial.debug=debug

# Increase Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

#root = Tk()

root=TkinterDnD.Tk()

# set a title for our file explorer main window
root.title('RC20XX - FFS CPM Explorer')

root.geometry("500x800")
root.resizable(0, 1)

root.grid_columnconfigure(0, weight=10)
root.grid_columnconfigure(2, weight=20)

root.grid_rowconfigure(9, weight=3)

drivescrollbar = Scrollbar(root)

def driveChange(cpmdrive):
    
    # Get all Files  from the given CPMDirectory
    #cpmdrive = os.listdir(currentPath.get())
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
    filenames=RCxxSerial.DirectoryToFilenames(directory)
    for i,fn in enumerate(filenames):
        list2.insert(i,fn)

    #remove selection
    state="disabled"
    b3["state"]=state
    b4["state"]=state
        
def driveSelect(cd):
     print("Drive ",currentDrive.get())
     driveChange(currentDrive.get())   

#def pathChange(*event):
#    # Get all Files and Folders from the given Directory
#    directory = os.listdir(currentPath.get())
#   # Clearing the list
#   list1.delete(0, END)
#    # Inserting the files and directories into the list
#    for file in directory:
#        list1.insert(0, file)

def changePathByClick(event=None):
    # Get clicked item.
    picked = list1.get(list.curselection()[0])
    # get the complete path by joining the current path with the picked item
    path = os.path.join(currentPath.get(), picked)
    # Check if item is file, then open it
    if os.path.isfile(path):
        print('Opening: '+path)
        os.startfile(path)
    # Set new path, will trigger pathChange function.
    else:
        currentPath.set(path)

def goBack(event=None):
    # get the new path
    newPath = pathlib.Path(currentPath.get()).parent
    # set it to currentPath
    currentPath.set(newPath)
    # simple message
    print('Going Back')

def open_popup():
    global top
    top = Toplevel(root)
    top.geometry("250x150")
    top.resizable(False, False)
    top.title("Child Window")
    top.columnconfigure(0, weight=1)
    Label(top, text='Enter File or Folder name').grid()
    Entry(top, textvariable=newFileName).grid(column=0, pady=10, sticky='NSEW')
    Button(top, text="Create", command=newFileOrFolder).grid(pady=10, sticky='NSEW')

def newFileOrFolder():
    # check if it is a file name or a folder
    if len(newFileName.get().split('.')) != 1:
        open(os.path.join(currentPath.get(), newFileName.get()), 'w').close()
    else:
        os.mkdir(os.path.join(currentPath.get(), newFileName.get()))
    # destroy the top
    top.destroy()
    pathChange()

def controls(enable):
    if enable: state="normal"
    else: state="disabled"

    cpmdrive["state"]=state
    #b3["state"]=state
    #b4["state"]=state
    b5["state"]=state
    b9["state"]=state
    list2["state"]=state
    
def chooseCommPort(choice):
    global serialport,Status,spdm
    spvar.set(choice)
    serialport = choice
    Stat.configure(state='normal')
    Stat.delete('1.0', END)

    if serialport=="-":
        controls(False)
        Stat.insert('end',"Disconnected")
    else:
        sp=serialport.split("|")
        serialport=sp[0].strip()
        controls(True)
        driveChange(currentDrive.get())
        Stat.insert('end',"Connected")
        
    Stat.configure(state='disabled')
    spdm.configure(state='disabled')
    


def rmFile():
     if serialport=="-":
        messagebox.showerror('Serial Error', 'Not Connected')
     else:
        for i in list2.curselection():
            print(list2.get(i))
            filename=list2.get(i)
            #filename=list2.get(list2.curselection())
            print(filename)
            cpmdrive=currentDrive.get()
            RCxxSerial.DoRM(serialport,Speed,StartToken,cpmdrive,filename)
            time.sleep(0.5)
        
        driveChange(cpmdrive)
    
def refreshDrive():
    cpmdrive=currentDrive.get()
    driveChange(cpmdrive)

def CopyTo(event):
    if serialport=="-":
        messagebox.showerror('Serial Error', 'Not Connected')
    else:
        cpmdrive=currentDrive.get()
        print(event.data)
        files = root.tk.splitlist(event.data)
        for filepath in files:
            print(filepath)
           
            filename=os.path.basename(filepath)
            if RCxxSerial.CheckFilename(filename)==False:
               messagebox.showerror('File Error', 'Filename incompatible with CPM 8.3 format')
            else:   
               RCxxSerial.DoCopyTo(serialport,Speed,StartToken,cpmdrive,filepath,filename,4096)
               time.sleep(0.5)
           
        driveChange(cpmdrive)

def CopyFrom():
    if serialport=="-":
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

def DoExit(event=None):
    global spdm
    RCxxSerial.DoExit(serialport,Speed)
    spdm.configure(state='normal')
    chooseCommPort("-")   
    spdm.configure(state='normal')
    
top = ''
cpmDrive="A"


#Serial Port Selection
serialframe=Frame(root,height=10)
serialframe.grid(row=0,column=0,sticky="NESW",columnspan=3)
serialab=Label(serialframe,text="Connect to RC20XX on port ")
serialab.pack(side=LEFT,expand=True,fill=BOTH)
sp=RCxxSerial.ListCommPorts(True)
sp.append("-")
spvar = StringVar()
spvar.set(serialport)
spdm = OptionMenu(serialframe, spvar,*sp,command=chooseCommPort)
spdm.pack(side=LEFT,expand=True,fill=BOTH)



#create dropdown for drive
driveframe=Frame(root,bg="black")
driveframe.grid(row=1,column=1,sticky="NESW",columnspan=5)
drivelab=Label(driveframe,text="CPM Drive",fg="GREEN",bg="black",font='Helvetica 14 bold')
drivelab.pack(side=LEFT,expand=True,fill=BOTH)

Drives=[]
for d in range(0,DrivesMax):
    #print(d,chr(d+ord('A')))
    Drives.append(chr(d+ord('A')))
currentDrive=StringVar()
currentDrive.set(cpmDrive)
cpmdrive = OptionMenu(driveframe, currentDrive,*Drives,command=driveSelect)
cpmdrive.config(fg="GREEN",bg="black", font='Helvetica 14 bold')
cpmdrive["menu"].config(fg="GREEN",bg="black")
cpmdrive.pack(side=LEFT,expand=True,fill=BOTH)


#buttons
b3=Button(root, text='Erase', command=rmFile,width=1,state='disabled')
b3.grid(sticky='NWE', column=0, row=3,padx=5,pady=5)



b4=Button(root, text='Copy Selected', command=CopyFrom,width=1,state='disabled')
b4.grid(sticky='NWE', column=0, row=4,padx=5,pady=5)

b5=Button(root, text='Refresh', command=refreshDrive,width=1)
b5.grid(sticky='NWE', column=0, row=5,padx=5,pady=5)

Label(root,text=" ").grid(sticky='NW', column=0, row=7)

b9=Button(root, text='Disconnect', command=DoExit,width=1)
b9.grid(sticky='NWE', column=0, row=8,padx=5,pady=5)

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

list2.grid(sticky='NSEW', column=1, row=2, rowspan=10, ipady=10, ipadx=10, columnspan=5)
list2.configure(background="black", foreground="green",selectforeground='Black',selectbackground='Green', activestyle='none')

list2.drop_target_register(DND_FILES)
list2.dnd_bind('<<Drop>>', CopyTo)
list2.bind('<Button-1>', FilesSelected)



# Menu
#menubar = Menu(root)
# Adding a new File button
#menubar.add_command(label="Add File or Folder", command=open_popup)
# Adding a quit button to the Menubar
#menubar.add_command(label="Quit", command=root.quit)
# Make the menubar the Main Menu
#root.config(menu=menubar)

# Call the function so the list displays
#pathChange('')
controls(False)
#driveChange('A')
# run the main program
root.mainloop()
