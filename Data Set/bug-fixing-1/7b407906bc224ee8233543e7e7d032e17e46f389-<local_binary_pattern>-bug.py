

def local_binary_pattern(image, P, R, method='default'):
    "Gray scale and rotation invariant LBP (Local Binary Patterns).\n\n    LBP is an invariant descriptor that can be used for texture classification.\n\n    Parameters\n    ----------\n    image : (N, M) array\n        Graylevel image.\n    P : int\n        Number of circularly symmetric neighbour set points (quantization of\n        the angular space).\n    R : float\n        Radius of circle (spatial resolution of the operator).\n    method : {'default', 'ror', 'uniform', 'var'}\n        Method to determine the pattern.\n\n        * 'default': original local binary pattern which is gray scale but not\n            rotation invariant.\n        * 'ror': extension of default implementation which is gray scale and\n            rotation invariant.\n        * 'uniform': improved rotation invariance with uniform patterns and\n            finer quantization of the angular space which is gray scale and\n            rotation invariant.\n        * 'nri_uniform': non rotation-invariant uniform patterns variant\n            which is only gray scale invariant [2]_.\n        * 'var': rotation invariant variance measures of the contrast of local\n            image texture which is rotation but not gray scale invariant.\n\n    Returns\n    -------\n    output : (N, M) array\n        LBP image.\n\n    References\n    ----------\n    .. [1] Multiresolution Gray-Scale and Rotation Invariant Texture\n           Classification with Local Binary Patterns.\n           Timo Ojala, Matti Pietikainen, Topi Maenpaa.\n           http://www.rafbis.it/biplab15/images/stories/docenti/Danielriccio/Articoliriferimento/LBP.pdf, 2002.\n    .. [2] Face recognition with local binary patterns.\n           Timo Ahonen, Abdenour Hadid, Matti Pietikainen,\n           http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.214.6851,\n           2004.\n    "
    assert_nD(image, 2)
    methods = {
        'default': ord('D'),
        'ror': ord('R'),
        'uniform': ord('U'),
        'nri_uniform': ord('N'),
        'var': ord('V'),
    }
    image = np.ascontiguousarray(image, dtype=np.double)
    output = _local_binary_pattern(image, P, R, methods[method.lower()])
    return output
