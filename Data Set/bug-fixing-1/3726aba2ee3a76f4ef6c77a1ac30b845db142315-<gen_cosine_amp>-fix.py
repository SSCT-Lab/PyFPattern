

def gen_cosine_amp(amp=100, period=1000, x0=0, xn=50000, step=1, k=0.0001):
    'Generates an absolute cosine time series with the amplitude\n    exponentially decreasing\n\n    Arguments:\n        amp: amplitude of the cosine function\n        period: period of the cosine function\n        x0: initial x of the time series\n        xn: final x of the time series\n        step: step of the time series discretization\n        k: exponential rate\n    '
    cos = np.zeros((((xn - x0) * step), 1, 1))
    for i in range(len(cos)):
        idx = (x0 + (i * step))
        cos[(i, 0, 0)] = (amp * np.cos((((2 * np.pi) * idx) / period)))
        cos[(i, 0, 0)] = (cos[(i, 0, 0)] * np.exp(((- k) * idx)))
    return cos
