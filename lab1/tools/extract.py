# uncompyle6 version 3.2.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.0 (default, Sep 15 2018, 19:13:07) 
# [GCC 8.2.1 20180831]
# Embedded file name: csfsteg/csfsteghide.py
# Compiled at: 2018-10-13 11:57:39
import sys, struct, numpy, PIL as pillow
from PIL import Image

def decompose(data):
    v = []
    fSize = len(data)
    bytes = [ ord(b) for b in struct.pack('i', fSize) ]
    bytes += [ ord(b) for b in data ]
    for b in bytes:
      for i in range(7, -1, -1):
        v.append(b >> i & 1)
    return v

def compose(databits):
    ret = ""
    for b in range(0,len(databits),8):
      word = 0
      k = 0
      for i in range(7, -1, -1):
        if (b+k<len(databits)):
          word = set_bit(word, i, databits[b+k])
        k+=1
      ret += chr(word)
    return ret


def set_bit(n, i, x):
    mask = 1 << i
    n &= ~mask
    if x:
        n |= mask
    return n

def get_bit(n, i):
    mask = 1 << i
    return (n & mask) != 0


def unembed(imgFile, password):
    img = Image.open(imgFile)
    width, height = img.size
    conv = img.convert('RGBA').getdata()
    print '[*] Input image size: %dx%d pixels.' % (width, height)
    max_size = width * height * 3.0 / 8 / 1024

    steg_img = Image.new('RGBA', (width, height))
    data_img = steg_img.getdata()
    idx = 0
    displacement = 0
    databits = []
    for h in range(height):
        for w in range(width):
            if displacement < password:
                displacement = displacement + 1
                continue
            r, g, b, a = conv.getpixel((w, h))
            databits += [get_bit(r, 0)]
            databits += [get_bit(r, 1)]
            databits += [get_bit(g, 0)]
            databits += [get_bit(g, 1)]
            databits += [get_bit(b, 0)]
            databits += [get_bit(b, 1)]
            idx = idx + 6

    data = compose(databits)
    calclen = struct.unpack('i', data[0:4])
    print calclen
    with open(imgFile + "." + str(password) + ".extracted", "w") as f:
      f.write(data[4:4+calclen[0]])
    print '[+] %s extracted successfully!' % "output"


def usage(progName):
    print 'Ciber Securanca Forense - Instituto Superior Tecnico / Universidade Lisboa'
    print 'LSB steganography tool: unhide files within least significant bits of images.\n'
    print ''
    print 'Usage:'
    print '  %s <img_file> [password]' % progName
    print ''
    print '  The password is a number and must be a number.'
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])
    password = int(sys.argv[2]) % 13 if len(sys.argv) == 3 else 0
    unembed(sys.argv[1], password)
# okay decompiling compress.pyo
