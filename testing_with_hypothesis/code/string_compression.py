from hypothesis import given, note
from hypothesis.strategies import text, characters, composite, integers

def string_compress(str0):
    if len(str0) == 0:
        return str0

    c = []
    c.append(str0[0])
    i = 1
    count = 1

    while i < len(str0):
        if c[-1] != str0[i]:
            c.append(str(count))
            c.append(str0[i])
            i += 1
            count = 1
        else:
            count += 1
            i += 1

    c.append(str(count))
    c = ''.join(c)
    
    if len(c) < len(str0):
        return c
    else:
        return str0

def expand(c_str):
    if len(c_str) < 2:
        return c_str
    
    res = []
    digit = 0
    pow_10 = 0
    for idx, c in enumerate(c_str):
        if c.isdigit():
            digit = digit * (10 ** pow_10) + int(c)
            pow_10 += 1
        else:
            if res:
                res.append(res[-1] * (digit -1))
            res.append(c)
            digit = 0
            pow_10 = 0
    
    res.append(res[-1] * (digit -1))

    return ''.join(res)

ch = characters(min_codepoint=1, max_codepoint=127, blacklist_categories=('Cc', 'Cs', 'N'))
@composite
def gen_repeated_char_strs(draw):
    res = []
    total_chars = draw(integers(min_value=0, max_value=10))
    for _ in range(total_chars):
        repeat_times = draw(integers(min_value=0, max_value=10))
        to_ap = draw(ch) * repeat_times
        res.append(to_ap)
    
    return ''.join(res)

@given(gen_repeated_char_strs())
def test_encode_decode(repeated_char_strs):
    note("compressed string = %s" % (string_compress(repeated_char_strs)))
    assert repeated_char_strs == expand(string_compress(repeated_char_strs))

if __name__ == "__main__":
    print(expand(string_compress('bbbbbbbaaaaaaa')))
    
