# Project 6

John French

## 1

> 7.12

TODO

## 2

> Let `N = pq` be the product of two distinct primes. Show that if `phi(N)` and `N` are known, then it is possible to compute p and q efficiently.
>
> ```
> N = \
>   95108693570035270144657857241002423425941108178488256393099501537459309973338\
>   65903207013740146605728809325133894534690938666295070929707354702678260553685\
>   14300093151549632505274835414996617776105712264615480179835373573409777911917\
>   82144166557488091378280662921890402461825132632264736288885016437441408031437
> phi(N) = \
>   95108693570035270144657857241002423425941108178488256393099501537459309973338\
>   65903207013740146605728809325133894534690938666295070929707354702678260553683\
>   18495457624031792603571257178204989211193226542164492447936114070312943915254\
>   98300469688335255546240141624625909322093238921327083984345759003847642930236
> ```

```
   phi(pq) = (p - 1)(q - 1)
=> phi(pq) = pq - p - q + 1
=>  phi(N) = N - p - q + 1
=>       q = N - p - phi(N) + 1
=>     N/p = N - p - phi(N) + 1
=>       N = -p^2 + (N - phi(N) + 1)p
=>       0 = -p^2 + (N - phi(N) + 1)p - N
```

So we can solve that quadratic equation to find `p` and then simply calculate `N/p = q`. Code to do this is in `factor.py`. For the values given, it outputs:

```
p = \
  89300314130157132517011694107560797929270706821864692871958531999198765236520\
  14993659519213116912069200954044106058932381498603052808998405591330354317643

q = \
  106504321397360707384691884129230830635641778900586294859940727503898068760142\
  68850037349939718919971320343220387080799512212334599495540851842263410783559
```

## 3

> Implement padded RSA, as introduced in class. Assume that the message m is always a 256 bit key, i.e. `|m| = 256` and that `|N| = 1024`.

My code is in `rsa.py`.

## 4

> In this question you will become familiar with real world usage of public key en- cryption. The goal is to send a correctly encrypted email to ece480x@wpi.edu, containing your name and explain why you might need to use this method to send an email to someone. Your email should be encrypted using the public key available in mywpi.

I sent the message:

```
This is a message from John French <jdfrench@wpi.edu>. One example of when you
might need to send an encrypted email is if you discover a severe vulnerability
in a piece of software and want to notify the developer without anyone else
finding out. This email is also signed with my PGP public key, which can be
downloaded from <hkp://pgp.mit.edu>. If you have verified my key fingerprint in
person, then you can be sure this email came from me. You may also be able to
trust that this email came from me via a web of trust if you trust any of the
signers of my key.
```

Encrypted with the given public key (and signed with my private key), in ASCII-armored format:

```
-----BEGIN PGP MESSAGE-----
Comment: GPGTools - https://gpgtools.org

hQEMA6cnFuBnBDP0AQf/Ys58e93cXogYffzrROlJYrIiOPbw2g3CNWKYCBXYz5aU
3Rk2cNMeqZGgCjWLhqS6lIb/eyRiqejAesUgFSSsHuNDqpnoa8Z7NiWAEyOEvIlo
1A1xlb6Wm1zinkU02SmJKHhNZix8tHy44Ic53x1qCh2LH0CqfLrtJUagXJXqyxP5
TTv8zGYx59eGDvS2ACuHpu4lHCCSeu0QXC6hNwTY72AdzF7PFCdctGSJ9N2wj9WU
Iw43dv6Zhh0a6K4W4VNjj5pkVgeSQWVlPl1/ATDCbkWmTaJV3+1D+ffA8+thn4If
3tkEUkz4wPaYswNXexFQ8CHlbR1OHqfAbxZ/J3S48cnAq8fr9d2f2Hz0EpO8sGY1
LnMBUINtAAQvydh1AaVbX9meraF6qB2eYAx62askSroihLNOPYSDyqyiD0MJvA4U
95LBECMBfevoOL+H+22BhE7cACJ3mBIEIEKsodpjnCvZy1fNTJH+P552WuUMa9zs
j0k6WgPWCmWLmfucH9gpfGExtQfccKapzlL+n80zw17zhWQMg0ZP7QVimhLRxgEf
o7OXv9xrY8oFTAZlPKAdJ2sJyNyk8hAx/Du3NRdVWt7nTqtPi8SjPIW1HV5TkN37
4+1Zqevd8hUBe+MvKVmmcP27wqYyniXOjO/reeMyjxcbsuU1pGuylY6P8lbUjY9N
AB61FdeQM2ZGN/bfXTm0r1n5168Ei/upqDk5nX951gAdht3/mbfv7S/Y2aKUKPY9
BA9mYSD5zSdHDIev51/C7l06DPSwCWVIBvOEMTsGrTS9U8hgg1M7XjeHYs3BawoF
XTHpDisWsRQKC+AYvQ==
=EzbV
-----END PGP MESSAGE-----
```
