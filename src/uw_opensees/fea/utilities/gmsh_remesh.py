
try:
    import gmsh
    import numpy as np
except:
    pass


from uw_opensees.utilities.geometry import geometric_key
from uw_opensees.utilities.geometry import Mesh
# from compas.datastructures import meshes_join
# from compas.datastructures import mesh_weld

class GMSH(object):
    def __init__(self, mesh, size):
        self.mesh = mesh
        self.lc = size
        self.half_edges = {}
        
    def remesh(self):
        gmsh.initialize(['-noenv'])
        # gmsh.
        gmsh.model.add(self.mesh.name)

        self.gmsh_add_points()
        self.gmsh_add_lines()
        self.gmsh_add_curve_loops()
        self.gmsh_add_plane_surfaces()

        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(2)
        gmsh.option.setNumber("Mesh.Algorithm", 8)

        v = gmsh.model.mesh.get_nodes()[1]
        f = gmsh.model.mesh.getElementFaceNodes(2, 3)
        f = [f[i].item() for i in f]


        _, node_coords, _ = gmsh.model.mesh.getNodes()
        vertices = np.array(node_coords).reshape(-1, 3)

        # --- Triangles ---
        _, elem_node_tags = gmsh.model.mesh.getElementsByType(2)  # 2 = triangle

        faces = np.array(elem_node_tags).reshape(-1, 3) - 1 
        faces = [f.tolist() for f in faces]

        # gmsh.fltk.run()

        self.mesh = Mesh.from_vertices_and_faces(vertices, faces)
        gmsh.finalize()
        
    def gmsh_add_points(self):
        for vk in self.mesh.vertices:
            x, y, z = self.mesh.vertex_coordinates(vk)
            gmsh.model.geo.add_point(x, y, z, self.lc, vk)

    def gmsh_add_lines(self):
        for i, (u, v) in enumerate(self.mesh.edges()):
            gmsh.model.geo.add_line(u, v, i + 1)
            self.half_edges[(u, v)] = str(i + 1)
            self.half_edges[(v, u)] = '-{}'.format(i + 1)

    def gmsh_add_curve_loops(self):
        for fk in self.mesh.faces:
            v = self.mesh.face_vertices(fk)
            ek = [self.half_edges[v[-i], v[-i - 1]] for i in range(len(v))]
            a = gmsh.model.geo.add_curve_loop(ek, fk + 1)

    def gmsh_add_plane_surfaces(self):
        for fk in self.mesh.faces:
            if len(self.mesh.face_vertices(fk)) > 4:
                gmsh.model.geo.addPlaneSurface([fk + 1], fk + 1)
            else:
                gmsh.model.geo.addSurfaceFilling([fk + 1], fk + 1)


def remesh_mesh(mesh, size):
    gm = GMSH(mesh, size)
    gm.remesh()
    rmesh = gm.mesh

    cpt_dict = {}

    for fk in mesh.faces:
        d = {geometric_key(rmesh.face_centroid(fk_)): fk for fk_ in rmesh.faces}
        cpt_dict.update(d)

    # for fk in rmesh.faces:
    #     gk = geometric_key(rmesh.face_centroid(fk))
    #     rmesh.face_attribute(fk, 'set', cpt_dict[gk])
    #     rmesh.face_attribute(fk, 'is_boundary', mesh.face_attribute(cpt_dict[gk],'is_boundary'))
    #     rmesh.face_attribute(fk, 'is_fin', mesh.face_attribute(cpt_dict[gk],'is_fin'))


    return rmesh

def remesh_vertices_faces(vertices, faces, size):
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    gm = GMSH(mesh, size)
    gm.remesh()
    return gm.mesh.to_vertices_and_faces()

def remesh_face_by_face(mesh, size, weld=True):
    rmeshes = []
    cpt_dict = {}

    for fk in mesh.face:
        vertices = [mesh.vertex_coordinates(vk) for vk in mesh.face_vertices(fk)]
        faces = [range(len(vertices))]
        fmesh = Mesh.from_vertices_and_faces(vertices, faces)
        rmesh = remesh_mesh(fmesh, size)
        rmeshes.append(rmesh)
        d = {geometric_key(rmesh.face_centroid(fk_)): fk for fk_ in rmesh.face}
        cpt_dict.update(d)

    if weld:
        rmesh = meshes_join(rmeshes)
        rmesh = mesh_weld(rmesh)

        for fk in rmesh.face:
            gk = geometric_key(rmesh.face_centroid(fk))
            # for att in mesh.face_attributes(cpt_dict[gk]):
            #     rmesh.face_attribute(fk, att, mesh.face_attribute(cpt_dict[gk],att))
            rmesh.face_attribute(fk, 'set', cpt_dict[gk])
            rmesh.face_attribute(fk, 'is_boundary', mesh.face_attribute(cpt_dict[gk],'is_boundary'))
            rmesh.face_attribute(fk, 'is_fin', mesh.face_attribute(cpt_dict[gk],'is_fin'))

        return rmesh
    else:
        return rmeshes


if __name__ == '__main__':
    pass
