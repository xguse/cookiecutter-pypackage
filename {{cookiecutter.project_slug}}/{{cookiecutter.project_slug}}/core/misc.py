"""Provide functionality that doesn't fit anywhere else."""


def true_false_word_to_bool(word):
    """Return appropriate `bool` given a string representing a bool-like word.

    Args:
        word (str): a string representing a bool-like word

    Raises:
        ValueError: if no `bool` can be interpreted from the string.
    """
    word_ = word.upper()
    if word_ == "TRUE":
        return True
    elif word_ == "FALSE":
        return False
    else:
        raise ValueError(f"word can not be interpreted as meaning True/False: {word}")


def cast_as(x, dtype):
    """Return `x` cast as `dtype` with some hand-holding.

    Strings that can be interpreted as bool-like will be converted to bool.
    `None` will be returned if the casting fails.

    Args:
        x (str): usually a string representation of a value.
        dtype (type): type-constructor to attempt the casting ex: cast_as('1', float) will return 1.0
    """
    if dtype.__name__ == "bool":
        return true_false_word_to_bool(x)

    try:
        return dtype(x)
    except ValueError:
        return None


def recode_table_by_test(df, column, tests, replacement):
    df = df.copy()
    df[column] = df[column].where(~tests, other=replacement)
    return df


def recode_flag_type(df, column, flag_type):
    df = df.copy()
    if flag_type is None:
        return df


class Tree(dict):
    """Autovivify arbitrary depth nested dicts."""

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
