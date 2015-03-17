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
Cracks a substitution cypher using character frequencies
Takes one argument, the file which contains the cyphertext
"""

RED = '\033[31m'
GREEN = '\033[32m'
END = '\033[0m'

def replace_all(string, replacements):
    rstring = ""

    for char in string:
        if char in replacements:
            rstring += replacements[char]
        else:
            rstring += char

    return rstring

import sys
with open(sys.argv[1].upper(), 'r') as ct_f:
    ct = ct_f.read()
    import string
    uc = string.ascii_uppercase

    counts = {}
    for char in ct:
        if char in uc:
            if char in counts:
                counts[char] += 1
            else:
                counts[char] = 0

#    print('Letter | Count')
#    print('------ | -----')
#    for char in uc:
#        print(char.ljust(6) + ' | ' + str(counts[char]).ljust(4))

    english_freq = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    ct_freq = ''.join(sorted(counts, key=lambda char: counts[char], reverse=True))

#    substitutions = {a: b for a, b in zip(ct_freq, english_freq)}
#
#    pt = ""
#    for char in ct:
#        if char in uc:
#            pt += substitutions[char]
#        else:
#            pt += char
    char_options = ct_freq
    replace_options = english_freq
    replacements = {}

    print(ct)

    while len(char_options) > 0:
        print("Add a [S]ubstitution, [R]emove a substitution, or [L]ist subsitutions?")
        choice = input('>').upper()
        if choice == 'S':
            print("Replace which letter next?")
            print("Available characters, in order of frequency in cyphertext, are:")
            print(char_options)
            char = input('s/').upper()
            if len(char) != 1 or char not in char_options:
                print("Invalid choice.")
                continue
            char_options = char_options.replace(char, '')

            partial = ct.replace(char, RED + char + END)
            partial = replace_all(partial, {a: GREEN + b + END for a, b in replacements.items()})
            print(partial)
            print("Replace " + char + " with what?")
            print("Available characters, in order of frequency in English, are:")
            print(replace_options)

            replace_char = input('s/' + char + '/').upper()
            if len(replace_char) != 1 or replace_char not in replace_options:
                print("Invalid choice.")
                continue
            replace_options = replace_options.replace(replace_char, '')
            replacements[char] = replace_char
            partial = replace_all(ct, {a: GREEN + b + END for a, b in replacements.items()})
            print(partial)
        elif choice == 'R':
            print("Remove which replacement? Options are:")
            print(''.join(replacements.keys()))
            char = input('>').upper()
            if len(char) != 1 or char not in replacements:
                print("Invalid choice.")
                continue
            del replacements[char]
            char_options = ct_freq
            replace_options = english_freq
            for a, b in replacements.items():
                char_options = char_options.replace(a, '')
                replace_options = replace_options.replace(b, '')
            partial = replace_all(ct, {a: GREEN + b + END for a, b in replacements.items()})
            print(partial)

        elif choice == 'L':
            print(replacements)
        else:
            print("Invalid choice.")
