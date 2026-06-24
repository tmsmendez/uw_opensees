__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.utilities import config

from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyMass
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyAirGap
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyNoMass
from pod_lca.lca_modules.building_envelope.material_property import WindowMaterialPropertyGlazing

from pod_lca.units import INCH, METER, SQUARE_METER, CUBIC_METER, WATT, KELVIN, KILOGRAM, JOULE
from pod_lca.units import Quantity as Q


# From properties - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def material_property_no_mass(name,
                              conductivity,
                              thickness,
                              roughness,
                              thermal_absorptance=.9,
                              solar_absorptance=.7, 
                              visible_absorptance=.7):
    m = EnvelopeMaterialPropertyNoMass()
    m.name                = name
    m.conductivity        = Q(conductivity, WATT/(METER*KELVIN))
    m.thickness           = Q(thickness, METER)
    m.roughness           = roughness
    m.thermal_absorptance = thermal_absorptance
    m.solar_absorptance   = solar_absorptance
    m.visible_absorptance = visible_absorptance
    return m




# From IDF - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

constructions_path = config['file_paths']['operational']['CONSTRUCTIONS']


def material_property_mass_from_idf(name):
    m = EnvelopeMaterialPropertyMass.from_idf(name, constructions_path)
    return m

def material_property_no_mass_from_idf(name):
    m = EnvelopeMaterialPropertyNoMass.from_idf(name, constructions_path)
    return m

def material_property_air_gap_from_idf(name):
    m = EnvelopeMaterialPropertyAirGap.from_idf(name, constructions_path)
    return m

def material_property_glazing_from_idf(name):
    m = WindowMaterialPropertyGlazing.from_idf(name, constructions_path)
    return m




if __name__ == '__main__':
    material_property = material_property_mass_from_idf('Clay Brick')
    print(material_property)