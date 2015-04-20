# Homework 4

John French

## 1

> 12.4

>> We will now discuss some issues when constructing an efficient MAC.

### a

>> The messages `X` to be authenticated consists of `z` independant blocks, so that `X = x[1]||x[2]||...||x[z]`, where every `x[i]` consists of 8 bits. The input blocks are consecutively put into the compression function:
>>
>> ```
>> c[i] = h(c[i-1], x[i]) = c[i-1] XOR x[i]
>> ```
>>
>> At the end, the MAC value
>>
>> ```
>> MAC[k](X) = c[z] + k mod 2^8
>> ```
>>
>> is calculated, where `k` is a 64-bit long shared key. Describe how exactly the (effective part of the) key `k` can be calculated with only one known message `X`.

The compression function basically computes the XOR of all of the blocks together. The effective part of `k` (that is, the value of `k mod 2^8`) can thus be found by simply subtracting the MAC from the compressed hash.

### b

>> Perform this attack for the following parameters and determine the key `k`:
>>
>> ```
>> X = 'HELLO ALICE!'
>> c[0] = 0b11111111
>> MAC[k](X) = 0b10011101
>> ```

First we compute the hash of X:

```python3
#!/usr/bin/env python3
X = b'HELLO ALICE!'
c = 0b11111111
for x in X:
	c ^= x
print(bin(c))	
```

This yields `0b11111110`. We subtract the MAC with this, and get `k = 0b11100001`.

### c

>> What is the effective key length of `k`?

8 bits.

### d

>> ALthough two different operations (XOR and + in the 2^8 ring) are utilized in this MAC, this MAC-based signature possesses significant weaknesses. To which property of the design can these be ascribed, and where should one take care when con- structing a cryptographic system? This essential property also applies for block ciphers and hash functions!

It does not have preimage resistance (specifically, you can recover the key from the plaintext and the cyphertext).

## 2

> Block ciphers can be turned into hash functions in a very simple way (cf. Section 11.3.2 of the book for a detailed explanation). One such construction is the Matyas-Meyer-Oseas construction defined as:
>
> ```
> H[i] = Enc[H[i-1]](m[i]) XOR m[i]
> ```
>
> Where `m[i]` is the `i`th block of the message, `H[i]` is the internal state of the hash function, and the output `h(m) = H[l]` is the last state of the hash function. This construction is considered secure for an appropriate block cypher.
>
> A slight modification of the Matyas-Meyer-Oseas mode results in the following construction:
>
> ```
> H[i] = Enc[H[i-1]](m[i])
> ```

### a

> Draw the block diagram for both constructions.

Matyas-Meyer-Oseas:

```
           m[i]
            |-----
            v    |
H[i-1] --> Enc   |
            |    |
            v    |
           XOR <--
            |
            v
           H[i]
```

Modified construction:

```
           m[i]
            |
            v
H[i-1] --> Enc
            |
            v
           H[i]
```

### b

> Show why the modified construction is not secure by using the decryption function of the block cipher to obtain a collision. Assume `H[0]` is all-zeros.

It is simple to get a collision for a given hash `h` by computing `Dec[0](h)` and using this as `H[1]`.

## 3

> The goal of this problem is to implement CBC-MAC yourself using a preexisting implementation of AES.

### a

> Your implementation should accept inputs of arbitrary length in bytes. Make sure to provide a single-1 padding (a single 1 followed by zeroes) combined with length strengthening where the length in bits is appended as a 64-bit number.
