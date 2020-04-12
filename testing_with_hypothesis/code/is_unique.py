from hypothesis import given
import hypothesis.strategies as st

def is_unique(string):
    unique_chars = set()
    for char in string:
        if char not in unique_chars:
            unique_chars.add(char)
        else:
            return False
    return True

@given(st.lists(elements = st.characters(max_codepoint=128, blacklist_categories=('Cc', 'Cs')), unique = True))
def test_unique(string):
    print(string)
    assert is_unique(string) == True

@given(st.lists(elements = st.characters(max_codepoint=128, blacklist_categories=('Cc', 'Cs'))).filter(lambda x: len(set(x)) != len(x)))
def test_non_unique(string):
    assert is_unique(string) == False

if __name__ == "__main__":
    print(is_unique(["'", '3', 'Ȇ', 'Ȇ']))