import base64
import argparse
import time
import serial
import io
import sys
import os
import RCxxSerial

StartToken = "&&&-magic-XXX"
Speed=115200

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] ...",
        description="copy CPM Drive on RC20XX to local directory."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('directory', help="Local Directory to save files into")
    
    return parser

def DoExec(cmd):
    stream = os.popen(cmd)
    output = stream.read()
    if debug:print(cmd)
    print(output)

#Get Command line
parser = init_argparse()
args = parser.parse_args()

debug=args.debug

serialport= args.port
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

path=args.directory
if not os.path.isdir(path):
    print ("Path does not exist")
    sys.exit(1)

#Open Serial Port
ser=RCxxSerial.OpenSerial(serialport,Speed)

#Flush buffers
RCxxSerial.InitSerial(ser)

#send initial string
RCxxSerial.WriteRead(ser,StartToken,"StartTok")
#send command
RCxxSerial.WriteRead(ser,"LS","LS")
#send drive and wait for OK
if b"OK" not in RCxxSerial.WriteRead(ser,drive,"Drive"):
    print ("No OK returned")
    RCxxSerial.Close(ser)  
    sys.exit(1)
   
RCxxSerial.WriteRead(ser,"","After OK")   
#receive data
b64ls=RCxxSerial.ReadOnly(ser,"b64")
#remove crlf's
b64ls=b64ls.replace(b'\r',b'')
b64ls=b64ls.replace(b'\n',b'')
#close serial
RCxxSerial.Close(ser)             # close port
if debug :print("b64",b64ls)

#decode message
try:
    message_bytes = base64.b64decode(b64ls)
except:
    print("decode failed ",b64ls)
    sys.exit(1)
  
#print it  
#print ("Drive  D",drive)
directory=message_bytes.decode('utf_8')
#print(directory)

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
      
db=" "
if debug:db=" -d "
    
for file in filenames:
    print(path,file)  
    pathfile=os.path.join(path,file)
    pythonpath=sys.executable
    cmd=pythonpath +" CopyFrom-RC20xx.py " + serialport + db + drive + " " + pathfile
    DoExec(cmd ) 
    time.sleep(0.1)    

