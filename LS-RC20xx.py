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
        description="List CPM Drive on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
   
    return parser

def DoExec(cmd):
    stream = os.popen(cmd)
    output = stream.read()
    print(cmd)
    print(output)

#Get Command line
parser = init_argparse()
args = parser.parse_args()

debug=args.debug

serialport= args.port
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

#Open Serial Port
ser=RCxxSerial.OpenSerial(serialport,Speed)

#Flush buffers
RCxxSerial.InitSerial(ser)

#send initial string
RCxxSerial.WriteRead(ser,StartToken,"Start Ok")
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
print ("Drive ",drive)
directory=message_bytes.decode('utf_8')
print(directory)
