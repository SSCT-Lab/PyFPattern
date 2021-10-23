

def figure_edit(axes, parent=None):
    'Edit matplotlib figure options'
    sep = (None, None)
    (xmin, xmax) = map(float, axes.get_xlim())
    (ymin, ymax) = map(float, axes.get_ylim())
    general = [('Title', axes.get_title()), sep, (None, '<b>X-Axis</b>'), ('Left', xmin), ('Right', xmax), ('Label', axes.get_xlabel()), ('Scale', [axes.get_xscale(), 'linear', 'log', 'logit']), sep, (None, '<b>Y-Axis</b>'), ('Bottom', ymin), ('Top', ymax), ('Label', axes.get_ylabel()), ('Scale', [axes.get_yscale(), 'linear', 'log', 'logit']), sep, ('(Re-)Generate automatic legend', False)]
    xconverter = axes.xaxis.converter
    yconverter = axes.yaxis.converter
    xunits = axes.xaxis.get_units()
    yunits = axes.yaxis.get_units()

    def cmp_key(label):
        match = re.match('(_line|_image)(\\d+)', label)
        if match:
            return (match.group(1), int(match.group(2)))
        else:
            return (label, 0)
    linedict = {
        
    }
    for line in axes.get_lines():
        label = line.get_label()
        if (label == '_nolegend_'):
            continue
        linedict[label] = line
    curves = []

    def prepare_data(d, init):
        'Prepare entry for FormLayout.\n\n        `d` is a mapping of shorthands to style names (a single style may\n        have multiple shorthands, in particular the shorthands `None`,\n        `"None"`, `"none"` and `""` are synonyms); `init` is one shorthand\n        of the initial style.\n\n        This function returns an list suitable for initializing a\n        FormLayout combobox, namely `[initial_name, (shorthand,\n        style_name), (shorthand, style_name), ...]`.\n        '
        if (init not in d):
            d = {
                **d,
                init: str(init),
            }
        name2short = {name: short for (short, name) in d.items()}
        short2name = {short: name for (name, short) in name2short.items()}
        canonical_init = name2short[d[init]]
        return ([canonical_init] + sorted(short2name.items(), key=(lambda short_and_name: short_and_name[1])))
    curvelabels = sorted(linedict, key=cmp_key)
    for label in curvelabels:
        line = linedict[label]
        color = mcolors.to_hex(mcolors.to_rgba(line.get_color(), line.get_alpha()), keep_alpha=True)
        ec = mcolors.to_hex(mcolors.to_rgba(line.get_markeredgecolor(), line.get_alpha()), keep_alpha=True)
        fc = mcolors.to_hex(mcolors.to_rgba(line.get_markerfacecolor(), line.get_alpha()), keep_alpha=True)
        curvedata = [('Label', label), sep, (None, '<b>Line</b>'), ('Line style', prepare_data(LINESTYLES, line.get_linestyle())), ('Draw style', prepare_data(DRAWSTYLES, line.get_drawstyle())), ('Width', line.get_linewidth()), ('Color (RGBA)', color), sep, (None, '<b>Marker</b>'), ('Style', prepare_data(MARKERS, line.get_marker())), ('Size', line.get_markersize()), ('Face color (RGBA)', fc), ('Edge color (RGBA)', ec)]
        curves.append([curvedata, label, ''])
    has_curve = bool(curves)
    imagedict = {
        
    }
    for image in axes.get_images():
        label = image.get_label()
        if (label == '_nolegend_'):
            continue
        imagedict[label] = image
    imagelabels = sorted(imagedict, key=cmp_key)
    images = []
    cmaps = [(cmap, name) for (name, cmap) in sorted(cm.cmap_d.items())]
    for label in imagelabels:
        image = imagedict[label]
        cmap = image.get_cmap()
        if (cmap not in cm.cmap_d.values()):
            cmaps = ([(cmap, cmap.name)] + cmaps)
        (low, high) = image.get_clim()
        imagedata = [('Label', label), ('Colormap', ([cmap.name] + cmaps)), ('Min. value', low), ('Max. value', high), ('Interpolation', ([image.get_interpolation()] + [(name, name) for name in sorted(mimage.interpolations_names)]))]
        images.append([imagedata, label, ''])
    has_image = bool(images)
    datalist = [(general, 'Axes', '')]
    if curves:
        datalist.append((curves, 'Curves', ''))
    if images:
        datalist.append((images, 'Images', ''))

    def apply_callback(data):
        'This function will be called to apply changes'
        orig_xlim = axes.get_xlim()
        orig_ylim = axes.get_ylim()
        general = data.pop(0)
        curves = (data.pop(0) if has_curve else [])
        images = (data.pop(0) if has_image else [])
        if data:
            raise ValueError('Unexpected field')
        (title, xmin, xmax, xlabel, xscale, ymin, ymax, ylabel, yscale, generate_legend) = general
        if (axes.get_xscale() != xscale):
            axes.set_xscale(xscale)
        if (axes.get_yscale() != yscale):
            axes.set_yscale(yscale)
        axes.set_title(title)
        axes.set_xlim(xmin, xmax)
        axes.set_xlabel(xlabel)
        axes.set_ylim(ymin, ymax)
        axes.set_ylabel(ylabel)
        axes.xaxis.converter = xconverter
        axes.yaxis.converter = yconverter
        axes.xaxis.set_units(xunits)
        axes.yaxis.set_units(yunits)
        axes.xaxis._update_axisinfo()
        axes.yaxis._update_axisinfo()
        for (index, curve) in enumerate(curves):
            line = linedict[curvelabels[index]]
            (label, linestyle, drawstyle, linewidth, color, marker, markersize, markerfacecolor, markeredgecolor) = curve
            line.set_label(label)
            line.set_linestyle(linestyle)
            line.set_drawstyle(drawstyle)
            line.set_linewidth(linewidth)
            rgba = mcolors.to_rgba(color)
            line.set_alpha(None)
            line.set_color(rgba)
            if (marker != 'none'):
                line.set_marker(marker)
                line.set_markersize(markersize)
                line.set_markerfacecolor(markerfacecolor)
                line.set_markeredgecolor(markeredgecolor)
        for (index, image_settings) in enumerate(images):
            image = imagedict[imagelabels[index]]
            (label, cmap, low, high, interpolation) = image_settings
            image.set_label(label)
            image.set_cmap(cm.get_cmap(cmap))
            image.set_clim(*sorted([low, high]))
            image.set_interpolation(interpolation)
        if generate_legend:
            draggable = None
            ncol = 1
            if (axes.legend_ is not None):
                old_legend = axes.get_legend()
                draggable = (old_legend._draggable is not None)
                ncol = old_legend._ncol
            new_legend = axes.legend(ncol=ncol)
            if new_legend:
                new_legend.set_draggable(draggable)
        figure = axes.get_figure()
        figure.canvas.draw()
        if (not ((axes.get_xlim() == orig_xlim) and (axes.get_ylim() == orig_ylim))):
            figure.canvas.toolbar.push_current()
    data = _formlayout.fedit(datalist, title='Figure options', parent=parent, icon=get_icon('qt4_editor_options.svg'), apply=apply_callback)
    if (data is not None):
        apply_callback(data)
