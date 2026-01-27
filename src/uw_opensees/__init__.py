"""
********************************************************************************
uw_opensees
********************************************************************************

.. currentmodule:: uw_opensees


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os
import sys


__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


HERE = os.path.dirname(__file__)

HOME     = os.path.abspath(os.path.join(HERE, "../../"))
DATA     = os.path.abspath(os.path.join(HOME, "data"))
DOCS     = os.path.abspath(os.path.join(HOME, "docs"))
TEMP     = os.path.abspath(os.path.join(HOME, "temp"))
OPENSEES = os.path.abspath(os.path.join(HOME, "OpenSees3.7.1", "bin", "OpenSees"))

__all__ = ["HOME", "DATA", "DOCS", "TEMP", "OPENSEES"]

