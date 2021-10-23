

def _zpkbilinear(z, p, k, fs):
    "\n    Return a digital filter from an analog one using a bilinear transform.\n\n    Transform a set of poles and zeros from the analog s-plane to the digital\n    z-plane using Tustin's method, which substitutes ``(z-1) / (z+1)`` for\n    ``s``, maintaining the shape of the frequency response.\n\n    Parameters\n    ----------\n    z : array_like\n        Zeros of the analog IIR filter transfer function.\n    p : array_like\n        Poles of the analog IIR filter transfer function.\n    k : float\n        System gain of the analog IIR filter transfer function.\n    fs : float\n        Sample rate, as ordinary frequency (e.g. hertz). No prewarping is\n        done in this function.\n\n    Returns\n    -------\n    z : ndarray\n        Zeros of the transformed digital filter transfer function.\n    p : ndarray\n        Poles of the transformed digital filter transfer function.\n    k : float\n        System gain of the transformed digital filter.\n\n    "
    z = atleast_1d(z)
    p = atleast_1d(p)
    degree = _relative_degree(z, p)
    fs2 = (2.0 * fs)
    z_z = ((fs2 + z) / (fs2 - z))
    p_z = ((fs2 + p) / (fs2 - p))
    z_z = append(z_z, (- ones(degree)))
    k_z = (k * real((prod((fs2 - z)) / prod((fs2 - p)))))
    return (z_z, p_z, k_z)
