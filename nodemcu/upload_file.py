import serial
import sys
import os

if len(sys.argv) < 2:
    print "Usage: %s filename" % sys.argv[0]
    exit(1)

if os.path.exists(sys.argv[1]) is False:
    print "File %s doesn't exist" % sys.argv[1]
    exit(1)

ser = serial.Serial('/dev/ttyUSB0',baudrate=9600)
ser.timeout = 1
upload_file = open(sys.argv[1],'r')
print "Opened file %s" % sys.argv[1]

lines = upload_file.readlines()
for line in lines:
    print "writing to esp : %s " %  line
    ser.write(chr(10))
    ser.write(line + chr(10))
    res = ser.read(1024)
    print "got from esp : %s " % res
upload_file.close()
