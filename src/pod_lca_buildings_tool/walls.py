__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope import FramedWall
from pod_lca.lca_modules.building_envelope import Wall


def framed_wall_from_layers_and_framing(name, layers, framing):
    framed_wall = FramedWall.from_layers_framing(name, layers, framing)
    return framed_wall

def wall_from_layers(name, layers):
    wall = Wall.from_layers(name, layers)
    return wall