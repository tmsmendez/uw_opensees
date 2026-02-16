import json
import os

import uw_opensees
from uw_opensees.structure import Structure
from uw_opensees.structure import FixedDisplacement
from uw_opensees.structure import PointLoad
from uw_opensees.structure import ISection, BoxSection, RectangularSection
from uw_opensees.structure import ElasticIsotropic
from uw_opensees.structure import ElementProperties
from uw_opensees.viewers import StructureViewer
from uw_opensees.utilities.geometry import length_vector, cross_vectors, subtract_vectors




def compute_max_disp(nodes, lines, fixed, visualize=True):
    path = uw_opensees.TEMP
    name = 'Arch598_model'

    s = Structure(path, name)

    el_keys = []
    for i, line in enumerate(lines):
        a, b = line
        a, b = nodes[a], nodes[b]
        v = subtract_vectors(a, b)
        normal = cross_vectors(v, [0,0,1])
        k = s.add_nodes_elements_from_lines([[a, b]], 'BeamElement', elset='beams_{}'.format(i), normal=normal)
        el_keys.append(k[0])

    s.add_set('beams', 'element', el_keys)

    fixed = [s.check_node_exists(nodes[fk]) for fk in fixed]
    d = FixedDisplacement('fixed', fixed)
    s.add(d)

    beam_section = BoxSection('beam_sec',  b=.05, h=.02, tw=.001, tf=.001)
    s.add(beam_section)

    clt_material = ElasticIsotropic('beam_mat', E=7e9, v=.42, p=500)
    s.add(clt_material)


    el_prop1 = ElementProperties('beams_elset',
                                material='beam_mat',
                                section='beam_sec',
                                elset='beams',
                                is_rad=False)
    s.add(el_prop1)

    all = range(s.node_count())

    load = PointLoad(name='pload', nodes=all, x=0, y=0, z=-10000/s.node_count(), xx=0, yy=0, zz=0)
    s.add(load)

    s.analyze_static(fields=['u'])

    if visualize:
        v = StructureViewer(s)
        v.static_scale = 0
        v.show('static')


    save_file=False
    if save_file:
        s.to_obj()

    xs = s.results['static'][0].displacements['ux']
    ys = s.results['static'][0].displacements['uy']
    zs = s.results['static'][0].displacements['uz']

    vls = []
    for i in range(len(xs)):
        vl = length_vector([xs[i], ys[i], zs[i]])
        vls.append(vl)
    return max(vls)


if __name__ == '__main__':

    import json
    from force_density import fd_numpy
    from force_density import nodes_edges_fixed_from_lines
    from force_density import plot_network


    for i in range(50): print('')


    filepath = '/Users/time/Documents/UW/02_teaching/00_courses/598_computational_design/2026/02_code/06_fdm_to_fea/data.json'

    with open(filepath, 'r') as file:
            data = json.load(file)

    lines = data['lines']
    fixed = data['fixed']


    nodes, edges, fixed = nodes_edges_fixed_from_lines(lines, fixed)

    nodes_ = fd_numpy(nodes, fixed, edges, loads=[0,0,.2])

    plot_network(nodes_, edges, fixed)

    max_disp = compute_max_disp(nodes_, edges, fixed, visualize=True)
    print('Maximum displacement = {}'.format(max_disp))