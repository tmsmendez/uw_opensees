#r: numpy
#r: scipy

try:
    from scipy.sparse.linalg import spsolve
    from scipy.sparse import coo_matrix

    import numpy as np
    from numpy import asarray
    from numpy import atleast_2d
except:
    pass

def edge_topology_from_geometry(nodes, edges_):
    gkdict = {geometric_key(p): i for i, p in enumerate(nodes)}
    edges = []
    for a, b in edges_:
        a = gkdict[geometric_key(a)]
        b = gkdict[geometric_key(b)]
        edges.append((a,b))
    return edges

def nodes_edges_fixed_from_lines(lines, fixed):

    all_nodes = []
    for lk in lines:
        a, b = lines[lk]
        all_nodes.extend([tuple(a), tuple(b)])

    nodes = list(set(all_nodes))
    gkdict = {geometric_key(p): i for i, p in enumerate(nodes)}


    fixed = [gkdict[geometric_key(fixed[fk])] for fk in fixed]
    fixed = list(set(fixed))

    edges = []
    for lk in lines:
        a, b = lines[lk]
        a = gkdict[geometric_key(a)]
        b = gkdict[geometric_key(b)]
        if (a,b) not in edges:
            edges.append((a,b))
    return nodes, edges, fixed

def geometric_key(xyz, precision=3, sanitize=True):
    x, y, z = xyz

    if precision == 0:
        raise ValueError("Precision cannot be zero.")

    if precision == -1:
        return "{:d},{:d},{:d}".format(int(x), int(y), int(z))

    if precision < -1:
        precision = -precision - 1
        factor = 10**precision
        return "{:d},{:d},{:d}".format(
            int(round(x / factor) * factor),
            int(round(y / factor) * factor),
            int(round(z / factor) * factor),
        )

    if sanitize:
        minzero = "-{0:.{1}f}".format(0.0, precision)
        if "{0:.{1}f}".format(x, precision) == minzero:
            x = 0.0
        if "{0:.{1}f}".format(y, precision) == minzero:
            y = 0.0
        if "{0:.{1}f}".format(z, precision) == minzero:
            z = 0.0

    return "{0:.{3}f},{1:.{3}f},{2:.{3}f}".format(x, y, z, precision)

def connectivity_matrix(edges, rtype='array'):
    m = len(edges)
    data = np.array([-1] * m + [1] * m)
    rows = np.array(list(range(m)) + list(range(m)))
    cols = np.array([edge[0] for edge in edges] + [edge[1] for edge in edges])
    C = coo_matrix((data, (rows, cols))).asfptype()
    return C.toarray()

def fd_numpy(nodes, fixed, edges, loads= [0,0,0]):
    q = np.ones(len(edges)) * 1.0
    forcedensities = q.tolist()
    nodes_ = np.array(nodes)
    edges = np.array(edges)
    loads = [loads for _ in range(len(edges))]


    free = list(set(range(len(nodes_))) - set(fixed))
    xyz = asarray(nodes_, dtype=np.float64).reshape((-1, 3))
    C = connectivity_matrix(edges, "csr")
    Ci = C[:, free]
    Cf = C[:, fixed]
    q = asarray(forcedensities, dtype=np.float64).reshape((-1, 1))
    # Q = diags([q.flatten()], [0])
    Q = np.diag(q.flatten())
    p = np.zeros_like(xyz) if loads is None else asarray(loads, dtype=np.float64).reshape((-1, 3))

    A = C.T.dot(Q).dot(C)
    Ai = Ci.T.dot(Q).dot(Ci)
    Af = Ci.T.dot(Q).dot(Cf)

    b = p[free] - Af.dot(xyz[fixed])

    xyz[free] = spsolve(Ai, b)
    # lengths = normrow(C.dot(xyz))
    # forces = q * lengths
    # residuals = p - A.dot(xyz)
    # print(residuals)
    return xyz

