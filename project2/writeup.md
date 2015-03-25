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

## a

>> What is the initialization vector?

We can determine the beginning of the keystring from the header `WPI` and the cyphertext:

```
Plaintext:  {-w-}{-p-}{-i-}{-?-}{-?-}{-?-}{-?-}{-?-}{-?-}
            101100111101000??????????????????????????????
Cyphertext: {-J-}{-5-}{-A-}{-0-}{-E-}{-D-}{-J-}{-2-}{-B-}
            010011111100000110100010000011010011110000001
Keystream:  {-5-}{-Q-}{-I-}{-?-}{-?-}{-?-}{-?-}{-?-}{-?-}
            111111000001000??????????????????????????????
```

The initialization vector is the first `m` bytes of the keystream, so `111111`.

## b

>> What are the feedback coefficients of the LFSR?

## c

>> Write a program in your favorite programming language which generates the whole sequence, and find the whole plaintext.

## d

>> Where does the thing after `WPI` live?

## e

>> What type of attack did we perform?

