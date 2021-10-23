def deconvolve(signal, divisor):
    "Deconvolves ``divisor`` out of ``signal`` using inverse filtering.\n\n    Returns the quotient and remainder such that\n    ``signal = convolve(divisor, quotient) + remainder``\n\n    Parameters\n    ----------\n    signal : array_like\n        Signal data, typically a recorded signal\n    divisor : array_like\n        Divisor data, typically an impulse response or filter that was\n        applied to the original signal\n\n    Returns\n    -------\n    quotient : ndarray\n        Quotient, typically the recovered original signal\n    remainder : ndarray\n        Remainder\n\n    Examples\n    --------\n    Deconvolve a signal that's been filtered:\n\n    >>> from scipy import signal\n    >>> original = [0, 1, 0, 0, 1, 1, 0, 0]\n    >>> impulse_response = [2, 1]\n    >>> recorded = signal.convolve(impulse_response, original)\n    >>> recorded\n    array([0, 2, 1, 0, 2, 3, 1, 0, 0])\n    >>> recovered, remainder = signal.deconvolve(recorded, impulse_response)\n    >>> recovered\n    array([ 0.,  1.,  0.,  0.,  1.,  1.,  0.,  0.])\n\n    See Also\n    --------\n    numpy.polydiv : performs polynomial division (same operation, but\n                    also accepts poly1d objects)\n\n    "
    num = atleast_1d(signal)
    den = atleast_1d(divisor)
    N = len(num)
    D = len(den)
    if (D > N):
        quot = []
        rem = num
    else:
        input = zeros(((N - D) + 1), float)
        input[0] = 1
        quot = lfilter(num, den, input)
        rem = (num - convolve(den, quot, mode='full'))
    return (quot, rem)