from hypothesis import given, assume
from hypothesis.strategies import characters, text, composite

def urlify(string, true_len):
    string = list(string)
    full_len = len(string)
    to = full_len - 1
    frm = true_len - 1

    while(frm >= 0):
        if string[frm] != ' ':
            string[to] = string[frm]
            frm -= 1
            to  -= 1
        else:
            string[to - 2], string[to - 1], string[to] = ('%', '2', '0')
            to -= 3
            frm -= 1
    
    return ''.join(string)

string_gen = text(characters(min_codepoint=1, max_codepoint=127, blacklist_categories=('Cc', 'Cs'))).map(lambda s: s.strip())

@composite
def gen_test_input(draw):
    stripped = draw(string_gen)
    actual_len = len(stripped)
    add_spaces = stripped.count(' ')
    before = stripped + (add_spaces * 2) * ' '
    return (stripped, before, actual_len)

@given(gen_test_input())
def test_urlify(inp):
    stripped, before, actual_len = inp
    assume(len(stripped) > 0)
    after = urlify(before, actual_len)
    print('before',before,'after',after)
    before_split = stripped.split(' ')
    after_split = after.split('%20')

    assert len(before_split) == len(after_split)
    
    for i in range(len(after_split)):
        assert before_split[i] == after_split[i]

if __name__ == "__main__":
    string = 'Mr John Smith    '
    string = '0 0  '
    print(urlify(string, 3))
