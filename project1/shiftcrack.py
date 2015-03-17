#!/usr/bin/env python3

"""
Takes two arguments, first is cyphertext, second is (optional) shift
"""

import sys
ct = sys.argv[1].upper()
print("Cracking cyphertext \"" + ct + "\"")

import string
uc = string.ascii_uppercase

if len(sys.argv) == 3:
    shift = int(sys.argv[2])
else:
    counts = {char: 0 for char in uc}
    for char in ct:
        counts[char] += 1

    max = 0
    maxchar = None
    for char, count in counts.items():
        if count > max:
            max = count
            maxchar = char

    assert maxchar is not None

    print("Most frequent character in cyphertext is " + maxchar + ", assuming this is E")

    shift = uc.index('E') - uc.index(maxchar)
    print("Assuming shift of " + str(shift))

pt = ""
for char in ct:
    pt += uc[(uc.index(char) + shift) % len(uc)]

print("Plaintext: \"" + pt + "\"")

