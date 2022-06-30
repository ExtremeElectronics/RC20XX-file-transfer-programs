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
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    return parser

def WriteCrLf():
    ser.write((crlf).encode('utf_8')) # write a string

def ReadOnly(ExpectData,dbt):
    if debug : print("Read ",dbt);
    ReadText = ser.readline() # read a string
    
    if(ExpectData and len(ReadText)==0):
      print ("Read only Timeout ")
      ser.close()             # close port
      sys.exit(1)
      
    if debug : print(ReadText.decode('ascii','ignore')) 
    return ReadText


def WriteRead(text,ExpectData,dbt):
    if debug : print("Write ",dbt);
    ser.flushInput()
    ser.write((text+crlf).encode('utf_8')) # write a string
    
    return ReadOnly(ExpectData," Read AfterWrite")




parser = init_argparse()
args = parser.parse_args()

debug=args.debug

serialport=args.port.upper()
if serialport=="": serialport="COM1"
drive=args.drive.upper()
if drive=="": drive="A"

try:
  ser = serial.Serial(serialport, 115200, timeout=5)  # open serial port
except:
  print ("Cant open serial port ",serialport)
  sys.exit(1)
  
if debug : print(ser.name)         # check which port was really used

StartToken = "&&&-magic-XXX"
EndToken = "XXX-magic-&&&"
crlf='\n';



#ser = serial.serial_for_url('loop://', timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),newline = '\n',line_buffering = True)              
    
ser.flushOutput()
ser.write((crlf+crlf).encode('utf_8'))
time.sleep(0.1)
ser.flushInput()
time.sleep(0.1)

WriteCrLf()
WriteRead(StartToken,True,"StartTok")
WriteRead("LS",True,"LS")

if b"OK" not in WriteRead(drive,True,"Drive"):
   print ("No OK returned")
   ser.close()
   sys.exit(1)
   
WriteRead("",False,"OK")   
b64ls=ReadOnly(True,"b64")
b64ls=b64ls.replace(b'\r',b'')
b64ls=b64ls.replace(b'\n',b'')

ser.close()             # close port
if debug :print("b64",b64ls)

try:
  message_bytes = base64.b64decode(b64ls)
except:
  print("decode failed ",b64ls)
  sys.exit(1)
  
print ("Drive ",drive)
print(message_bytes.decode('utf_8'))
#WriteRead(EndToken)



