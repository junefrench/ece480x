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
Implementation of the LFSR cypher from book problem 2.11
"""

def gen(token_bits = 5, degree=6, initial_vector=0b111111, coefficients=0b0000110):
    """
    LFSR keystream generator

    Parameters:
        degree: the number of terms in the LFSR
        initial_vector: an integer, the bits of which comprise the initial values of each term in the LFSR (the LSB will be the first bit yielded)
        coefficients: an integer, the bits of which comprise the coefficients of each term (where the LSB is the constant term)

    In other words, the feedback to the LFSR is computed as the XOR of all of the bits in ((vector << 1) | 1) & coefficients.

    Returns: a generator which yields ints corresponding to the tokens of the keystream
    """
    from gmpy import popcount
    x = initial_vector
    out_byte = 0
    out_ind = 0
    while True:
        out_byte |= (x & 1) << (token_bits - 1 - out_ind)
        out_ind = (out_ind + 1) % token_bits
        if out_ind == 0:
            yield out_byte
            out_byte = 0
        feedback = popcount(((x << 1) | 1) & coefficients) % 2
        x = (x >> 1) | (feedback << (degree - 1))

def enc(p, k):
    for pc, kc in zip(p, k):
        yield pc ^ kc

def dec(c, k):
    return enc(c, k)  # decryption is the same algorithm as encryption, just xor

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Encrypt or decrypt messages with an LFSR")
    parser.add_argument('command', choices=['encrypt', 'decrypt'], help='The operation to perform')
    parser.add_argument('text', help='The plaintext to encrypt or cyphertext to decrypt')
    args = parser.parse_args()

    def encode(t):
        from string import ascii_uppercase
        for c in t:
            if c in ascii_uppercase:
                yield ord(c) - ord('A')
            elif c in '012345':
                yield ord(c) - ord('0') + 26
            else:
                raise ValueError()

    def decode(e):
        for c in e:
            if c < 26:
                yield chr(ord('A') + c)
            elif c < 32:
                yield chr(ord('0') + c - 26)

    if args.command == 'encrypt':
        print(''.join(decode(enc(encode(args.text.upper()), gen()))))
    elif args.command == 'decrypt':
        print(''.join(decode(dec(encode(args.text.upper()), gen()))).lower())

