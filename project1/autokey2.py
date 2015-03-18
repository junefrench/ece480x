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

from string import ascii_uppercase
import itertools

"""
Implementation of Vigenere's Cyphertext-Autokey Cypher
"""

def gen(keyword, cyphertext, tokens=ascii_uppercase):
    def check(token):
        if token not in tokens:
            raise ValueError()
        return token
    return map(check, itertools.chain(keyword, cyphertext))

def enc(keyword, plaintext, tokens=ascii_uppercase):
    cyphertext = []
    key = gen(keyword, cyphertext, tokens=tokens)
    def enc_token(key_token, plain_token):
        if plain_token not in tokens:
            raise ValueError()
        cypher_token = tokens[(tokens.index(key_token) + tokens.index(plain_token)) % len(tokens)]
        cyphertext.append(cypher_token) # for the key generator
        return cypher_token
    return map(enc_token, key, plaintext)

def dec(keyword, cyphertext, tokens=ascii_uppercase):
    key = gen(keyword, cyphertext, tokens=tokens)
    def dec_token(key_token, cypher_token, tokens=tokens):
        if cypher_token not in tokens:
            raise ValueError()
        return tokens[(tokens.index(cypher_token) - tokens.index(key_token)) % len(tokens)]
    return map(dec_token, key, cyphertext)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Encrypt or decrypt messages with Vigenere's autokey cypher.")
    parser.add_argument('command', choices=['encrypt', 'decrypt'], help='The operation to perform')
    parser.add_argument('keyword', help='The keyword to use for key generation')
    parser.add_argument('text', help='The plaintext to encrypt or cyphertext to decrypt')
    args = parser.parse_args()

    if args.command == 'encrypt':
        print(''.join(enc(args.keyword.upper(), args.text.upper())))
    elif args.command == 'decrypt':
        print(''.join(dec(args.keyword.upper(), args.text.upper())))
