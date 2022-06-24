import serial
import io
import time
import base64
import sys
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] ...",
        description="Remove CPM File on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )

    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('filename', help="local CPM file and file to save on the Attached RC20XX")
    
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=0
serialport=args.port.upper()
if serialport=="": serialport="COM1"
drive=args.drive.upper()
if drive=="": drive="A"

filename=args.filename

try:
  ser = serial.Serial(serialport, 115200, timeout=5)  # open serial port
except:
  print ("Can't open serial port ",serialport)
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



#ser = serial.serial_for_url('loop://', timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),newline = '\n',line_buffering = True)              
    
ser.flushOutput()
ser.write((crlf+crlf).encode('utf_8'))
time.sleep(0.1)
ser.flushInput()
time.sleep(0.1)

WriteRead(StartToken)
WriteRead("RM")
WriteRead(drive)

if b"OK" not in WriteRead(filename) :#read OK
   print ("No OK returned")
   sys.exit(1)
   


ser.close()             # close port

print ("Removed",filename)
#WriteRead(EndToken)



