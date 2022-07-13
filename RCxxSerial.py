import serial
import io
import time
import sys

debug=0;
crlf='\n';

       
def WriteCrLf(ser):
    ser.write((crlf).encode('utf_8')) # write a string


def ReadOnly(ser,dbt):
    if debug : print("Read ",dbt);
    ReadText = ser.readline() # read a string
    if(len(ReadText)==0):
      print ("Timeout")
      ser.close()             # close port
      sys.exit(1)
      
    if debug : print("<",ReadText.decode('ascii','ignore')) 
    return ReadText


def WriteRead(ser,text,dbt,binary=0):
    if debug : print("Write ",dbt)
    ser.flushInput()
    #ser.write((text+crlf).encode('utf_8')) # write a string
    
    if(binary==0):
      ser.write((text+crlf).encode('utf_8')) # write a string
    else:
      ser.write(text+crlf.encode('utf_8')) # write a string  
      
    ReadText = ser.readline() # read a string
    if(len(ReadText)==0):
      print ("Timeout ",dbt)
      ser.close()             # close port
      sys.exit(1)
      
    if debug : print("<",ReadText.decode("ascii",'ignore')) 
    return ReadText
    
    
def WriteOnly(ser,text,dbt,binary=0):
    if debug : print("Write ",dbt)
    ser.flushInput()
    if(binary==0):
      ser.write((text+crlf).encode('utf_8')) # write a string
    else:
      ser.write(text+crlf.encode('utf_8')) # write a string  
      
   
def FlushOutput(ser):
    ser.flushOutput()
    
def FlushInput(ser):
    ser.flushInput()

def OpenSerial(serialport,speed):
    try:
        ser = serial.Serial(serialport, speed, timeout=5)  # open serial port
    except serial.SerialException as e:
        print ("Cant open serial port ",serialport,e)
        sys.exit(1)
    #sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),newline = '\n',line_buffering = True)    
    return ser
        
def InitSerial(ser):
    ser.write(("0"+crlf+"##"+crlf).encode('utf_8'))       #scrap previous waiting commands
    ser.write(("0"+crlf+"##"+crlf).encode('utf_8'))       #scrap previous waiting commands
                        
    if debug : print(ser.name)         # check which port was really used
    
    FlushOutput(ser)
    WriteCrLf(ser)
    WriteCrLf(ser)
    time.sleep(0.1)
    FlushInput(ser)
    time.sleep(0.1)
    
    return ser
    
def Close(ser):
    ser.close()
    
    
