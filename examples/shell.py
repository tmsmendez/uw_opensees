import uw_opensees
from uw_opensees.structure import Structure
from uw_opensees.structure import FixedDisplacement
from uw_opensees.structure import PointLoad
from uw_opensees.structure import ShellSection
from uw_opensees.structure import ElasticIsotropic
from uw_opensees.structure import ElementProperties
from uw_opensees.viewers import StructureViewer
from uw_opensees.fea import remesh_mesh

from uw_opensees.utilities.geometry import length_vector



def make_floor(w, l, a, b, h1, h2, h3):
    p0 = [0, 0, 0]
    p1 = [w, 0, 0]
    p2 = [w, l, 0]
    p3 = [0, l, 0]
    p4 = [w / 2., l * a, h2]
    p5 = [w - (w * b), l / 2., h1]
    p6 = [w / 2., l - (l * a), h2]
    p7 = [w * b, l /2., h1]
    p8 = [w / 2., l / 2., h3]

    f0 = [0, 1, 4]
    f1 = [1, 2, 5]
    f2 = [2, 3, 6]
    f3 = [3, 0, 7]
    f4 = [0, 4, 8]
    f5 = [1, 8, 4]
    f6 = [1, 5, 8]
    f7 = [2, 8, 5]
    f8 = [2, 6, 8]
    f9 = [3, 8, 6]
    f10 = [3, 7, 8]
    f11 = [0, 8, 7]

    vertices = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
    faces = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11]

    return vertices, faces

def compute_max_disp(mesh, thickness, visualize=True):
    """
    This function computes the maximum displacement of a structure made from
    a mesh. Boundary points are considered to be fixed supports.

    Parameters
    ----------

    mesh (object): A COMPAS mesh containing the geometry of the shell structure 
    to be studied.

    thickness (float): The thickness of the floor structure.

    Returns
    -------

    (float) The maximum displacement of the structure under the gravity loads
    """

    path = uw_opensees.TEMP
    name = 'opensees_shell_static'

    s = Structure(path, name)

    mesh = remesh_mesh(mesh, .4)


    # v = MeshViewer(mesh)
    # v.show_vertex_labels = False
    # v.show()

    s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='shell')

    # bound = mesh.vertices_on_boundary()
    bound = [0,1,2,3]


    d = FixedDisplacement('boundary', bound)
    s.add(d)

    section = ShellSection('shell_sec', t=thickness)
    s.add(section)

    material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
    s.add(material)


    el_prop = ElementProperties('concrete_shell',
                                material='concrete',
                                section='shell_sec',
                                elset='shell')
    s.add(el_prop)


    # s.add_gravity_from_mesh(mesh, thickness, 2400)

    nl = PointLoad('point_load', [8], z=-1000)
    s.add_load(nl)

    # if visualize:
    #     v = StructureViewer(s)
    #     v.show_node_labels = False
    #     v.show_point_loads = True
    #     v.show()


    s.analyze_static(fields=['u'])
    
    if visualize:
        v = StructureViewer(s)
        v.show_node_labels = True
        v.show_point_loads = True
        v.show('static')



    xs = s.results['static'][0].displacements['ux']
    ys = s.results['static'][0].displacements['uy']
    zs = s.results['static'][0].displacements['uz']


    vls = []
    for i in range(len(xs)):
        vl = length_vector([xs[i], ys[i], zs[i]])
        vls.append(vl)
    return max(vls)




for i in range(50): print('')

from uw_opensees.utilities.geometry import Mesh
from uw_opensees.viewers import MeshViewer

w = 20
l = 16
a = .3
b = .3
h1 = 1
h2 = 1
h3 = 1



vertices, faces = make_floor(w, l, a, b, h1, h2, h3)


mesh = Mesh.from_vertices_and_faces(vertices, faces)
print(mesh)

# v = MeshViewer(mesh)
# v.show_vertex_labels = True
# v.show()

thickness = .2
max_disp = compute_max_disp(mesh, thickness, visualize=True)
print(max_disp)
