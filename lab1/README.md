How files where extracted:


mechanism 1: stego images of compress.pyo
1) Uncompyle compress.py
2) Create tool to decompress compressed images and brute force 13 possible passwords
3) Run tool on every file

We extracted:
  oktoberfest.png.0.extracted
  street.png.0.extracted
  wursten.png.0.extracted

After running again on street.png.0.extracted:
  street.png.0.extracted.0.extracted


snow.txt:
  There is text after the end of the bmp file.


zip password:
  1) generate wordlist from .txt file
  2) Here is johnny




Artifacts list:
md5sum | filename
74ead8bf19e3f12f131666fe3752b67e  compress.py
d99f500968d444b5e0a1c9fd1dd69274  drone-A.png
cbe4c039f3fa2b312bb95a0964ffba4d  oktoberfest.png.0.extracted
b70702822417bd39a7997a0f8c73941f  online_banking.docx
f8105917067d26e022ff6e657f6cd9d8  snow.txt
d770b66b4f5833b0be194362f440e494  street.png.0.extracted
3ba4ca7f05bbf65083360e455fa8ea8a  street.png.0.extracted.0.extracted
3cb3f3162e4cf990168d904d3bb300b9  wursten.png.0.extracted

sha1sum | filename
bf83e126c0166bce3d0526e0dfa0a74f5960f60f  compress.py
14099f30e4b2c894cff20a3fa498808f66e31780  drone-A.png
01ab4e16ed2b7b15c47aafc9b6a168a527a2218a  oktoberfest.png.0.extracted
8cf635ceba0334d0a1c018df676ad03fa06d817b  online_banking.docx
63515f910ad88b76950384fea470e5e3ccc3a38a  snow.txt
1b5d516a7a65da889a83c01adae7ea24d5955ac3  street.png.0.extracted
e0d5c932d2a7c13338d3cbb7ec5618066ca5a13c  street.png.0.extracted.0.extracted
7c241b5af909484f2004359ed697e9a68abf186f  wursten.png.0.extracted

size | filename
  2774 compress.py
 92401 drone-A.png
106674 oktoberfest.png.0.extracted
 22313 online_banking.docx
   145 snow.txt
169868 street.png.0.extracted
  1139 street.png.0.extracted.0.extracted
    80 wursten.png.0.extracted
