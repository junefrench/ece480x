#!/usr/bin/env python3

# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to <http://unlicense.org/>

"""
Encrypt only the data in a bitmap file
"""

class Bmp:
    from struct import Struct
    _bmp_header = Struct('<2sIHHI')

    def __init__(self, bytes):
        self.header, size, self.res1, self.res2, self.image_offset = self._bmp_header.unpack_from(bytes)
        size -= self._bmp_header.size
        self.image_offset -= self._bmp_header.size
        self.data = bytes[self._bmp_header.size:]
        if self.header not in (b'BM', b'BA', b'CI', b'CP', b'IC', b'PT'):
            raise ValueError('File does not contain BMP data');

    def get_bytes(self):
        return self._bmp_header.pack(self.header, len(self.data) + self._bmp_header.size, self.res1, self.res2, self.image_offset + self._bmp_header.size) + self.data

from Crypto.Cipher import AES
from Crypto.Util import Counter

for mode, name in [(AES.MODE_ECB, 'ecb'), (AES.MODE_CBC, 'cbc'), (AES.MODE_CTR, 'ctr')]:
    with open('gompei.bmp', 'rb') as gompei:
        bmp = Bmp(gompei.read())

        key = b'0' * AES.block_size
        iv = key

        ctr = Counter.new(128)

        aes = AES.new(key, mode, iv, counter=ctr) if mode == AES.MODE_CTR else AES.new(key, mode, iv)

        bmp.data = bmp.data[:bmp.image_offset] + aes.encrypt(bmp.data[bmp.image_offset:])

        with open('gompei_' + name + '.bmp', 'wb') as out:
            out.write(bmp.get_bytes())
