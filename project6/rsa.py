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

from Crypto import Random
from Crypto.Util.number import getPrime

_random = Random.new()


def _gcd(x, y):
    """Returns the greatest common denominator of x and y"""
    # Algorithm from http://en.wikipedia.org/wiki/Greatest_common_divisor
    twos = 0
    while (x % 2 == 0) and (y % 2 == 0):
        x //= 2
        y //= 2
        twos += 1
    while x != y:
        if x % 2 == 0:
            x //= 2
        elif y % 2 == 0:
            y //= 2
        elif x > y:
            x = (x - y) // 2
        else:
            y = (y - x) // 2
    return x * pow(2, twos)


def _mmi(x, modulo):
    """Returns the modular multiplicative inverse of x in a given modulo"""
    # Algorithm from http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Modular_integers
    def div(n, d):
        return (-1 if (n < 0) != (d < 0) else 1) * (n // abs(d))

    t = 0
    next_t = 1
    r = modulo
    next_r = x
    while next_r != 0:
        q = div(r, next_r)
        t, next_t = next_t, t - q * next_t
        r, next_r = next_r, r - q * next_r
    if r > 1:
        raise ValueError('Not invertible')
    if t < 0:
        t += modulo
    return t


def gen(factor_length=2048, random_function=_random.read, all_values=False):
    """Return an RSA keypair
    Returned keys are two dictionaries, public (with keys n and e) and private (with keys n and d)
    Will use the provided random_function to get random bytes.
    If all_values is True, the private key will also include e, p, q, and phi.
    """
    # Choose p and q and calculate n and phi
    p, q = getPrime(factor_length, random_function), getPrime(factor_length, random_function)
    n = p * q
    phi = n - p - q + 1

    # Select e
    if phi > 65537:
        # 65537 is a good value for e, so use it as long as it's in the acceptable range 1 < e < phi
        e = 65537
    else:
        # Otherwise pick the largest acceptable value
        try:
            e = next(filter(
                lambda x: (_gcd(x, phi) == 1) and (pow(x, 2, phi) != 1),
                range(phi - 1, 1, -1)
            ))
        except StopIteration:
            raise ValueError("No valid choice for e")

    # Compute d
    d = _mmi(e, phi)

    # Return keys
    public = {'n': n, 'e': e}
    private = {'n': n, 'd': d}
    if all_values:
        private.update({'e': e, 'p': p, 'q': q, 'phi': phi})
    return public, private


def enc(m, public_key):
    """Encrypt message m with a given public key (dictionary containing n and e)"""
    return pow(m, public_key['e'], public_key['n'])


def dec(c, private_key):
    """Decrypt cyphertext c with a given private key (dictionary containing n and d)"""
    return pow(c, private_key['d'], private_key['n'])


def pad(message, padded_length=1024, random_function=_random.read):
    """Convert a given message into a number m with random padding"""
    if padded_length % 8 != 0:
        raise ValueError('Bit length of padded message is not a multiple of 8')
    return int.from_bytes(random_function(padded_length // 8 - len(message)) + message, 'big')


def unpad(m, message_length=256):
    """Recover a message of a given length from a padded numerical representation m"""
    if message_length % 8 != 0:
        raise ValueError('Bit length of message is not a multiple of 8')
    return m.to_bytes(m.bit_length() // 8 + 1, 'big')[-(message_length // 8):]


from unittest import TestCase


class TestPaddedRSA(TestCase):
    def test_static_message(self):
        message = b'hello world'
        self.assertEqual(message, self._round_trip(message))

    def test_random_message(self):
        message = _random.read(256 // 8)
        self.assertEqual(message, self._round_trip(message))

    def test_encrypt_against_reference_decrypt(self):
        from Crypto.PublicKey import RSA

        public, private = gen(all_values=True)
        message = b'crypto is cool'
        m = pad(message)
        c = enc(m, public)

        rsa = RSA.construct((private['n'], private['e'], private['d']))
        m2 = rsa.decrypt(c)
        message2 = unpad(m2, len(message) * 8)

        self.assertEqual(message, message2)

    def test_decrypt_against_reference_encrypt(self):
        from Crypto.PublicKey import RSA

        rsa = RSA.generate(2048)
        message = b'textbook rsa sux'
        m = pad(message)
        c = rsa.encrypt(m, None)[0]
        m2 = dec(c, {'n': rsa.n, 'd': rsa.d})
        message2 = unpad(m2, len(message) * 8)
        self.assertEqual(message, message2)

    def _round_trip(self, message):
        public, private = gen()
        m = pad(message)
        c = enc(m, public)
        m2 = dec(c, private)
        return unpad(m2, len(message) * 8)
