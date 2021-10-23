@deprecate_kwarg(old_arg_name='data', new_arg_name='frame')
def andrews_curves(frame, class_column, ax=None, samples=200, color=None, colormap=None, **kwds):
    '\n    Generates a matplotlib plot of Andrews curves, for visualising clusters of\n    multivariate data.\n\n    Andrews curves have the functional form:\n\n    f(t) = x_1/sqrt(2) + x_2 sin(t) + x_3 cos(t) +\n           x_4 sin(2t) + x_5 cos(2t) + ...\n\n    Where x coefficients correspond to the values of each dimension and t is\n    linearly spaced between -pi and +pi. Each row of frame then corresponds to\n    a single curve.\n\n    Parameters:\n    -----------\n    frame : DataFrame\n        Data to be plotted, preferably normalized to (0.0, 1.0)\n    class_column : Name of the column containing class names\n    ax : matplotlib axes object, default None\n    samples : Number of points to plot in each curve\n    color: list or tuple, optional\n        Colors to use for the different classes\n    colormap : str or matplotlib colormap object, default None\n        Colormap to select colors from. If string, load colormap with that name\n        from matplotlib.\n    kwds: keywords\n        Options to pass to matplotlib plotting method\n\n    Returns:\n    --------\n    ax: Matplotlib axis object\n\n    '
    from math import sqrt, pi
    import matplotlib.pyplot as plt

    def function(amplitudes):

        def f(t):
            x1 = amplitudes[0]
            result = (x1 / sqrt(2.0))
            coeffs = np.delete(np.copy(amplitudes), 0)
            coeffs.resize(int(((coeffs.size + 1) / 2)), 2)
            harmonics = (np.arange(0, coeffs.shape[0]) + 1)
            trig_args = np.outer(harmonics, t)
            result += np.sum(((coeffs[:, 0, np.newaxis] * np.sin(trig_args)) + (coeffs[:, 1, np.newaxis] * np.cos(trig_args))), axis=0)
            return result
        return f
    n = len(frame)
    class_col = frame[class_column]
    classes = frame[class_column].drop_duplicates()
    df = frame.drop(class_column, axis=1)
    t = np.linspace((- pi), pi, samples)
    used_legends = set([])
    color_values = _get_standard_colors(num_colors=len(classes), colormap=colormap, color_type='random', color=color)
    colors = dict(zip(classes, color_values))
    if (ax is None):
        ax = plt.gca(xlim=((- pi), pi))
    for i in range(n):
        row = df.iloc[i].values
        f = function(row)
        y = f(t)
        kls = class_col.iat[i]
        label = pprint_thing(kls)
        if (label not in used_legends):
            used_legends.add(label)
            ax.plot(t, y, color=colors[kls], label=label, **kwds)
        else:
            ax.plot(t, y, color=colors[kls], **kwds)
    ax.legend(loc='upper right')
    ax.grid()
    return ax