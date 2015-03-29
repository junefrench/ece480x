# Homework 2

John French

## 1

> Problem 2.11 from the book.
>> We want to perform an attack on another LFSR-based stream cipher. In order to process letters, each of the 26 uppercase letters and the numbers 0, 1, 2, 3, 4, 5 are represented by a 5-bit vector according to the following mapping:
>>
>> ```
>> A <-> 0  = 0b00000
>> ...
>> Z <-> 25 = 0b11001
>> 0 <-> 26 = 0b11010
>> ...
>> 5 <-> 31 = 0b11111
>> ```
>>
>> We happen to know the following facts about the system:
>>
>> * The degree of the LFSR is `m = 6`.
>> * Every message starts with the header `WPI`.
>>
>> We observe now on the channel the following message: `j5a0edj2b`

### a

>> What is the initialization vector?

We can determine the beginning of the keystream by XORing the known partial plaintext `wpi` with the cyphertext:

```
Plaintext:  {-w-}{-p-}{-i-}{-?-}{-?-}{-?-}{-?-}{-?-}{-?-}
            101100111101000??????????????????????????????
Cyphertext: {-J-}{-5-}{-A-}{-0-}{-E-}{-D-}{-J-}{-2-}{-B-}
            010011111100000110100010000011010011110000001
Keystream:  {-5-}{-Q-}{-I-}{-?-}{-?-}{-?-}{-?-}{-?-}{-?-}
            111111000001000??????????????????????????????
```

The initialization vector is the first `m` bytes of the keystream, so `111111`.

### b

>> What are the feedback coefficients of the LFSR?

The feedback to the LFSR for each clock tick is:
```
t = 0: 111111 -> 0
t = 1: 011111 -> 0
t = 2: 001111 -> 0
t = 3: 000111 -> 0
t = 4: 000011 -> 0
t = 5: 000001 -> 1
t = 6: 100000 -> 0
t = 7: 010000 -> 0
t = 8: 001000 -> ?
```

One bit changes in the input each tick from `t = 1` to `t = 4`. The bit which changes for each tick `t` is the bit `x[t - 1]`. Because the feedback bit does not change for any of these steps we know that `x[0]` through `x[3]` all have coefficients of 0. On `t = 5` the bit `x[4]` changes, as does the feedback, so this bit has a coefficient of 1. On `t = 6` the bits `x[0]` and `x[5]` both change, as does the feedback. We already know that `x[0]` has a coefficient of 0 so `x[5]` must have a coefficient of 1. On `t = 7` the bits `x[0]` and `x[1]` change, and the feedback does not, as expected (since we know they both have coefficients of 0).

Now we know the coefficients of each bit, but we still need the constant. When all bits are 1, the output is 0 (at `t = 0`). There are two bits with coefficients of 1, so the feedback will be 0 if the constant term is 0. The polynomial is therefore `0&x[0] ^ 0&x[1] ^ 0&x[2] ^ 0&x[3] ^ 1&x[4] ^ 1&x[5] ^ 0`.

### c

>> Write a program in your favorite programming language which generates the whole sequence, and find the whole plaintext.

The program can be found in `lfsr.py`. The plaintext is `wpiwombat`.

### d

>> Where does the thing after `WPI` live?

Australia

### e

>> What type of attack did we perform?

A known-plaintext attack

## 2

> Problem 3.6 from the book.
>> An avalanche effect is also desirable for the key: A one-bit change in a key should result in a dramatically different ciphertext if the plaintext is unchanged.

### a

>> Assume an encryption with a given key. Now assume the key bit at position 1 is being flipped. Which S-boxes in which rounds are affected by the bit flip during DES encryption?

TODO

### b

>> Which S-boxes in which rounds are affected by this bit flip during DES decryption?

TODO

## 3

TODO

## 4

> Implement an exhaustive key search for DES. Recover the key for the following plaintext-ciphertext pair (both given in hex notation):
>
> ```
> pt = 48656c6c6f212121
> ct = 1f6339383e8da6c4
> ```
> 
> Please turn in your working code together with the correct 64-bit representation of the key.
>
> Note: while the key space of DES is way too small by now, it is still too large to be searched in reasonable time on a simple desktop PC. In order to facilitate the search, the first four bytes of the 64-bit key have been fixed to 0. i.e. the 64-bit key looks like this (in hex representation): `00000000XXXXXXXX`.

A python implementation is in `desbf.py`. I ran it thus: `./desbf.py 48656c6c6f212121 1f6339383e8da6c4 -k "00000000????????" -j 24`. This produced the result `00000000c0feee22`, or, taking into account parity bits, `00000000c0ffee22`.

## Bonus

> Recover the DES key for the following plaintext-ciphertext pair (both given in hex notation):
>
> ```
> pt = 48656c6c6f212121
> ct = ddb92846141922b8
> ```
>
> The key starts with zeros, just as the one before (but less). Please turn in your working code together with the correct 64-bit representation of the key and the runtime needed.

The key is `00000ceaf4c0feee` (or, flipping some parity bits to make more sense, `00000deaf4c0ffee`). The code used is in `desbf.c`. It implements basically the same algorithm as the python version from problem 4, but is much faster. Build with `./make.sh`. The command I used was `./desbf 48656c6c6f212121 ddb92846141922b8 24`. It took just under an hour and a half with 24 threads on `fourbanger.wpi.edu`.
