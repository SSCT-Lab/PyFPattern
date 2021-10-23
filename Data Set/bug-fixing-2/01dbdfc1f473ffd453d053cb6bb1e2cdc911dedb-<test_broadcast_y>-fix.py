

def test_broadcast_y(self):
    xdata = np.arange(10)
    target = (((4.7 * (xdata ** 2)) + (3.5 * xdata)) + np.random.rand(len(xdata)))
    fit_func = (lambda x, a, b: (((a * (x ** 2)) + (b * x)) - target))
    for method in ['lm', 'trf', 'dogbox']:
        (popt0, pcov0) = curve_fit(fit_func, xdata=xdata, ydata=np.zeros_like(xdata), method=method)
        (popt1, pcov1) = curve_fit(fit_func, xdata=xdata, ydata=0, method=method)
        assert_allclose(pcov0, pcov1)
