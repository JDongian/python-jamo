python-jamo
===========

python-jamo is a Python Hangul syllable decomposition and sythesis library
for working with Hangul characters and jamo (U+11xx).

Currently in early release, only modern Hangul is currently supported
(no U+317x, ㆀ, ㆄ, or other archaic stuff).
Support for archaic Hangul will probably be added in the future (read: never).

Originally designed to help students identify difficult-to-spell words
containing (ㅔ,ㅐ) or (ㅗ,ㅜ), this project hopes to fill the niche of Korean
phonetic and spelling analysis.


Installation
------------

Install from `pypi <https://pypi.python.org/pypi/jamo/0.1>`_::

   $ pip install jamo


Examples
--------

Hangul syllables can be decomposed and sythesised using jamo::

   >>> from jamo import jamo
   >>> lead, vowel, tail = jamo.hangul_to_jamo("한")
   >>> print((ord(lead), ord(vowel), ord(tail)))
   (4370, 4449, 4523)
   >>> print(''.join([jamo.jamo_to_hcj(_) for _ in (lead, vowel, tail)]))
   ㅎㅏㄴ
   >>> print(jamo.jamo_to_hangul(lead, vowel, tail))
   한


Documentation
-------------

Documentation on ReadTheDocs coming soon.


Contributing
------------

Like this project or want to help? I'm an active github-er, and will review
pulls. I'm open to email as well, so please contact me if you have any ideas
for this project.


License
-------

Apache 2.0
