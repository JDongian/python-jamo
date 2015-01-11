"""Syllable and jamo analysis for Korean. Default internal exchange form is
Hangul characters, not codepoints. Jamo exchange form is U+11xx characters,
not U+3xxx Hangul Compatibility Jamo (HCJ) characters or codepoints.

For more information, see:
http://python-jamo.readthedocs.org/ko/latest/
"""

from sys import stderr
from itertools import chain

JAMO_OFFSET = 44032
JAMO_LEAD_OFFSET = 0x10ff
JAMO_VOWEL_OFFSET = 0x1160
JAMO_TAIL_OFFSET = 0x11a7
JAMO_TO_HCJ_TRANSLATIONS = {jamo: hcj for jamo, hcj in
                            zip("ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒ"
                                "ᅡᅢᅣᅤᅥᅦᅧᅨᅩᅪᅫᅬᅭᅮᅯᅰᅱᅲᅳᅴᅵ"
                                "ᆨᆩᆪᆫᆬᆭᆮᆯᆰᆱᆲᆳᆴᆵᆶᆷᆸᆹᆺᆻᆼᆽᆾᆿᇀᇁᇂ",
                                "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
                                "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
                                "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")}
VALID_JAMO = JAMO_TO_HCJ_TRANSLATIONS.keys()
VALID_HCJ = JAMO_TO_HCJ_TRANSLATIONS.values()


class InvalidJamoError(Exception):
    """jamo is a U+11xx codepoint."""
    def __init__(self, message, jamo):
        super(InvalidJamoError, self).__init__(message)
        self.jamo = hex(jamo)
        print("Could not parse jamo: U+{code}".format(code=self.jamo[2:]),
              file=stderr)


def _to_codepoint(character):
    """Accept a Unicode character or integer and return a codepoint."""
    if not character:
        raise TypeError
    if type(character) == int:
        return character
    else:
        return ord(character)


def _value_to_jamo(value, jamo_class=None):
    try:
        _value = chr(value)
    except TypeError:
        _value = value
    # If given a jamo char or jamo integer
    if _value in VALID_JAMO:
        return value
    # If given a hcj char or hcj integer
    if _value in VALID_HCJ:
        translations = {get_jamo_class(jamo): jamo for jamo, hcj in
                        JAMO_TO_HCJ_TRANSLATIONS.items() if hcj == _value}
        # TODO: Add a custom exception for KeyError.
        return translations[jamo_class]
    # If given something else
    return value


def _value_to_hcj(value):
    """Convert a value to an HCJ character.
    Jamo characters or ints in the U+11xx jamo range will be converted to HCJ.
    """

    # TODO: Allow non-matches to pass unharmed!
    try:
        _value = chr(value)
    except TypeError:
        _value = value
    if _value in VALID_JAMO:
        return JAMO_TO_HCJ_TRANSLATIONS.get(value, value)
    return value


def _iter_to_hcj_iter(iterable):
    """Convert an iterable to an HCJ iterable.
    All ints in the U+11xx jamo range and all jamo characters will be
    converted to HCJ.
    """

    return (_value_to_hcj(_) for _ in iterable)


def _hangul_char_to_jamo(syllable):
    """Return a 3-tuple of lead, vowel, and tail jamo characters.
    Note: Non-Hangul characters are echoed back.
    """
    if is_hangul_char(syllable):
        rem = ord(syllable) - JAMO_OFFSET
        tail = rem % 28
        vowel = 1 + ((rem - tail) % 588) // 28
        lead = 1 + rem // 588
        return (chr(lead + JAMO_LEAD_OFFSET),
                chr(vowel + JAMO_VOWEL_OFFSET),
                chr(tail + JAMO_TAIL_OFFSET if tail else 0))
    else:
        return syllable


