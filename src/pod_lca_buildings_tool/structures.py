__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_structure import Structure
from pod_lca.lca_modules.building_structure import StatisticalStructure


def statistical_structure_from_floor_plan(floor_plan, structure_type, mui_type, num_stories):
    s_floor = Structure.create(structure_type, floor_plan)
    s = StatisticalStructure.create(s_floor, num_stories)
    s.build(mui_type)
    return s