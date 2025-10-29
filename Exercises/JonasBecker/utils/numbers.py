def can_be_interpreted_as_number(arg: str) -> bool:
    """
    Check if a given string can be interpreted as number in various ways.

    This function tests whether the input string can be interpreted as:
    - a complex number (e.g., "1+2j"),
    - an integer in hexadecimal (0x...), octal (0o...), or binary (0b...) format.

    - no operations like fractions or keywords like PI supported!
    - trailing or leading spaces get removed

    Parameters
    ----------
    arg : str
        The string to test.

    Returns
    -------
    bool
        True if the string represents a number according to above's definition, False otherwise.
    """
    arg = arg.replace(
        " ", ""
    )  # debatable, irl you would discuss exact behaviour before hand, kept it in for demonstration because you could argue spaces are just for decoration and no new operations were added
    arg.strip()  # \t etc.
    try:  # alternatively check instead of error-proofing "EAFP" -> "Easier to ask for forgiveness than permission" or "European Association of Fish Pathologists e.V."
        complex(
            arg  # remove leading and trailing spaces \t etc
        )  # to support fractions (operations) -> e.g. use Fraction(arg)
        return True
    except (
        ValueError
    ):  # ValueError is the only type of error that could happen and the one we are interested in
        pass

    for base in (16, 8, 2):
        try:
            int(arg, base)
            return True
        except ValueError:
            continue
    return False
