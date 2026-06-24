__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.units import Quantity
from pod_lca.units import UNITS_MAP


def quantity_from_value_unit(value, unit):
    if unit not in UNITS_MAP:
        raise ValueError('The {} unit does not exist in the library'.format(unit))
    unit = UNITS_MAP[unit]
    return Quantity(value, unit)