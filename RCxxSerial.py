import serial
import io
import time
import sys
import serial.tools.list_ports
import base64
import os.path

debug=0;
crlf='\n';


#     ________________________________
#    /                                |
#   /       RC20xx  FFS tools         |
#  /         Derek Woodroffe          |
# |  O        Extreme Kits            |
# |     Kits at extkits.uk/RC2040     |
# |               2022                |
# |___________________________________|
#   | | | | | | | | | | | | | | | | |

# https://github.com/ExtremeElectronics/RC20XX-file-transfer-programs

#Serial Def's

def ListCommPorts(withdesc=False):
    cp=[]
    ports = serial.tools.list_ports.comports()
    for p in ports:
       #print(p.device)
        if withdesc: 
           cp.append(p.device+" | "+ p.description)
        else:
           cp.append(p.device)
    return cp
       
def WriteCrLf(ser):
    ser.write((crlf).encode('utf_8')) # write a string


def ReadOnly(ser,dbt):
    if debug : print("Read ",dbt);
    ReadText = ser.readline() # read a string
    if(len(ReadText)==0):
      print ("Timeout")
      ser.close()             # close port
      sys.exit(1)
      
    if debug : print("<",ReadText.decode('ascii','ignore')) 
    return ReadText


def WriteRead(ser,text,dbt,binary=0):
    if debug : print("Write ",dbt)
    ser.flushInput()
    #ser.write((text+crlf).encode('utf_8')) # write a string
    
    if(binary==0):
      ser.write((text+crlf).encode('utf_8')) # write a string
    else:
      ser.write(text+crlf.encode('utf_8')) # write a string  
      
    ReadText = ser.readline() # read a string
    if(len(ReadText)==0):
      print ("Timeout ",dbt)
      ser.close()             # close port
      #sys.exit(1)
      raise SystemExit(1)
      
    if debug : print("<",ReadText.decode("ascii",'ignore')) 
    return ReadText
    
    
def WriteOnly(ser,text,dbt,binary=0):
    if debug : print("Write ",dbt)
    ser.flushInput()
    if(binary==0):
      ser.write((text+crlf).encode('utf_8')) # write a string
    else:
      ser.write(text+crlf.encode('utf_8')) # write a string  
      
   
def FlushOutput(ser):
    ser.flushOutput()
    
def FlushInput(ser):
    ser.flushInput()

def OpenSerial(serialport,speed):
    try:
        ser = serial.Serial(serialport, speed, timeout=5)  # open serial port
    except serial.SerialException as e:
        print ("Cant open serial port ",serialport,e)
        sys.exit(1)
    #sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),newline = '\n',line_buffering = True)    
    return ser
        
def InitSerial(ser):
    ser.write(("0"+crlf+"##"+crlf).encode('utf_8'))       #scrap previous waiting commands
    ser.write(("0"+crlf+"##"+crlf).encode('utf_8'))       #scrap previous waiting commands
                        
    if debug : print(ser.name)         # check which port was really used
    
    FlushOutput(ser)
    WriteCrLf(ser)
    WriteCrLf(ser)
    time.sleep(0.1)
    FlushInput(ser)
    time.sleep(0.1)
    
    return ser
    
def Close(ser):
    ser.close()

#Routines

def DirectoryToFilenames(directory):
    lines=directory.split("\n")
    filenames=[]
    for line in lines:
        a1=line.split(".")
        if len(a1)>1:
            #print(a1[1])
            a2=a1[1].split(" ")
            #print(a2)
            filename=a1[0].strip()+"."+a2[0]
            #print (filename)
            if len(filename)<=13:
                filenames.append(filename)
    return filenames


def CheckFilename(filename):
    fnok=True
    why=""
    
    #create acceptable char list
    okchar=[]
    for a in range(0,26):
      okchar.append(chr(ord('A')+a))
      okchar.append(chr(ord('a')+a))
    for a in range(0,10):
      okchar.append(chr(ord('0')+a))  
    okchar.append('.')

    #check all chars are in above list
    for a in range(0,len(filename)):
      if not filename[a] in okchar :fnok=False

    if fnok==False:why="Bad Char"  

    #check length and dot position
    if "." in filename:  
      p=filename.split(".")
      #check lengths either side of .'s
      if len(p[0])<1 or len(p[0])>8 : fnok=False 
      if len(p[1])<1 or len(p[1])>3 : fnok=False
      if len(p)>2:fnok=False #toomany .'s
      if fnok==False:why+=" .position"
    else:
        #no .
        fnok=False
        if fnok==False:why+=" no ."
    
    return fnok



#File Move commands

def DoWho(serialport,Speed,StartToken):
    #Open Serial Port
    ser=OpenSerial(serialport,Speed)

    #Flush buffers
    InitSerial(ser)

    #send initial string
    WriteRead(ser,StartToken,"Start Ok")
    #send command
    WriteRead(ser,"WHO","WHO")
    who=ReadOnly(ser,"who?").decode()
    #close serial
    Close(ser)             # close port
    return who.strip()



def DoLS(serialport,Speed,StartToken,drive):
    #Open Serial Port
    ser=OpenSerial(serialport,Speed)

    #Flush buffers
    InitSerial(ser)

    #send initial string
    WriteRead(ser,StartToken,"Start Ok")
    #send command
    WriteRead(ser,"LS","LS")
    #send drive and wait for OK
    if b"OK" not in WriteRead(ser,drive,"Drive"):
       print ("No OK returned")
       Close(ser)  
       sys.exit(1)
       
    WriteRead(ser,"","After OK")   
    #receive data
    b64ls=ReadOnly(ser,"b64")
    #remove crlf's
    b64ls=b64ls.replace(b'\r',b'')
    b64ls=b64ls.replace(b'\n',b'')
    
    #close serial
    Close(ser)             # close port
    return b64ls



