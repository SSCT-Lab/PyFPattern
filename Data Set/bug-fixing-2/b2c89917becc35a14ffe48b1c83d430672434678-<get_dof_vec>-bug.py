

@staticmethod
def get_dof_vec(tri_z, tri_dz, J):
    '\n        Computes the dof vector of a triangle, knowing the value of f, df and\n        of the local Jacobian at each node.\n\n        *tri_z*: array of shape (3,) of f nodal values\n        *tri_dz*: array of shape (3,2) of df/dx, df/dy nodal values\n        *J*: Jacobian matrix in local basis of apex 0\n\n        Returns dof array of shape (9,) so that for each apex iapex:\n            dof[iapex*3+0] = f(Ai)\n            dof[iapex*3+1] = df(Ai).(AiAi+)\n            dof[iapex*3+2] = df(Ai).(AiAi-)]\n        '
    npt = tri_z.shape[0]
    dof = np.zeros([npt, 9], dtype=np.float64)
    J1 = _prod_vectorized(_ReducedHCT_Element.J0_to_J1, J)
    J2 = _prod_vectorized(_ReducedHCT_Element.J0_to_J2, J)
    col0 = _prod_vectorized(J, np.expand_dims(tri_dz[:, 0, :], axis=3))
    col1 = _prod_vectorized(J1, np.expand_dims(tri_dz[:, 1, :], axis=3))
    col2 = _prod_vectorized(J2, np.expand_dims(tri_dz[:, 2, :], axis=3))
    dfdksi = _to_matrix_vectorized([[col0[:, 0, 0], col1[:, 0, 0], col2[:, 0, 0]], [col0[:, 1, 0], col1[:, 1, 0], col2[:, 1, 0]]])
    dof[:, 0:7:3] = tri_z
    dof[:, 1:8:3] = dfdksi[:, 0]
    dof[:, 2:9:3] = dfdksi[:, 1]
    return dof
