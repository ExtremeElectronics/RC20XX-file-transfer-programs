import os
import time
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [PORT] [DRIVE] [filepath]...",
        description="Copy Local Directory to drive on RC20XX."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-debug', help="Set Debug",action='store_true')
    
    parser.add_argument('port', help="Com or TTY port with an RC20XX attached")
    parser.add_argument('drive', help="CPM Drive on the Attached RC20XX")
    parser.add_argument('path', help="local directory with files to save on the Attached RC20XX")
    
    return parser

parser = init_argparse()
args = parser.parse_args()

debug=args.debug


serialport=args.port 
if serialport=="": serialport="COM1"

drive=args.drive.upper()
if drive=="": drive="A"

path=args.path
#filename=os.path.basename(filepath)
if debug: print(path)


def DoExec(cmd):
    stream = os.popen(cmd)
    output = stream.read()
    print(cmd)
    print(output)

db=" "
if debug:db=" -d "

for file in os.listdir(path):
  pathfile=os.path.join(path, file)
  if os.path.isfile(pathfile):
    cmd="python CopyTo-RC20xx.py " + serialport + db + drive + " " + pathfile
    DoExec(cmd ) 
    time.sleep(0.1)
  
