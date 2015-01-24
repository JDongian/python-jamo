.. _sample_usage:


=======
Samples
=======

Listed here are basic use cases of the jamo module.

Checking Character Types
------------------------

Functions exist to determine character types::

    >>> from jamo import (is_jamo, is_jamo_modern,
                          is_hcj, is_hcj_modern,
                          is_hangul_char)
    >>> is_jamo("한")
    False
    >>> is_jamo("ㅎ")
    True
    >>> is_jamo_modern("ㆄ")
    False
    >>> is_jamo_modern("ㅍ")
    True
    >>> is_hcj(chr(0x1100))
    False
    >>> is_hcj(chr(0x3131))
    True
    >>> is_hcj_modern("ㄱ")
    True
    >>> is_hangul_char("한")
    True
    >>> ''.join(_ for _ in "한글=ㅎㅏㄴㄱㅡㄹ" if is_jamo(_))
    'ㅎㅏㄴㄱㅡㄹ'

These functions require a single character as input. Note that ``is_jamo`` and
``is_jamo_modern`` return ``True`` for HCJ characters.


Jamo Position
--------------

The function ``get_jamo_class`` returns a string
representing the position of the jamo character. Initial consonants are
represented with ``"lead"``, vowels with ``"vowel"``, and final consonants with
``"tail"``::

    >>> from jamo import get_jamo_class
    >>> get_jamo_class("ᄋ")
    'lead'
    >>> get_jamo_class("ᆐ")
    'vowel'
    >>> get_jamo_class("ᆼ")
    'tail'
    >>> get_jamo_class("ㅁ")
    Could not parse jamo: U+3141
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/joshua/git/jamo/jamo/jamo.py", line 168, in get_jamo_class
        raise InvalidJamoError("Invalid or classless jamo argument.", jamo)
    jamo.jamo.InvalidJamoError: Invalid or classless jamo argument.

This function does not accept HCJ consonants, as they are ambiguous.


Converting between Jamo and HCJ
-------------------------------

Converting from jamo to HCJ is straightforward::

    >>> from jamo import j2hcj
    >>> j2hcj("자모: ᄀ ᄁ ᄂ ᄃ ᄄ ᄅ")
    '자모: ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ'

The associated generator is ``jamo_to_hcj``.

Converting from HCJ to jamo is less simple::

    >>> from jamo import hcj2j
    >>> hcj2j("ㅇ", "lead")
    'ᄋ'
    >>> hcj2j("ㅇ", "tail")
    'ᆼ'
    >>> hcj2j("ㅏ", "vowel")
    'ᅡ'
    >>> hcj2j("ㅏ")
    'ᅡ'

The class must be given for consonants, and must be either the string
``"lead"```, ``"vowel"``, or ``"tail"``.

Both of these functions have corresponding generators: ``jamo_to_hcj`` and
``hcj_to_jamo``, respectively.


Converting from Hangul to Jamo
------------------------------

Converting from Hangul to jamo is straightforward::

    from jamo import h2j
    >>> h2j("What is 한글?")
    'What is 한글?'

or more commonly::

    from jamo import h2j, j2hcj
    >>> j2hcj(h2j("What is 한글?"))
    'What is ㅎㅏㄴㄱㅡㄹ?'

This produces HCJ output and is preferable for font compatibility on the web.


Building Hangul Characters
--------------------------

Building Hangul from jamo is easy, but must be done character-by-character::

    from jamo import j2h
    >>> j2h("ㅈ", "ㅏ")
    '자'
    >>> j2h("ㅎ", "ㅏ", "ㄴ")
    '한'

Note that HCJ and jamo inputs are both supported.
