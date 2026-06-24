__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope import Floor
from pod_lca.utilities import config


constructions_path = config['file_paths']['operational']['CONSTRUCTIONS']


def floor_from_idf(name):
    floor = Floor.from_idf(name, constructions_path)
    return floor
