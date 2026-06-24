__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope import BuildingEnvelope


def envelope_from_components(envelope, num_stories):
    be = BuildingEnvelope.from_envelope_and_stories(envelope, num_stories)
    return be