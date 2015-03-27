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
Brute-forcer for DES
"""

class Keyspace:
    def __init__(self, key, mask):
        self._key = key & ~mask # ensure all masked bits are 0 in _key
        self._mask = mask
        from gmpy import popcount
        self._len = 1<<popcount(mask)
        self._blocks = []
        mask_bits = bin(mask)[::-1][:-2]
        start = None
        for i in range(len(mask_bits) + 1):
            if i < len(mask_bits) and mask_bits[i] == '1':
                if start is None:
                    start = i
            else:
                if start is not None:
                    self._blocks.append((start, i))
                    start = None

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __getitem__(self, i):
        k = self._key
        for start, end in self._blocks:
            k |= (i & ((1 << end) - 1)) << start
            i >>= end - start
        #import binascii
        #import struct
        #print(binascii.hexlify(struct.pack('>Q', k)))
        return k

    def __len__(self):
        return self._len

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Brute-force a DES key given a known plaintext")
    parser.add_argument('plaintext', help='The plaintext of the known message, hex-encoded')
    parser.add_argument('cyphertext', help='The cyphertext of the known message, hex-encoded')
    parser.add_argument('-k', '--key', help='The key, hex-encoded, with unknown digits replaced by ?')
    parser.add_argument('-j', '--jobs', help='The number of processes to spawn')
    args = parser.parse_args()

    import binascii
    pt = binascii.unhexlify(args.plaintext)
    ct = binascii.unhexlify(args.cyphertext)
    
    if args.key is None:
        key = 0x0
        mask = 0xffffffffffffffff
    else:
        import re
        key = int(args.key.replace('?', '0'), 16)
        mask = int(re.sub(r'[^\?]', '0', args.key).replace('?', 'F'), 16)
        mask &= ~0x0101010101010101 # unmask parity bits to reduce keyspace a bit more
        key &= ~0x0101010101010101 # replace parity bits with 0 in key

    keyspace = Keyspace(key, mask)

    from Crypto.Cipher import DES
    import struct

    chunk_size = 1<<16
    nchunks = len(keyspace) // chunk_size
    if len(keyspace) % chunk_size != 0:
        nchunks += 1

    def check(i):
        for i in range(chunk_size * i, min(chunk_size * (i + 1), len(keyspace))):
            k = keyspace[i]
            if DES.new(struct.pack('>Q', k)).encrypt(pt) == ct:
                return k

    if args.jobs is None:
        results = map(check, range(nchunks))
    else:
        from multiprocessing import Pool
        results = Pool(int(args.jobs)).imap_unordered(check, range(nchunks))

    from sys import exit
    for result in results:
        if result is not None:
                print(binascii.hexlify(struct.pack('>Q', result)).decode('ascii'))
                exit(0)
    print("No solution")
    exit(1)

