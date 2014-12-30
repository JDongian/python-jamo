.. _Jamo:

============================
A Guide to using Python-Jamo
============================

*DISCLAIMER: This library is under development and is going through big
changes. Read at your own risk.*

`Hangul <https://en.wikipedia.org/wiki/Hangul>`_ is a wonderful writing system.
Originating in 1443 to represent the Korean language, it is an alphabet of 24
consonants and vowels, each of which are called **jamo** (자모/字母).

Let's analyze it's phonemes by decomposing some Hangul. Maybe even construct
some Hangul afterwards.

Hangul Decomposition
--------------------

The python jamo library aims to provide a straightforward interface to Hangul
decomposition::

    >>> from jamo import h2j
    >>> h2j("한굴")
    ['ᄒ', 'ᅡ', 'ᆫ', 'ᄀ', 'ᅮ', 'ᆯ']
    >>> h2j("자모=字母")
    ['ᄌ', 'ᅡ', '\\x00', 'ᄆ', 'ᅩ', '\\x00', '=', '字', '母']

That was easy! Notice that the characters may not have rendered correctly. This
is because there are actually two sets of jamo in Unicode. We printed the
U+11xx set. The set that computers actually use for *rendering* individual jamo
characters is in U+31xx. To learn more, read more about `Hangul Compatibility
Jamo` (here on referenced as HJC).

Say we wanted to get the display characters::

    >>> from jamo import h2cj
    >>> h2cj("한굴")
    ㅎㅏㄴㄱㅜㄹ
    >>> h2cj("자모=字母")
    ㅈㅏㅁㅗ=字母 

Decomposing Hangul is as simple as that.

Hangul Synthesis
----------------

There are two functions for Hangul synthesis. The first combines a lead, vowel,
and optional tail::
    
    >>> from jamo import j2h
    >>> j2h('ㅇ', 'ㅕ', 'ㅇ')
    영
    >>> j2h('ㅇ', 'ㅓ')
    어

Ambiguity may arise when there is a long string of jamo. The library does its
best to guess what the original Hangul was::

    >>> from jamo import synth_hangul
    >>> synth_hangul("...")
    (True, ...)
    >>> synth_hangul("...")
    (False, ...)

Note that when there are ambiguous cases, `False` is returned as the status.

Large Texts
------------

When working with large files, we will end up with lots of output. To handle
large files, it is recommended to use the generator functions::

    >>> from jamo import hangul_to_jamo
    >>> long_story = open("구운몽.txt", 'r').read()
    >>> hangul_to_jamo(long_story)
    <itertools.chain at 0x7f31baf89cc0>

and for HCJ::

    >>> from jamo import hangul_to_hcj
    >>> long_story = open("구운몽.txt", 'r').read()
    >>> hangul_to_hcj(long_story)
    <itertools.chain at 0x7f31baf89cc0>
