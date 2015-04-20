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


def sqm_pow(b, e, m, verbose=False):
    """Computes b^e mod m using the square and multiply algorithm. If verbose is True, prints intermediate results."""
    r = 1
    while e > 0:
        if verbose:
            print("(sqm iteration) computing ({0} * {1}^{2}) % {3}".format(r, b, e, m))
        if e % 2 == 1:
            r = (r * b) % m
        b = (b * b) % m
        e >>= 1
    return r


if __name__ == '__main__':
    arg_sets = [
        (235973, 456789, 583903),
        (984327457683, 2153489582, 994348472629),
    ]
    funcs = [
        ('sqm', lambda *args: sqm_pow(*args, verbose=True)),
        ('pow', pow),
    ]

    import itertools

    results = {args: [] for args in arg_sets}
    for func_name, func in funcs:
        for args in arg_sets:
            print("({name}) computing {0}^{1} % {2}".format(*args, name=func_name))
            result = func(*args)
            print("({name}) {0}^{1} % {2} = {result}".format(*args, name=func_name, result=result))
            results[args].append(result)

    # Assert all implementations produced the same results
    for args in results:
        for result in results[args][1:]:
            assert result == results[args][0]
