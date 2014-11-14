from setuptools import setup, find_packages
from jamo import __version__
import sys

if sys.version_info <= (3, 0):
    print("ERROR: jamo requires Python 3.0 or later "
          "(bleeding edge preferred)", file=sys.stderr)
    sys.exit(1)

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="jamo",
    version=__version__,
    description="A Hangul syllable and jamo analyzer.",
    long_description=long_description,
    url="https://github.com/jdong820/python-jamo",
    author="Joshua Dong",
    author_email="jdong42@gmail.com",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    keywords="Korean Hangul jamo syllable nlp",
    packages=find_packages(),
)
