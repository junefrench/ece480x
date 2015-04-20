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

# 2

> Implement the square and multiply algorithm using a computer language of your choice. The program should print all intermediate results.
>
> Compute the following exponentiations of `a^e mod p` using your program:
> ```
> a = 235973, e = 456789, p = 583903` 
> a = 984327457683, e = 2153489582, p = 994348472629
> ```

My program (see `square_and_multiply.py`) gives 418744 and 331688688384 respectively, the same as the built-in function `pow` in python. The output is:

```
(sqm) computing 235973^456789 % 583903
(sqm iteration) computing (1 * 235973^456789) % 583903
(sqm iteration) computing (235973 * 514940^228394) % 583903
(sqm iteration) computing (235973 * 5434^114197) % 583903
(sqm iteration) computing (26294 * 333206^57098) % 583903
(sqm iteration) computing (26294 * 2501^28549) % 583903
(sqm iteration) computing (364158 * 415971^14274) % 583903
(sqm iteration) computing (364158 * 393433^7137) % 583903
(sqm iteration) computing (79207 * 343607^3568) % 583903
(sqm iteration) computing (79207 * 583849^1784) % 583903
(sqm iteration) computing (79207 * 2916^892) % 583903
(sqm iteration) computing (79207 * 328414^446) % 583903
(sqm iteration) computing (79207 * 112751^223) % 583903
(sqm iteration) computing (455975 * 51885^111) % 583903
(sqm iteration) computing (265024 * 260395^55) % 583903
(sqm iteration) computing (12813 * 404053^27) % 583903
(sqm iteration) computing (247091 * 131912^13) % 583904
(sqm iteration) computing (218629 * 466344^6) % 583903
(sqm iteration) computing (218629 * 302277^3) % 583903
(sqm iteration) computing (376693 * 491580^1) % 583903
(sqm) 235973^456789 % 583903 = 418744
(sqm) computing 984327457683^2153489582 % 994348472629
(sqm iteration) computing (1 * 984327457683^2153489582) % 994348472629
(sqm iteration) computing (1 * 751837619932^1076744791) % 994348472629
(sqm iteration) computing (751837619932 * 133647923556^538372395) % 994348472629
(sqm iteration) computing (630996993289 * 702432827587^269186197) % 994348472629
(sqm iteration) computing (981214015219 * 408284410699^134593098) % 994348472629
(sqm iteration) computing (981214015219 * 518938198018^67296549) % 994348472629
(sqm iteration) computing (466407490241 * 805940334697^33648274) % 994348472629
(sqm iteration) computing (466407490241 * 194448987220^16824137) % 994348472629
(sqm iteration) computing (921153283301 * 494888873439^8412068) % 994348472629
(sqm iteration) computing (921153283301 * 255946549071^4206034) % 994348472629
(sqm iteration) computing (921153283301 * 921556030333^2103017) % 994348472629
(sqm iteration) computing (268488152375 * 990196147175^1051508) % 994348472629
(sqm iteration) computing (268488152375 * 47198554029^525754) % 994348472629
(sqm iteration) computing (268488152375 * 467841164647^262877) % 994348472629
(sqm iteration) computing (644809215284 * 865816798398^131438) % 994348472629
(sqm iteration) computing (644809215284 * 501639319341^65719) % 994348472629
(sqm iteration) computing (26337228643 * 891167495425^32859) % 994348472629
(sqm iteration) computing (895642694818 * 467043903631^16429) % 994348472629
(sqm iteration) computing (404756218143 * 622045366798^8214) % 994348472629
(sqm iteration) computing (404756218143 * 522760780235^4107) % 994348472629
(sqm iteration) computing (281255078862 * 803664929813^2053) % 994348472629
(sqm iteration) computing (502271318414 * 852782121265^1026) % 994348472629
(sqm iteration) computing (502271318414 * 407646260658^513) % 994348472629
(sqm iteration) computing (33851880051 * 760374205862^256) % 994348472629
(sqm iteration) computing (33851880051 * 277397929319^128) % 994348472629
(sqm iteration) computing (33851880051 * 535426710156^64) % 994348472629
(sqm iteration) computing (33851880051 * 627846812638^32) % 994348472629
(sqm iteration) computing (33851880051 * 48601339780^16) % 994348472629
(sqm iteration) computing (33851880051 * 386874218949^8) % 994348472629
(sqm iteration) computing (33851880051 * 560712679276^4) % 994348472629
(sqm iteration) computing (33851880051 * 484659064418^2) % 994348472629
(sqm iteration) computing (33851880051 * 551560475289^1) % 994348472629
(sqm) 984327457683^2153489582 % 994348472629 = 331688688384
(pow) computing 235973^456789 % 583903
(pow) 235973^456789 % 583903 = 418744
(pow) computing 984327457683^2153489582 % 994348472629
(pow) 984327457683^2153489582 % 994348472629 = 331688688384
```


