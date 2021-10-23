def _weights(x, dx=1, orig=0):
    x = np.ravel(x)
    floor_x = np.floor(((x - orig) / dx))
    alpha = (((x - orig) - (floor_x * dx)) / dx)
    return (np.hstack((floor_x, (floor_x + 1))), np.hstack(((1 - alpha), alpha)))