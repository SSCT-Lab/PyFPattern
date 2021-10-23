def random_color_distort(src, brightness_delta=32, contrast_low=0.5, contrast_high=1.5, saturation_low=0.5, saturation_high=1.5, hue_delta=18):
    'Randomly distort image color space.\n    Note that input image should in original range [0, 255].\n\n    Parameters\n    ----------\n    src : mxnet.nd.NDArray\n        Input image as HWC format.\n    brightness_delta : int\n        Maximum brightness delta. Defaults to 32.\n    contrast_low : float\n        Lowest contrast. Defaults to 0.5.\n    contrast_high : float\n        Highest contrast. Defaults to 1.5.\n    saturation_low : float\n        Lowest saturation. Defaults to 0.5.\n    saturation_high : float\n        Highest saturation. Defaults to 1.5.\n    hue_delta : int\n        Maximum hue delta. Defaults to 18.\n\n    Returns\n    -------\n    mxnet.nd.NDArray\n        Distorted image in HWC format.\n\n    '

    def brightness(src, delta, p=0.5):
        'Brightness distortion.'
        if (np.random.uniform(0, 1) > p):
            delta = np.random.uniform((- delta), delta)
            src += delta
            return src
        return src

    def contrast(src, low, high, p=0.5):
        'Contrast distortion'
        if (np.random.uniform(0, 1) > p):
            alpha = np.random.uniform(low, high)
            src *= alpha
            return src
        return src

    def saturation(src, low, high, p=0.5):
        'Saturation distortion.'
        if (np.random.uniform(0, 1) > p):
            alpha = np.random.uniform(low, high)
            gray = (src * nd.array([[[0.299, 0.587, 0.114]]], ctx=src.context))
            gray = mx.nd.sum(gray, axis=2, keepdims=True)
            gray *= (1.0 - alpha)
            src *= alpha
            src += gray
            return src
        return src

    def hue(src, delta, p=0.5):
        'Hue distortion'
        if (np.random.uniform(0, 1) > p):
            alpha = random.uniform((- delta), delta)
            u = np.cos((alpha * np.pi))
            w = np.sin((alpha * np.pi))
            bt = np.array([[1.0, 0.0, 0.0], [0.0, u, (- w)], [0.0, w, u]])
            tyiq = np.array([[0.299, 0.587, 0.114], [0.596, (- 0.274), (- 0.321)], [0.211, (- 0.523), 0.311]])
            ityiq = np.array([[1.0, 0.956, 0.621], [1.0, (- 0.272), (- 0.647)], [1.0, (- 1.107), 1.705]])
            t = np.dot(np.dot(ityiq, bt), tyiq).T
            src = nd.dot(src, nd.array(t, ctx=src.context))
            return src
        return src
    src = src.astype('float32')
    src = brightness(src, brightness_delta)
    if np.random.randint(0, 2):
        src = contrast(src, contrast_low, contrast_high)
        src = saturation(src, saturation_low, saturation_high)
        src = hue(src, hue_delta)
    else:
        src = saturation(src, saturation_low, saturation_high)
        src = hue(src, hue_delta)
        src = contrast(src, contrast_low, contrast_high)
    return src