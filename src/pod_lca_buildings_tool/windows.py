__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope import Window
from pod_lca.utilities import config


constructions_path = config['file_paths']['operational']['CONSTRUCTIONS']



def window_from_idf_and_dimensions(name, width, length):
    window = Window.from_idf(name, constructions_path)
    window.set_width_height(width, length)
    return window

def window_from_idf_and_wwr(name, wwr):
    window = Window.from_idf(name, constructions_path)
    window.set_wwr(wwr)
    return window