def plot_network(nodes, edges, fixed):
    import plotly.graph_objects as go

    name = 'Force Density Network'
    title = '{0} - Structure'.format(name)
    layout = go.Layout(title=title,
                        scene=dict(aspectmode='data',
                                xaxis=dict(
                                            gridcolor='rgb(255, 255, 255)',
                                            zerolinecolor='rgb(255, 255, 255)',
                                            showbackground=False,
                                            showgrid=False,
                                            backgroundcolor='rgb(230, 230,230)'),
                                yaxis=dict(
                                            gridcolor='rgb(255, 255, 255)',
                                            zerolinecolor='rgb(255, 255, 255)',
                                            showbackground=False,
                                            showgrid=False,
                                            backgroundcolor='rgb(230, 230,230)'),
                                zaxis=dict(
                                            gridcolor='rgb(255, 255, 255)',
                                            zerolinecolor='rgb(255, 255, 255)',
                                            showbackground=False,
                                            showgrid=False,
                                            backgroundcolor='rgb(230, 230,230)')
                                ),
                        showlegend=True,
                        )

    line_marker = dict(color='rgb(0,0,0)', width=1.5)
    lines = []
    dots = []

    edges = [(nodes[a], nodes[b]) for a,b in edges]

    x, y, z = [], [],  []
    for u, v in edges:
        x.extend([u[0], v[0], [None]])
        y.extend([u[1], v[1], [None]])
        z.extend([u[2], v[2], [None]])
    lines = [go.Scatter3d(name='edges',
                          x=x,
                          y=y,
                          z=z,
                          mode='lines',
                          line=line_marker,
                          legendgroup='Beam Elements',
                          )]

    x = [nodes[i][0] for i in fixed]
    y = [nodes[i][1] for i in fixed]
    z = [nodes[i][2] for i in fixed]

    dots.append(go.Scatter3d(name='fixed',
                            x=x,
                            y=y,
                            z=z,
                            mode='markers',
                            # marker_color=colors,
                            # marker={'color': 'red'',
                            #         'cmax': self.kmax,
                            #         'cmin':self.kmin,
                            #         'colorscale': 'jet',
                            #         'colorbar': {'thickness': 20, 'x': 0},
                            # },
                            # text=text,
                            # hoverinfo='text',
                            ))

    data = []
    data.extend(lines)
    data.extend(dots)

    fig = go.Figure(data=data, layout=layout)
    fig.show()

def rhino_draw_network(nodes, edges, fixed):
    import rhinoscriptsyntax as rs
    lines = []
    for a, b in edges:
        a = nodes[a]
        b = nodes[b]
        lines.append(rs.AddLine(a, b))
    return lines


if __name__ == '__main__':
    import numpy as np
    for i in range(50): print('')

    nx = 10
    ny = 20
    dx = 1
    dy = 1

    nodes = []
    mat = []
    for i in range(nx):
        col = []
        for j in range(ny):
            if i ==0 or i==nx-1:
                z = 0
            else:
                z = 0
            col.append([i*dx, j*dy, z])
            nodes.append([i*dx, j*dy, z])
        mat.append(col)

    edges_ = []
    for i in range(len(mat)):
        for j in range(len(mat[0]) - 1):
            a = mat[i][j]
            b = mat[i][j+1]
            edges_.append([a,b])
    
    for i in range(len(mat)-1):
        for j in range(len(mat[0])):
            a = mat[i][j]
            b = mat[i+1][j]
            edges_.append([a,b])


    edges = edge_topology_from_geometry(nodes, edges_)

    q = np.ones(len(edges)) * 1.0
    q = q.tolist()

    fixed = []
    for i, n in enumerate(nodes):
        if n[0] == 0:
            fixed.append(i)
        if n[0] >= (nx-1) * dx:
            fixed.append(i)
        if n[1] == 0:
            fixed.append(i)
        if n[1] >= (ny-1) * dy:
            fixed.append(i)

    nodes = np.array(nodes)
    edges = np.array(edges)
    loads = [[0,0,0.5] for _ in range(len(edges))]
    xyz = fd_numpy(nodes, fixed, edges, q,loads)
    # lines = rhino_draw_network(xyz, edges, fixed)
    plot_network(xyz, edges, fixed)

