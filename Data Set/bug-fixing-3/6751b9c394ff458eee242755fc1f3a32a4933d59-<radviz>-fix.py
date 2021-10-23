def radviz(frame, class_column, ax=None, color=None, colormap=None, **kwds):
    'RadViz - a multivariate data visualization algorithm\n\n    Parameters\n    ----------\n    frame: DataFrame\n    class_column: str\n        Column name containing class names\n    ax: Matplotlib axis object, optional\n    color: list or tuple, optional\n        Colors to use for the different classes\n    colormap : str or matplotlib colormap object, default None\n        Colormap to select colors from. If string, load colormap with that name\n        from matplotlib.\n    kwds: keywords\n        Options to pass to matplotlib scatter plotting method\n\n    Returns\n    -------\n    ax: Matplotlib axis object\n    '
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    def normalize(series):
        a = min(series)
        b = max(series)
        return ((series - a) / (b - a))
    n = len(frame)
    classes = frame[class_column].drop_duplicates()
    class_col = frame[class_column]
    df = frame.drop(class_column, axis=1).apply(normalize)
    if (ax is None):
        ax = plt.gca(xlim=[(- 1), 1], ylim=[(- 1), 1])
    to_plot = {
        
    }
    colors = _get_standard_colors(num_colors=len(classes), colormap=colormap, color_type='random', color=color)
    for kls in classes:
        to_plot[kls] = [[], []]
    m = (len(frame.columns) - 1)
    s = np.array([(np.cos(t), np.sin(t)) for t in [((2.0 * np.pi) * (i / float(m))) for i in range(m)]])
    for i in range(n):
        row = df.iloc[i].values
        row_ = np.repeat(np.expand_dims(row, axis=1), 2, axis=1)
        y = ((s * row_).sum(axis=0) / row.sum())
        kls = class_col.iat[i]
        to_plot[kls][0].append(y[0])
        to_plot[kls][1].append(y[1])
    for (i, kls) in enumerate(classes):
        ax.scatter(to_plot[kls][0], to_plot[kls][1], color=colors[i], label=pprint_thing(kls), **kwds)
    ax.legend()
    ax.add_patch(patches.Circle((0.0, 0.0), radius=1.0, facecolor='none'))
    for (xy, name) in zip(s, df.columns):
        ax.add_patch(patches.Circle(xy, radius=0.025, facecolor='gray'))
        if ((xy[0] < 0.0) and (xy[1] < 0.0)):
            ax.text((xy[0] - 0.025), (xy[1] - 0.025), name, ha='right', va='top', size='small')
        elif ((xy[0] < 0.0) and (xy[1] >= 0.0)):
            ax.text((xy[0] - 0.025), (xy[1] + 0.025), name, ha='right', va='bottom', size='small')
        elif ((xy[0] >= 0.0) and (xy[1] < 0.0)):
            ax.text((xy[0] + 0.025), (xy[1] - 0.025), name, ha='left', va='top', size='small')
        elif ((xy[0] >= 0.0) and (xy[1] >= 0.0)):
            ax.text((xy[0] + 0.025), (xy[1] + 0.025), name, ha='left', va='bottom', size='small')
    ax.axis('equal')
    return ax