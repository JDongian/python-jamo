"""Syllable and jamo analysis for Korean. Default exchange form is Hangul
characters, not codepoints. Jamo exchange form is U+11xx codepoints, not
Hangul Compatibility Jamo (HCJ) codepoints U+3xxx or characters.

For more information, see:
http://gernot-katzers-spice-pages.com/var/korean_hangul_unicode.html
"""

JAMO_OFFSET = 44032

def jamo_to_hangul(lead, vowel, tail=0):
    """Return the Hangul character for the given jamo parts."""
    # TODO: allow non-index input i.e. HCJ and 0x11XX jamo.
    return chr(tail + (vowel-1)*28 + (lead-1)*588 + JAMO_OFFSET)

def hangul_to_jamo(syllable):
    """Return a 3-tuple of lead, vowel, and tail jamo."""
    rem = ord(syllable) - JAMO_OFFSET
    tail = rem % 28
    vowel = 1 + ((rem - tail) % 588)//28
    lead = 1 + rem//588
    return lead + 0x10ff, vowel + 0x1160, tail + 0x11a7

def get_jamo_positon(jamo):
    """Determine if a jamo (not HCJ) is a lead, vowel, or tail.
    """
    # Allow single character strings, autoconverting to a codepoint.
    if type(jamo) == str:
        jamo = ord(jamo)
    # TODO: Stricter jamo constraint checking (not all in range are valid).
    if 0x1100 <= jamo <= 0x1112:
        return "lead"
    if 0x1161 <= jamo <= 0x1175:
        return "vowel"
    if 0x11a8 <= jamo <= 0x11c2:
        return "lead"
    else:
        # TODO: perhaps raise an InvalidJamoError
        return False

def to_hcj(jamo):
    """Change a jamo codepoint to a HCJ codepoint (better for display)."""
    # Allow single character strings, autoconverting to a codepoint.
    if type(jamo) == str:
        jamo = ord(jamo)
    syllable_class = get_jamo_positon(jamo)
    if syllable_class == "lead":
        # TODO: implement
        return None
    if syllable_class == "vowel":
        return jamo + (ord("ㅏ") - 0x1161)
    if syllable_class == "tail":
        # TODO: implement
        return None
