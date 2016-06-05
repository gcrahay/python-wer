========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls|
        | |landscape| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/wer/badge/?style=flat
    :target: https://readthedocs.org/projects/wer
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/gcrahay/python-wer.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/gcrahay/python-wer

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/gcrahay/python-wer?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/gcrahay/python-wer

.. |requires| image:: https://requires.io/github/gcrahay/python-wer/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/gcrahay/python-wer/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/github/gcrahay/python-wer/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/gcrahay/python-wer

.. |landscape| image:: https://landscape.io/github/gcrahay/python-wer/master/landscape.svg?style=flat
    :target: https://landscape.io/github/gcrahay/python-wer/master
    :alt: Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/gcrahay/python-wer/badges/gpa.svg
   :target: https://codeclimate.com/github/gcrahay/python-wer
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/wer.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/wer

.. |downloads| image:: https://img.shields.io/pypi/dm/wer.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/wer

.. |wheel| image:: https://img.shields.io/pypi/wheel/wer.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/wer

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/wer.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/wer

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/wer.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/wer


.. end-badges

Python parser for Microsoft Windows Event Reports (WER)

* Free software: BSD license

Installation
============

::

    pip install wer

Documentation
=============

https://wer.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
