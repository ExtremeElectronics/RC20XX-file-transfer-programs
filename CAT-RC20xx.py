import serial
import io
import time
import base64
import sys
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] ...",
        description="List CPM Directory on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )

    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('filename', help="CPM file on the Attached RC20XX")
    
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=0

serialport=args.port #.upper()
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

filename=args.filename
if filename=="":sys.exit(1)
if len(filename)>12:sys.exit(1)

try:
  ser = serial.Serial(serialport, 115200, timeout=5)  # open serial port
except:
  print ("Cant open serial port ",serialport)
  sys.exit(1)
  
if debug : print(ser.name)         # check which port was really used

StartToken = "&&&-magic-XXX"
EndToken = "XXX-magic-&&&"
crlf='\n';

def WriteRead(text):
    ser.write((text+crlf).encode('utf_8')) # write a string
    #ser.flushOutput()
    time.sleep(0.1)
    try:
      ReadText = ser.readline() # read a string
    except serial.SerialTimeoutException:
      print ("Timeout")
      ser.close()             # close port
      sys.exit(1)
      
    if debug : print(ReadText.decode("ascii",'ignore')) 
    return ReadText

def ReadOnly():
    try:
      ReadText = ser.readline() # read a string
    except serial.SerialTimeoutException:
      print ("Timeout")
      ser.close()             # close port
      sys.exit(1)
      
    if debug : print(ReadText.decode('ascii','ignore')) 
    return ReadText


sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),newline = '\n',line_buffering = True)              
    
ser.flushOutput()
ser.write((crlf+crlf).encode('utf_8'))
time.sleep(0.1)
ser.flushInput()
time.sleep(0.1)

print("fetching ",filename);

WriteRead(StartToken)
WriteRead("COPYFROM")
WriteRead(drive)

if debug :print("wait for OK");
if b"OK" not in WriteRead(filename): #read OK
   print ("No OK returned")
   sys.exit(1)
   
if debug :print("wait for filename");
ReadOnly() #read filename
ReadOnly()
if debug :print("wait for base64");
b64ls=ReadOnly()
if debug :print(b64ls)
b64ls=b64ls.replace(b'\r',b'')
b64ls=b64ls.replace(b'\n',b'')

ser.close()             # close port
if debug :print("b64",b64ls)

try:
  message_bytes = base64.b64decode(b64ls)
except:
  print("base 64 decode failed ",b64ls)
  sys.exit(1)

print (filename)

if len(message_bytes)<2:
    print ("File empty")
    sys.exit(1)
else:
    print(message_bytes.decode('utf_8'))




#WriteRead(EndToken)




