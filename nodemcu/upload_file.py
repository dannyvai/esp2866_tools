import serial
import sys
import os

if len(sys.argv) < 3:
    print "Usage: %s device filename" % sys.argv[0]
    exit(1)

if os.path.exists(sys.argv[2]) is False:
    print "File %s doesn't exist" % sys.argv[2]
    exit(1)

ser = serial.Serial(sys.argv[1],baudrate=9600)
ser.timeout = 0.01
upload_file = open(sys.argv[2],'r')


lines = upload_file.readlines()
for line in lines:
    print "writing to esp : %s " %  line
    ser.write(chr(10))
    ser.write(line + chr(10))
    res = ser.read(1024)
    while res == 0:
        res = ser.read(1024)
    print "got from esp : %s " % res

res = 0
while res == 0:
        res = ser.read(1024)

upload_file.close()