def _jamo_to_hangul_char(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo characters.
    Equivalent to jamo_to_hangul, but exported function has a shorter name.
    """
    lead = _to_codepoint(_value_to_jamo(lead, "lead"))
    vowel = _to_codepoint(_value_to_jamo(vowel, "vowel"))
    tail = _to_codepoint(_value_to_jamo(tail, "tail")) if tail else 0

    lead -= JAMO_LEAD_OFFSET
    vowel -= JAMO_VOWEL_OFFSET
    tail = tail - JAMO_TAIL_OFFSET if tail else 0
    return chr(tail + (vowel - 1) * 28 + (lead - 1) * 588 + JAMO_OFFSET)


def is_hangul_char(character):
    """Determine if a given unicode character is Hangul.
    Does not support old-style Hangul.
    """

    return ord(character) in range(0xAC00, 0xD7A4)


def get_jamo_class(jamo):
    """Determine if a jamo character is a lead, vowel, or tail.
    Integers and U+11xx characters are valid arguments. HCJ is not valid here.

    get_jamo_class should return the class ["lead" | "vowel" | "tail"] of a
    given character or integer.
    """

    # Allow single character strings, autoconverting to a codepoint.
    if type(jamo) == str:
        jamo = ord(jamo)
    # Perhaps raise a separate error for U+3xxx jamo.
    if chr(jamo) in "ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒ":
        return "lead"
    if chr(jamo) in "ᅡᅢᅣᅤᅥᅦᅧᅨᅩᅪᅫᅬᅭᅮᅯᅰᅱᅲᅳᅴᅵ":
        return "vowel"
    if chr(jamo) in "ᆨᆩᆪᆫᆬᆭᆮᆯᆰᆱᆲᆳᆴᆵᆶᆷᆸᆹᆺᆻᆼᆽᆾᆿᇀᇁᇂ":
        return "tail"
    else:
        raise InvalidJamoError("Could not not determine jamo class.", jamo)


def jamo_to_hangul(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo input.
    Integers corresponding to U+11xx jamo codepoints, U+11xx jamo characters,
    or HCJ are valid inputs.

    Outputs a one-character Hangul string.

    This function is identical to j2h.
    """

    # TODO: Allow HCJ input.
    # TODO: Implement string input.

    # Internally, we convert everything to a jamo char,
    # then pass it to _jamo_to_hangul_char
    return _jamo_to_hangul_char(lead, vowel, tail)


def j2h(lead, vowel, tail=0):
    """Arguments may be integers corresponding to the U+11xx codepoints, the
    actual U+11xx jamo characters, or HCJ.

    Outputs a one-character Hangul string.

    This function is defined solely for naming conisistency with
    jamo_to_hangul.
    """

    return jamo_to_hangul(lead, vowel, tail=0)


def jamo_to_hcj(jamo):
    """Transform jamo to HCJ.
    Arguments may be integers corresponding to U+11xx codepoints, actual
    U+11xx jamo characters, or HCJ characters. These may be in an iterable.

    jamo_to_hcj should convert every U+11xx jamo character into U+31xx HCJ
    in a given string. Non-hangul and HCJ characters are not touched.

    jamo_to_hcj is the generator version of j2hcj, the string version. Note
    that passing a non-iterable to jamo_to_hcj will still return a generator.
    """

    try:
        return _iter_to_hcj_iter(jamo)
    except TypeError:
        pass

    try:
        _value = chr(jamo)
    except TypeError:
        _value = jamo

    if _value in VALID_JAMO:
        return (_value_to_hcj(_) for _ in chr(jamo))
    return (_ for _ in [_value_to_hcj(jamo)])


def j2hcj(jamo):
    """Transform jamo into HCJ.
    Arguments may be integers corresponding to U+11xx codepoints, actual
    U+11xx jamo characters, or HCJ characters. These may be in an iterable.

    j2hcj should convert every U+11xx jamo character into U+31xx HCJ in a
    given string. Non-hangul and HCJ characters are not touched.

    j2hcj is the string version of jamo_to_hcj, the generator version.
    """

    return ''.join(jamo_to_hcj(jamo))


def hangul_to_jamo(hangul_string):
    """Convert a string of Hangul to jamo.
    Arguments may be iterables of characters.

    hangul_to_jamo should split every Hangul character into U+11xx jamo
    characters for any given string. Non-hangul characters are not changed.

    hangul_to_jamo is the generator version of h2j, the string version.
    """

    return (_ for _ in
            chain.from_iterable(_hangul_char_to_jamo(_) for _ in
                                hangul_string))


def h2j(hangul_string):
    """Convert a string of Hangul to jamo.
    Arguments may be iterables of characters.

    h2j should split every Hangul character into U+11xx jamo for any given
    string. Non-hangul characters are not touched.

    h2j is the string version of hangul_to_jamo, the generator version.
    """

    return ''.join(hangul_to_jamo(hangul_string))


def hcj_char_to_jamo(hcj_char, position="vowel"):
    """Transform a HCJ character to jamo based on jamo class."""
    raise NotImplementedError
    if position == "lead":
        return hcj_char
    elif position == "vowel":
        return hcj_char
    elif position == "tail":
        return hcj_char
    raise InvalidJamoError


def synth_hangul(string):
    """Convert jamo characters in a string into hcj as much as possible."""
    raise NotImplementedError
    return ''.join([''.join(''.join(jamo_to_hcj(_)) for _ in string)])
