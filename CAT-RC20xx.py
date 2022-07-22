import serial
import io
import time
import base64
import sys
import argparse
import RCxxSerial

StartToken = "&&&-magic-XXX"
Speed=115200

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] ...",
        description="CAT CPM File on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('filename', help="CPM file to cat on the Attached RC20XX")
    
    
    return parser


parser = init_argparse()
args = parser.parse_args()

debug=args.debug
RCxxSerial.debug=debug

serialport=args.port 
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

filename=args.filename
if filename=="":sys.exit(1)
if len(filename)>12:sys.exit(1)

#Open Serial Port
ser=RCxxSerial.OpenSerial(serialport,Speed)

#Flush buffers
RCxxSerial.InitSerial(ser)

RCxxSerial.WriteRead(ser,StartToken,"Start Ok")
RCxxSerial.WriteRead(ser,"COPYFROM","CopyFrom")
RCxxSerial.WriteRead(ser,drive,"Drive")

if debug :print("wait for OK");
if b"OK" not in RCxxSerial.WriteRead(ser,filename,"FileName"): #read OK
   print ("No OK returned")
   sys.exit(1)
   

RCxxSerial.ReadOnly(ser,"filename") #read filename
RCxxSerial.ReadOnly(ser,"After Filename")

b64ls=RCxxSerial.ReadOnly(ser,"b64")
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




