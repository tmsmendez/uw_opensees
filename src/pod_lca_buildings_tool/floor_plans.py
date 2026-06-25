__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building import BuildingFloor
from pod_lca.units import Quantity as Q
from pod_lca.units import UNITS_MAP


def floor_plan_from_polyline(polyline, floor_to_floor, building_type):
    import rhinoscriptsyntax as rs

    rhino_unit = rs.UnitSystem()
    unit_map = {4: 'm', 9: 'ft', 8: 'in'}
    unit = UNITS_MAP[unit_map[rhino_unit]]
    floor_plan = []
    for pt in rs.PolylineVertices(polyline):
        x, y, z = pt
        floor_plan.append([Q(x, unit), Q(y, unit), Q(z, unit)])

    flr = BuildingFloor.from_floor_plan(floor_plan, floor_to_floor, building_type)
    return flr