__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.lca_modules.building_envelope import WoodFraming
from pod_lca.lca_modules.building_envelope import MetalFraming


def wooden_framing_from_parameters(name, material_property, spacing, width, length):
    framing = WoodFraming.from_parameters(name, material_property, spacing, width, length)
    return framing

def metal_framing_from_parameters(name, material_property, spacing, section_id):
    framing = MetalFraming.from_parameters(name, material_property, spacing, section_id)
    return framing