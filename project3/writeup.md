# Homework 3

John French

## 1

> Consider a modified substitution-permutation network where instead of car- rying out the key-mixing, substitution, and permutation steps in alternating order for `r` rounds, the cipher instead first applies `r` rounds of key-mixing, then carries out `r` rounds of substitution, and finally applies `r` permutations. Analyze the security of this construction.

This would effectively be equivalent to a single round of mixing, substitution, and permutation. Multiple stages of any one operation without performing the other operations in between is effectively like doing one (somewhat different) stage of the operation. For instance if you have a given substitution and you perform it multiple times in a row without doing anything else in between, this is really the same as doing a single (different) substitution.

## 2

> A small company has developed a messaging application that allows to send text messages between two parties. The transferred messages `m` are encoded in the ASCII format, i.e., each symbol `m[i]` of the message `M = m[0] m[1] ... m[l]` (be it a letter, a number, or other symbol) is represented by a string of 7 bits, i.e., `|m[i]| = 7 bit`.
>
> At some point the company decides to add security to the application by encrypting the transferred messages. For this, sender and receiver share a secret key `v` via a secure channel. The company decides to use the highly secure AES-256 encryption scheme for marketing reasons. The implemented encryp- tion scheme takes each symbol `m[i]` and encrypts it separately. Missing input bits are padded with zeros. The resulting encryption scheme is:
>
> ```
> c[i] = AES[k](m[i]||000...)
> C = c[0] c[1] ... c[l]
> ```

### a

> Is this encryption scheme secure? How many different ciphertext symbols does this scheme produce? Describe an efficient attack against this encryption scheme. What does an adversary need to successfully perform your attack?

No, it is not secure. Because each symbol in the plaintext is encrypted independently, this scheme is in effect a substitution cypher, and can be attacked in the same way (by guessing substitutions with the help of frequency analysis, known or guessed plaintext/cyphertext pairs, etc.) Using frequency analysis, this would allow an attacker to decrypt a conversation as long as they had a sufficiently long cyphertext.

### b

> Does your attack recover the secret key? What is the attack complexity to recover the secret key?

No, it does not. Recovering the secret key would require an exhaustive keyspace search, so the complexity is 2^256 AES decryption operations.

### c

> The company asks you to improve the employed encryption scheme. Unfortunately you may not change the main protocol (the product is in use and being advertised as highly secure AES-based messenger). Each symbol `m[i]` still has to be encrypted separately.
>
> Replace the zero padding of the encryption scheme described above with a new padding scheme that restores the secrecy requirement. Which essential property do you need to add to the encryption scheme?

To make the scheme secure, replace the padding with a counter, effectively using AES in CTR mode. The encryption algorithm becomes:

```
c[i] = AES[k](m[i]||i)
C = c[0] c[1] ... c[l]
```

This still has a flaw: identical plaintexts will produce identical cyphertexts. This could be resolved by XORing the counter with a randomly-chosen nonce. The randomly-chosen nonce would, however, need to be included in the message; this would require a change to the protocol beyond simply changing the padding.

## 3

> The goal of this problem is to encrypt the payload of a `.bmp` file using three different modes of operation. The cipher to be used is AES. As in the last project, please use a preexisting AES implementation for this project.
>
> Please write code to encrypt the payload of `gompei.bmp` using AES in electronic codebook (ECB) mode, cipher block chaining (CBC) mode, and counter (CTR) mode of operation. Submit the code in each case together with the encrypted file. The key (and initialization vector (IV)) should be all-zero.

The code for all three cases is in `bmpenc.py`. It expects a file `gompei.bmp` in the working directory and outputs encrypted versions of it for each mode. They are also included.
