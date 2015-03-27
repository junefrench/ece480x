# Homework 2

John French

## 1

> Problem 2.11 from the book.
>> We want to perform an attack on another LFSR-based stream cipher.
>> In order to process letters, each of the 26 uppercase letters and the numbers 0, 1, 2, 3, 4, 5 are represented by a 5-bit vector according to the following mapping:
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

One bit changes in the input each tick from `t = 1` to `t = 4`.
The bit which changes for each tick `t` is the bit `x[t - 1]`.
Because the feedback bit does not change for any of these steps we know that `x[0]` through `x[3]` all have coefficients of 0.
On `t = 5` the bit `x[4]` changes, as does the feedback, so this bit has a coefficient of 1.
On `t = 6` the bits `x[0]` and `x[5]` both change, as does the feedback.
We already know that `x[0]` has a coefficient of 0 so `x[5]` must have a coefficient of 1.
On `t = 7` the bits `x[0]` and `x[1]` change, and the feedback does not, as expected (since we know they both have coefficients of 0).

Now we know the coefficients of each bit, but we still need the constant.
When all bits are 1, the output is 0 (at `t = 0`).
There are two bits with coefficients of 1, so the feedback will be 0 if the constant term is 0.
The polynomial is therefore `0&x[0] ^ 0&x[1] ^ 0&x[2] ^ 0&x[3] ^ 1&x[4] ^ 1&x[5] ^ 0`.

### c

>> Write a program in your favorite programming language which generates the whole sequence, and find the whole plaintext.

The program can be found in `lfsr.py`.
The plaintext is `wpiwombat`.

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

>> Assume an encryption with a given key.
>> Now assume the key bit at position 1 is being flipped.
>> Which S-boxes in which rounds are affected by the bit flip during DES encryption?

TODO

### b

>> Which S-boxes in which rounds are affected by this bit flip during DES decryption?

TODO

## 3

TODO

## 4


