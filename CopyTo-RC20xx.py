import serial
import io
import time
import base64
import sys
import argparse
import os.path
import RCxxSerial

StartToken = "&&&-magic-XXX"
Speed=115200

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] [filepath]...",
        description="Copy file to CPM Drive on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('filepath', help="local CPM file and file to save on the Attached RC20XX")
    
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=args.debug
RCxxSerial.debug=debug

bufsize=(4*1024) #needs to be EXACTLY 4096  else cpmWrite fails

zork=96000
totalsize=0

serialport=args.port 
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

filepath=args.filepath
filename=os.path.basename(filepath)
if debug: print(filepath,filename)

if filename=="":sys.exit(1)
if len(filename)>12:sys.exit(1)

#Open Serial Port
ser=RCxxSerial.OpenSerial(serialport,Speed)

#Flush buffers
RCxxSerial.InitSerial(ser)
#send initial string
RCxxSerial.WriteRead(ser,StartToken,"StartTok")
#send command
RCxxSerial.WriteRead(ser,"COPYTO","COPYTO")
#send drive
RCxxSerial.WriteRead(ser,drive,"Drive")

#Time the transfer
start = time.time()

#send filename and wait for OK
if b"OK" not in RCxxSerial.WriteRead(ser,filename,"Wait for OK") :#read OK
    print ("No OK returned")
    RCxxSerial.Close(ser) 
    sys.exit(1)
   
localfile = open(filepath, "rb")
while True:
    message_bytes = localfile.read(bufsize)
    if not message_bytes:
         if debug :print("EOM");
         break
    
    #txt=RCxxSerial.WriteRead(ser,"","Wait for OK:")
    #if b"OK" not in txt:
    #     print(" Not Rceived OK: ", txt)
    #     RCxxSerial.Close(ser)
    #     sys.exit(1)
    
    txt=RCxxSerial.ReadOnly(ser,"Wait for ChunkSize:")
    #txt=RCxxSerial.WriteRead(ser,"","Wait for ChunkSize:")
    if b"Chunk" not in txt:
         print(" Not Rceived Chunksize: ", txt)
         RCxxSerial.Close(ser)
         sys.exit(1)
   
    #send chunk size
    if debug :print("sending chunk ",str(len(message_bytes)) )
    txt=RCxxSerial.WriteRead(ser,str(len(message_bytes)),"Chunk")
    if b"Data" not in txt:
         print(" Not Rceived Data: ", txt)
         RCxxSerial.Close(ser)
         sys.exit(1)
         
    totalsize+=len(message_bytes)
    print(".", end='',flush=True)
    
    b64ls=base64.b64encode(message_bytes)
    if debug :print("send base64\n")
    txt=RCxxSerial.WriteRead(ser,b64ls,"b64",1)
    if b"OK" not in txt:
         print(" Not Received OK ", txt)
         RCxxSerial.Close(ser)
         sys.exit(1)
      
time.sleep(0.1)   
   
localfile.close()
print("")

#send zero chunk
if debug :print("send zero Chunk");

#ReadOnly()
txt=RCxxSerial.WriteRead(ser,"0","0")
if b"OK" not in txt :
    print ("No OK returned on last chunk ",txt)
    RCxxSerial.Close(ser) 
    sys.exit(1)
   
end = time.time()
RCxxSerial.Close(ser)           # close port

print (filepath+" Sent")
bps=totalsize/(end-start)
print("%d Bytes in %0.3f Seconds, %0.0f B/s (%0.3f Z/s) " %(totalsize,end-start,bps,bps/zork))
      





