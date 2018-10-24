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