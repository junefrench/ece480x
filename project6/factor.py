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


def _integer_sqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    if x * x != n:
        raise ValueError("{0} is not a perfect square".format(n))
    return x


def _integer_div(n, d):
    if n % d != 0:
        raise ValueError('{0} is not divisible by {1}'.format(n, d))
    return n // d


def factor_prime_product(product, phi):
    """Given a product of two primes and the value of Euler's totient function for that product, find the primes."""
    # 0 = -p^2 + (N - phi(N) + 1)p - N
    # so coefficients (for form 0 = ax^2 + bx + c) are:
    a = -1
    b = product - phi + 1
    c = -product
    # Apply quadratic formula to find p
    # x = (sqrt(b^2 - 4ac) - b) / 2a
    p = _integer_div(_integer_sqrt(b * b - 4 * a * c) - b, 2 * a)

    q = _integer_div(product, p)
    return p, q


from unittest import TestCase


class TestFactor(TestCase):
    def testFactor(self):
        self.assertEqual(factor_prime_product(35, 24), (5, 7))
        self.assertEqual(factor_prime_product(143, 120), (11, 13))

if __name__ == '__main__':
    n = int(
        "95108693570035270144657857241002423425941108178488256393099501537459309973338659032070137401466057288093251338"
        "94534690938666295070929707354702678260553685143000931515496325052748354149966177761057122646154801798353735734"
        "0977791191782144166557488091378280662921890402461825132632264736288885016437441408031437"
    )
    phi_n = int(
        "95108693570035270144657857241002423425941108178488256393099501537459309973338659032070137401466057288093251338"
        "94534690938666295070929707354702678260553683184954576240317926035712571782049892111932265421644924479361140703"
        "1294391525498300469688335255546240141624625909322093238921327083984345759003847642930236"
    )

    print("p, q = {0}, {1}".format(*factor_prime_product(n, phi_n)))
