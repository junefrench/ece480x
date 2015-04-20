# Project 4

John French

## 1

> 8.4
>> In this exercise we want to identify primitive elements (generators) of a multiplicative group since they play a big role in the DHKE and and many other publickey schemes based on the DL problem. You are given a prime `p = 4969` and the corresponding multiplicative group `Z∗[4969]`.

## a

>> Determine how many generators exist in `Z*[4969]`.

`Z*[4969]` is a finite cyclic group because 4969 is prime (theorem 8.2.2). The number of generators (primitive elements) in this group is `totient(|Z*[4969]|)` (theorem 8.2.4). `|Z*[4969]|` is 4968, because since 4969 is prime, all integers `0..4969-1` are coprime with 4969 and therefore in the group, except for 0. `totient(4968)` is 1584 (computed with `totient.py`). So, there are 1584 generators.

## b

>> What is the probability of a randomly chosen element in `Z∗[4969]` being a generator?

The number of generators over the number of elements is 1584/4968 which reduces to 22/69.

## c

>> Determine the smallest generator `a` in `Z*[4969]` with `a > 1000`.

1005 (using `find_generator.py`).
