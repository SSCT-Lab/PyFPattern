

def clip_evals(x, value=0):
    (evals, evecs) = np.linalg.eigh(x)
    clipped = np.any((evals < 0))
    x_new = np.dot((evecs * np.maximum(evals, value)), evecs.T)
    return (x_new, clipped)
