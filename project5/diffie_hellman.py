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


from gmpy2 import is_prime
from Crypto.Hash import SHA256
# Uncomment next line and comment line after for more secure random numbers.
# from Crypto.Random import random
import random


def get_random(bits):
    """Get a random number which is a specified number of bits long."""

    # Get bits - 1 random bits, and then make the highest-order bit 1.
    return random.getrandbits(bits - 1) | (1 << (bits - 1))


def get_safe_prime(bits):
    """Get a safe prime which is a specified number of bits long."""

    while True:
        # Generate a random 1024 bit number, ensuring the lowest order bit is 1 (so it's odd).
        candidate = (get_random(bits - 1) << 1) | 1
        if candidate % 12 != 11:
            continue  # all safe primes mod 12 are 11
        if not is_prime(candidate):
            continue  # obviously a safe prime must be prime
        if not is_prime((candidate - 1) // 2):
            continue  # a safe prime must be equal to 2q + 1 where q is prime
        return candidate


class DiffieHellmanParticipant():
    def __init__(self, p, g, a=None, min_bits_p=1024, min_bits_a=256):
        """Create a Diffie-Hellman Key Exchange participant.
        :param p: the public prime p, should be prime
        :param g: the base g, should be a primitive root modulo p
        :param a: this participant's private exponent (if None, it will be picked randomly)
        :param min_bits_p: the minimum acceptable length of p, in bits
        :param min_bits_a: the minimum acceptable length of a, in bits
        :return: a Diffie-Hellman Key Exchange participant
        """
        # ensure that p is a safe prime
        if not (is_prime(p) and is_prime((p - 1) // 2)):
            raise ValueError("p is not a safe prime")

        # ensure that p is big enough
        if p.bit_length() < min_bits_p:
            raise ValueError("p is too small")

        # ensure that g is in the multiplicative group of integers mod p ([2, 3, 4, ... p-2])
        if g not in range(2, p-1):
            raise ValueError("g is not in the multiplicative group of integers mod p")

        # generate a or check its size
        if a is None:
            a = random.randrange(1 << (min_bits_a - 1), (p - 1) // 2)
        elif a.bit_length < min_bits_a or a >= (p - 1) // 2:
            raise ValueError("a is either too small or too big")

        # store values
        self.p = p
        self.g = g
        self._a = a
        # calculate and store this participant's public key
        self.A = pow(g, a, p)

        # initialize other participant's public key and session key to None
        self.B = None
        self._s = None
        self._session_key = None

    def get_pubkey(self):
        """Get this participant's public key."""
        return self.A

    def receive_pubkey(self, B):
        """Give this participant the other's public key and compute the shared session key."""
        self.B = B

        # Compute session secret.
        self._s = pow(B, self._a, self.p)

        # Compute session key by hashing session secret.
        hash = SHA256.new()
        hash.update(self._s.to_bytes((self._s.bit_length() + 7) // 8, 'big'))
        self._session_key = hash.digest()


if __name__ == '__main__':
    # Seed the random generator with a constant for deterministic behavior.
    random.seed(12345)

    # Uncomment next line and comment out the static initialization below to generate a safe prime on-the fly.
    # This takes a minute or two.
    # p = get_safe_prime(1024)
    p = int(
        "0xfaa5d435db51cdfe851b06cdef5c1649dae717681c24dcadc43c9d6a57d4d0ad2b041c4c97fe9776449933be9c34861bd9ab0f6b6eae"
        "6db09f3176305a44d9e590d68602686efe4f7da37b8e0c97114e4051788522fa72b381d4c0b6e2d3b87411c2ff01db87470d1cb0db53df"
        "9fd8a4634bbef61c3305d883701ee02eed5cdb",
        16
    )
    print("Alice and Bob agree on prime {0}".format(hex(p)))

    # Select g randomly from [2, 3, 4, ... p-2].
    g = random.randint(2, p - 2)
    print("Alice and Bob agree on base {0}".format(hex(g)))

    # Construct the participants from the public p and g.
    # They will internally select secret exponents.
    alice = DiffieHellmanParticipant(p, g, min_bits_p=1024)
    print("Alice selects private key {0}".format(hex(alice._a)))
    print("Alice computes her public key {0}".format(hex(alice.A)))
    bob = DiffieHellmanParticipant(p, g, min_bits_p=1024)
    print("Bob selects private key {0}".format(hex(bob._a)))
    print("Bob computes his public key {0}".format(hex(bob.A)))

    # Exchange public keys.
    alice.receive_pubkey(bob.get_pubkey())
    print("Alice receives Bob's public key and computes the shared secret 0x{0}".format(hex(alice._s)))
    bob.receive_pubkey(alice.get_pubkey())
    print("Bob receives Alice's public key and computes the shared secret 0x{0}".format(hex(bob._s)))

    # Check that Alice and Bob have the same key.
    assert alice._session_key == bob._session_key
    from binascii import hexlify
    print("Alice and Bob both hash their shared secret to get the session key 0x{0}".format(hexlify(alice._session_key).decode('utf-8')))

