# License information goes here
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
# The line above will help with 2to3 support.
"""
========
desiUtil
========

This package provides low-level utilities for general use by DESI_.

.. _DESI: http://desi.lbl.gov
"""

def version():
    """Returns the version of the desiUtil package.

    Parameters
    ----------
    None

    Returns
    -------
    version : str
        A PEP386-compatible version string.

    Notes
    -----
    The version string should be compatible with PEP386_.

    .. _PEP386: http://www.python.org/dev/peps/pep-0386).
    """
    return '0.1.1.dev'

__version__ = version()
