import serial
import sys
import os
import time

def write_lines(ser, lines):
    for line in lines:
        print "writing to esp : %s " %  line.strip()
        ser.write(line)
        ser.write(chr(10))
        
        res = ser.read(1024)
        while line.strip() not in res:
            res += ser.read(1024)
        
        #print "got from esp : %s " % res
    return res

if len(sys.argv) < 3:
    print "Usage: %s device filename" % sys.argv[0]
    exit(1)

if not os.path.exists(sys.argv[2]):
    print "File %s doesn't exist" % sys.argv[2]
    exit(1)

# TODO: add option to compile the file on ESP.
# TODO: Extract the baudrate as parameter => flash faster!
try:
    ser = serial.Serial(sys.argv[1], baudrate=9600)
    if not ser.isOpen():
        print "failed ser.open()"
        exit(1)
except:
    print "Port %s is locked. Can't open it." % sys.argv[1]
    exit(1)

print sys.argv[1], "port is opened successfully."
ser.timeout = 0.5
upload_file = open(sys.argv[2], 'r')

filename = sys.argv[2]
# TODO: Find elegant method to split with regex
if "\\" in filename: filename = filename.split('\\')[-1]
if "/" in filename: filename = filename.split('/')[-1]
print "Saving to esp:", filename

# Prepare to upload.
prelines = [('file.open("%s", "w+")' % filename) + chr(10), 'w = file.writeline' + chr(10)]
postlines = ['file.close()' + chr(10)]
lines = upload_file.readlines()
lines = [r"w([[" + line.strip() + r"]])" + chr(10) for line in lines]

# Upload + write to flash
write_lines(ser, prelines)
write_lines(ser, lines)
write_lines(ser, postlines)

upload_file.close()

print "Verify written file by read."
lines = ['l = file.list()',
    'for k,v in pairs(l) do if k == "%s" then print("name:", k, ", size:", v) end end' % filename,
]
res = write_lines(ser, lines).split('\n')

# Report results
print "-"*50
res = [i for i in res if "name" in i]
if res:
    print "\nCompleted successfully:", res[1]
else:
    print "The file %s is not written." % filename
