__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.lca_modules.building_envelope import Layer

def layer_from_material_property_and_thickness(name, material_property, thickness, classification):
    l = Layer.from_property_and_thickness(name, material_property, thickness, classification)
    return l