import serial
import io
import time
import base64
import sys
import argparse
import os.path

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] [filepath]...",
        description="List CPM Directory on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )

    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('filepath', help="local CPM file and file to save on the Attached RC20XX")
    
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=0
bufsize=(3*1024) #needs to be divisable by 3 &4

serialport=args.port.upper()
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

filepath=args.filepath
filename=os.path.basename(filepath)
if debug: print(filepath,filename)

if filename=="":sys.exit(1)
if len(filename)>12:sys.exit(1)

try:
  ser = serial.Serial(serialport, 115200, timeout=5)  # open serial port
except:
  print ("Can't open serial port ",serialport)
  sys.exit(1)
  
if debug : print(ser.name)         # check which port was really used

StartToken = "&&&-magic-XXX"
EndToken = "XXX-magic-&&&"
crlf='\n';


def WriteRead(text,b=0):
    if debug : print(">",text)
    ser.flushInput()
    if(b==0):
      ser.write((text+crlf).encode('utf_8')) # write a string
    else:
      ser.write(text+crlf.encode('utf_8')) # write a string  
    
    time.sleep(0.1)
   
    ReadText = ser.readline() # read a string
    if(len(ReadText)==0):
      print ("Timeout")
      ser.close()             # close port
      sys.exit(1)
      
    if debug : print("<",ReadText.decode("ascii",'ignore')) 
    return ReadText

def ReadOnly():
    ser.flushInput()
    if debug : print("RD")
    ReadText = ser.readline() # read a string
    if(len(ReadText)==0):
      print ("Timeout")
      ser.close()             # close port
      sys.exit(1)
      
    if debug : print("<",ReadText.decode('ascii','ignore')) 
    return ReadText

if not os.path.exists(filepath):
    print(filepath, "does not exist in this directory")
    sys.exit(1)

sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),newline = '\n',line_buffering = True)              
    
ser.flushOutput()
ser.write((crlf+crlf).encode('utf_8'))
time.sleep(0.1)
ser.flushInput()
time.sleep(0.1)

start = time.time()

print("sending ",filename);

WriteRead(StartToken)
WriteRead("COPYTO")
WriteRead(drive)


if b"OK" not in WriteRead(filename) :#read OK
   print ("No OK returned")
   ser.close() 
   sys.exit(1)
   
localfile = open(filepath, "rb")
while True:
    message_bytes = localfile.read(bufsize)
    if not message_bytes:
        if debug :print("EOM");
        break
    
    #send chunk size
    if debug :print("sending chunk ");
    WriteRead(str(len(message_bytes)))

    print(".", end='');
    
    b64ls=base64.b64encode(message_bytes)
    if debug :print("send base64\n");
    if b"OK" not in WriteRead(b64ls,1):
        print(" failed to acknoledge last packet")
        break
    
localfile.close()
print("")

#send zero chunk
if debug :print("send zero CS");
#ReadOnly()
if b"OK" not in WriteRead("0"):
   print ("No OK returned")
   ser.close() 
   sys.exit(1)
   
end = time.time()
ser.close()             # close port



print (filepath+" Sent")
if debug: print("in ",end-start);





