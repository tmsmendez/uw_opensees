__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building import Building


def building_from_assemblies(name, location, built_year, life_span, structure, building_envelope):
    building = Building.from_assemblies(name, location, built_year, life_span, structure, building_envelope)
    return building