def DoCat(serialport,Speed,StartToken,drive,filename):
    if CheckFilename(filename)==False:
        print ("Invalid Filename ",filename)
        sys.exit(1)    
        
    #Open Serial Port
    ser=OpenSerial(serialport,Speed)

    #Flush buffers
    InitSerial(ser)

    WriteRead(ser,StartToken,"Start Ok")
    WriteRead(ser,"COPYFROM","CopyFrom")
    WriteRead(ser,drive,"Drive")

    if debug :print("wait for OK");
    if b"OK" not in WriteRead(ser,filename,"FileName"): #read OK
       print ("No OK returned")
       sys.exit(1)
       
    ReadOnly(ser,"filename") #read filename
    ReadOnly(ser,"After Filename")

    b64cat=ReadOnly(ser,"b64")
    b64cat=b64cat.replace(b'\r',b'')
    b64cat=b64cat.replace(b'\n',b'')

    ser.close()             # close port

    return b64cat

def DoCopyTo(serialport,Speed,StartToken,drive,filepath,filename,bufsize):
    if CheckFilename(filename)==False:
        print ("Invalid Filename ",filename)
        sys.exit(1)    
        
    totalsize=0;
    
    if not os.path.exists(filepath):
        print (filepath, " doesn't exist")
        sys.exit(1)
    
    try: 
      localfile = open(filepath, "rb")
    except:
        print ("Cant open",filepath)
        sys.exit(1)
       
    
    #Open Serial Port
    ser=OpenSerial(serialport,Speed)

    #Flush buffers
    InitSerial(ser)
    #send initial string
    WriteRead(ser,StartToken,"Start Ok")
    #send command
    WriteRead(ser,"COPYTO","COPYTO")
    #send drive
    WriteRead(ser,drive,"Drive")

    #send filename and wait for OK
    if b"OK" not in WriteRead(ser,filename,"Wait for OK") :#read OK
        print ("No OK returned (cleck file donesn't already Exist)")
        Close(ser) 
        sys.exit(1)
       
    
    while True:
        message_bytes = localfile.read(bufsize)
        if not message_bytes:
             if debug :print("EOM");
             break

        txt=ReadOnly(ser,"Wait for ChunkSize:")

        if b"Chunk" not in txt:
             print(" Not Rceived Chunksize: ", txt)
             Close(ser)
             sys.exit(1)
       
        #send chunk size
        if debug :print("sending chunk ",str(len(message_bytes)) )
        txt=WriteRead(ser,str(len(message_bytes)),"Chunk")
        if b"Data" not in txt:
             print(" Not Rceived Data: ", txt)
             RCxxSerial.Close(ser)
             sys.exit(1)
             
        totalsize+=len(message_bytes)
        print(".", end='',flush=True)
        
        b64ls=base64.b64encode(message_bytes)
        if debug :print("send base64\n")
        txt=WriteRead(ser,b64ls,"b64",1)
        if b"OK" not in txt:
             print(" Not Received OK ", txt)
             Close(ser)
             sys.exit(1)
          
    time.sleep(0.1)   
       
    localfile.close()
    print("")

    #send zero chunk
    if debug :print("send zero Chunk");

    #ReadOnly()
    txt=WriteRead(ser,"0","0")
    if b"OK" not in txt :
        print ("No OK returned on last chunk ",txt)
        Close(ser) 
        sys.exit(1)
       
    Close(ser)           # close port
    return totalsize


def DoRM(serialport,Speed,StartToken,drive,filename):

    if CheckFilename(filename)==False:
        print ("Invalid Filename ",filename)
        sys.exit(1)    
        
    
    #Open Serial Port
    ser=OpenSerial(serialport,Speed)

    #Flush buffers
    InitSerial(ser)

    WriteRead(ser,StartToken,"Start Ok")
    WriteRead(ser,"RM","RM")
    WriteRead(ser,drive,"Drive")

    txt=WriteRead(ser,filename,"OK")
    if b"OK" not in txt :#read OK
       print ("No OK returned ",txt)
       Close(ser)
       sys.exit(1)
       
    Close(ser)            # close port


def DoCopyFrom(serialport,Speed,StartToken,drive,filename):

    if CheckFilename(filename)==False:
        print ("Invalid Filename ",filename)
        sys.exit(1)    
        
    #Open Serial Port
    ser=OpenSerial(serialport,Speed)

    #Flush buffers
    InitSerial(ser)
    #send initial string
    WriteRead(ser,StartToken,"Start Ok")
    #send command
    WriteRead(ser,"COPYFROM","COPYFROM")
    #send drive
    WriteRead(ser,drive,"Drive")

    print("fetching ",filename);

    if debug :print("wait for OK");
    if b"OK" not in WriteRead(ser,filename,"Filename"): #read OK
       print ("No OK returned")
       Close(ser) 
       sys.exit(1)
       
    if debug :print("wait for filename");
    ReadOnly(ser,"Fn1") #read filename
    ReadOnly(ser,"Fn2")
    if debug :print("wait for base64");
    b64from=ReadOnly(ser,"B64")
    if debug :print(b64ls)
    b64from=b64from.replace(b'\r',b'')
    b64from=b64from.replace(b'\n',b'')

    Close(ser)              # close port

    return b64from


def DoExit(serialport,Speed):
    #Open Serial Port
    ser=OpenSerial(serialport,Speed)

    #Flush buffers
    InitSerial(ser)

    WriteCrLf(ser)

    FlushOutput(ser)
    WriteCrLf(ser)

    WriteRead(ser,"EXIT","Start")
    WriteCrLf(ser)
    Close(ser)            
