__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope import Envelope


def envelope_from_components(name,
                             floor_plan,
                             wall=None,
                             floor=None,
                             ceiling=None,
                             windows=None,
                             window_wall_keys=None):

    windows_ = {}
    if windows:
        for i,window in enumerate(windows):
            windows_[window_wall_keys[i]] = window

    env = Envelope.from_components(name,
                                   floor_plan,
                                   wall=wall,
                                   floor=floor,
                                   ceiling=ceiling,
                                   windows=windows_)
    return env