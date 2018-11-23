from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long
import base64
import binascii
import sys

encoded_string = c = ""

if(len(sys.argv) != 2):
	print "python2 recover.py [file_path]"
	sys.exit(0)

with open(sys.argv[1], 'rb') as f:
    file = f.read()
    iv = file[:16]
    encrypted = file[16:]

key = binascii.unhexlify("47683b9a9663c065353437b35c5d8519")
counter = Counter.new(128, initial_value = bytes_to_long(iv))
cipher = AES.new(key, AES.MODE_CTR, counter = counter)
print cipher.decrypt(encrypted) 