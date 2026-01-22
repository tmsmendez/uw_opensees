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



def make_tower(w, l, h, num_s):
    columns = []
    beams = []
    braces = []

    for i in range(num_s):
        a = [0, 0, h * i]
        b = [w, 0, h * i]
        c = [w, l, h * i]
        d = [0, l, h * i]
        a_ = [0, 0, h * (i + 1)]
        b_ = [w, 0, h * (i + 1)]
        c_ = [w, l, h * (i + 1)]
        d_ = [0, l, h * (i + 1)]
        columns.extend([[a, a_], [b, b_], [c, c_], [d, d_]])
        beams.extend([[a_, b_], [b_, c_], [c_, d_], [d_, a_]])
        braces.extend([[a, b_], [b_, c,], [c, d_], [d_, a]])
    return columns, beams, braces

def compute_nat_freq(columns, beams, braces):
    path = uw_opensees.TEMP
    name = 'Arch598_modal'

    s = Structure(path, name)

    cols_k = s.add_nodes_elements_from_lines(columns, 'BeamElement', elset='columns', normal=[1, 0, 0])
    beam_k = s.add_nodes_elements_from_lines(beams, 'BeamElement', elset='beams', normal=[0, 0, 1])
    brce_k = s.add_nodes_elements_from_lines(braces, 'BeamElement', elset='braces', normal=[0, 0, 1])

    pts = [col[0] for col in columns[:4]]
    fixed = [s.check_node_exists(pt) for pt in pts]
    d = FixedDisplacement('corners', fixed)
    s.add(d)


    col_section = RectangularSection('col_sec',   b=.3, h=.3)
    beam_section = RectangularSection('beam_sec',  b=.15, h=.25)
    brace_section = RectangularSection('brace_sec',  b=.1, h=.1)
    s.add(col_section)
    s.add(beam_section)
    s.add(brace_section)

    clt_material = ElasticIsotropic('clt1', E=7e9, v=.42, p=500)
    s.add(clt_material)
    clt_material = ElasticIsotropic('clt2', E=7e9, v=.42, p=500)
    s.add(clt_material)
    clt_material = ElasticIsotropic('clt3', E=7e9, v=.42, p=500)
    s.add(clt_material)


    el_prop1 = ElementProperties('columns_elset',
                                material='clt1',
                                section='col_sec',
                                elset='columns',
                                is_rad=False)
    s.add(el_prop1)


    el_prop2 = ElementProperties('beams_elset',
                                material='clt2',
                                section='beam_sec',
                                elset='beams',
                                is_rad=False)
    s.add(el_prop2)





    el_prop3 = ElementProperties('braces_elset',
                                    material='clt3',
                                    section='brace_sec',
                                    elset='braces',
                                    is_rad=False)
    s.add(el_prop3)

    s.analyze_modal(backend='opensees', fields=['f', 'u'], num_modes=12, exe=exe)

    visualize = False
    if visualize:
        v = StructureViewer(s)
        v.show('modal')

    print_data= True
    if print_data:
        modes = s.results['modal'].keys()
        for mode in modes:
            f = s.results['modal'][mode].frequency
            m = s.results['modal'][mode].efmass['z']
            mr = s.results['modal'][mode].efmass_r['z']
            print(mode, f, m, mr)

    save_file=False
    if save_file:
        s.to_obj()

    print(s.results['modal'].keys())
    # return s.results['modal'][0].frequency

def compute_max_disp(columns, beams, braces):
    path = uw_opensees.TEMP
    name = 'Arch598_model'

    s = Structure(path, name)

    cols_k = s.add_nodes_elements_from_lines(columns, 'BeamElement', elset='columns', normal=[1, 0, 0])
    beam_k = s.add_nodes_elements_from_lines(beams, 'BeamElement', elset='beams', normal=[0, 0, 1])
    brce_k = s.add_nodes_elements_from_lines(braces, 'BeamElement', elset='braces', normal=[0, 0, 1])

    pts = [col[0] for col in columns[:4]]
    fixed = [s.check_node_exists(pt) for pt in pts]
    d = FixedDisplacement('corners', fixed)
    s.add(d)

    col_section = BoxSection('col_sec',   b=.3, h=.3, tw=.01, tf=.01)
    beam_section = BoxSection('beam_sec',  b=.15, h=.25, tw=.01, tf=.01)
    brace_section = BoxSection('brace_sec',  b=.1, h=.1, tw=.01, tf=.01)
    s.add(col_section)
    s.add(beam_section)
    s.add(brace_section)

    clt_material = ElasticIsotropic('clt1', E=7e9, v=.42, p=500)
    s.add(clt_material)
    clt_material = ElasticIsotropic('clt2', E=7e9, v=.42, p=500)
    s.add(clt_material)
    clt_material = ElasticIsotropic('clt3', E=7e9, v=.42, p=500)
    s.add(clt_material)


    el_prop1 = ElementProperties('columns_elset',
                                material='clt1',
                                section='col_sec',
                                elset='columns',
                                is_rad=False)
    s.add(el_prop1)


    el_prop2 = ElementProperties('beams_elset',
                                material='clt2',
                                section='beam_sec',
                                elset='beams',
                                is_rad=False)
    s.add(el_prop2)


    el_prop3 = ElementProperties('braces_elset',
                                    material='clt3',
                                    section='brace_sec',
                                    elset='braces',
                                    is_rad=False)
    s.add(el_prop3)

    load = PointLoad(name='pload', nodes=cols_k, x=-1000, y=0, z=0, xx=0, yy=0, zz=0)
    s.add(load)

    s.analyze_static(backend='opensees', fields=['u'], exe=exe)

    visualize = True
    if visualize:
        v = StructureViewer(s)
        v.static_scale = 20
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

    for i in range(50): print('')

    exe = '/Applications/OpenSees3.3.0/bin/OpenSees'

    w = 14
    l = 10
    h = 3
    num_s = 10

    co, be, br = make_tower(w, l, h, num_s)
    # compute_nat_freq(co, be, br)
    m = compute_max_disp(co, be, br)
    print(m)