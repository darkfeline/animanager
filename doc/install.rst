Installation and configuration
==============================

For all methods, `Python 3`_ is required.

.. _Python 3: https://www.python.org/

.. note::

   The current version of tabulate_ from PyPi does not support double-width
   characters, leading to ugly table formatting.  You can install tabulate from
   the source, or install Animanager's development dependencies (see
   :ref:`requirements`).

.. _tabulate: https://bitbucket.org/astanin/python-tabulate

From PyPi
---------

Animanager can be installed fairly easily using from PyPi using pip_::

  $ pip3 install animanager

You may want to or need to install Animanager for the current user only::

  $ pip3 install --user animanager

This requires pip_ for Python 3.

.. _pip: https://pip.pypa.io/en/stable/

Setuptools
----------

Animanager can also be installed from the source::

  $ make install

This is equivalent to::

  $ python3 setup.py install

You can also supply extra flags::

  $ make INSTALL_FLAGS=--user install

This requires setuptools_ for Python 3.  You can also install Animanager's
development dependencies, which includes setuptools, among other useful packages
when building from source (see :ref:`requirements`).

.. _setuptools: https://pythonhosted.org/setuptools/

.. _requirements:

Development dependencies
------------------------

You can install the development dependencies via a make shortcut::

  $ make requirements

This is equivalent to::

  $ pip3 install -r requirements.txt

Again, you can supply extra flags::

  $ make INSTALL_FLAGS=--user requirements

Incidentally, this will also install setuptools_, which is needed for installing
Animanager from source.

This requires pip_ for Python 3.

Configuration
-------------

Animanager uses an INI configuration file.  An example ``config.ini`` is
supplied with the source distribution.

By default, Animanager looks for the configuration file at
``~/.animanager/config.ini``.  This can be changed with the ``-config`` flag.
