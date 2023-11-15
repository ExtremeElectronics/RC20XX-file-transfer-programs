
import RCxxSerial

def chk(filename):
  print(filename,RCxxSerial.CheckFilename(filename))

chk("HELLO")
chk("HI.THERE")
chk("")
chk("AAA.ZZZ")
chk("TOOLONGFILE.txt")
chk("aaa.zzz")
chk("text.")
chk(".fal")
chk("ZZZZZZZZ.ZZZ")
chk("A.A")
chk("TEST.001")
chk("1456.789")
chk(" ")
chk("   .   ")
chk("dot.dot.dot")
chk("help.tx")
chk("TEST.t@T")
chk("File!.TXT")


        
        
