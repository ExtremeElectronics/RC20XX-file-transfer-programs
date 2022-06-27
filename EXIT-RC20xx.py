import serial
import io
import time
import base64
import sys
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] ...",
        description="EXIT Serial File Mode on RC2040."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )

    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=0
serialport=args.port #.upper()
if serialport=="": serialport="COM1"


try:
  ser = serial.Serial(serialport, 115200, timeout=5)  # open serial port
except:
  print ("Cant open serial port ",serialport)
  sys.exit(1)
  
if debug : print(ser.name)         # check which port was really used

StartToken = "EXIT"
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
#WriteRead("EXIT")
ser.close()             # close port


  
print ("EXIT")



