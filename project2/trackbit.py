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
Track changes in S-boxes from flipping bit 1 of a DES key
"""

rot_amt = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
p = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
e = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

def all_inds(l, e):
    for i in range(len(l)):
        if l[i] == e:
            yield i

half_index = 8 # PC-1 mapping of 1
last_round_sboxes = set()
for i in range(16):
    half_index -= rot_amt[i];
    if half_index == 0: half_index = 24; # basically mod 24 but we want to index from 1 for some stupid reason
    if half_index in pc2:
        subkey_index = pc2.index(half_index)
    else:
        subkey_index = None

    this_round_sboxes = set() # set of s-boxes which are 'dirty' this round (affected by the flipped bit)
    if subkey_index is not None:
        # if the flipped bit is in the subkey this round, add the s-box which gets that part of the subkey
        this_round_sboxes.add(subkey_index // 6)

    for sbox in last_round_sboxes:
        # compute which s-boxes are affected in this round by the output of each dirty s-box from last round
        for j in range(sbox * 4, (sbox + 1) * 4):
            p_ind = p.index(j + 1)
            e_inds = all_inds(e, p_ind + 1)
            for ind in e_inds:
                this_round_sboxes.add(ind // 6)
        
    print("Round {0:2}: << {1:2d}, L[{2:2}], K[{3:4}]".format(i + 1, rot_amt[i], half_index,'{0:4}'.format(subkey_index + 1) if subkey_index is not None else 'None')
            + (" -> S-Box {0},".format((subkey_index // 6) + 1) if subkey_index is not None else ',           ')
            + " Dirty: " + ', '.join(map(lambda s: 'S-Box {0}'.format(s + 1), this_round_sboxes)))
    last_round_sboxes = this_round_sboxes
