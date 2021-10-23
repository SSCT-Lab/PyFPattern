

def figure_edit(axes, parent=None):
    'Edit matplotlib figure options'
    sep = (None, None)
    has_curve = (len(axes.get_lines()) > 0)
    (xmin, xmax) = axes.get_xlim()
    (ymin, ymax) = axes.get_ylim()
    general = [('Title', axes.get_title()), sep, (None, '<b>X-Axis</b>'), ('Min', xmin), ('Max', xmax), ('Label', axes.get_xlabel()), ('Scale', [axes.get_xscale(), 'linear', 'log']), sep, (None, '<b>Y-Axis</b>'), ('Min', ymin), ('Max', ymax), ('Label', axes.get_ylabel()), ('Scale', [axes.get_yscale(), 'linear', 'log']), sep, ('(Re-)Generate automatic legend', False)]
    xconverter = axes.xaxis.converter
    yconverter = axes.yaxis.converter
    xunits = axes.xaxis.get_units()
    yunits = axes.yaxis.get_units()
    if has_curve:
        linedict = {
            
        }
        for line in axes.get_lines():
            label = line.get_label()
            if (label == '_nolegend_'):
                continue
            linedict[label] = line
        curves = []
        linestyles = list(six.iteritems(LINESTYLES))
        drawstyles = list(six.iteritems(DRAWSTYLES))
        markers = list(six.iteritems(MARKERS))
        curvelabels = sorted(linedict.keys())
        for label in curvelabels:
            line = linedict[label]
            color = rgb2hex(colorConverter.to_rgb(line.get_color()))
            ec = rgb2hex(colorConverter.to_rgb(line.get_markeredgecolor()))
            fc = rgb2hex(colorConverter.to_rgb(line.get_markerfacecolor()))
            curvedata = [('Label', label), sep, (None, '<b>Line</b>'), ('Line Style', ([line.get_linestyle()] + linestyles)), ('Draw Style', ([line.get_drawstyle()] + drawstyles)), ('Width', line.get_linewidth()), ('Color', color), sep, (None, '<b>Marker</b>'), ('Style', ([line.get_marker()] + markers)), ('Size', line.get_markersize()), ('Facecolor', fc), ('Edgecolor', ec)]
            curves.append([curvedata, label, ''])
        has_curve = bool(curves)
    datalist = [(general, 'Axes', '')]
    if has_curve:
        datalist.append((curves, 'Curves', ''))

    def apply_callback(data):
        'This function will be called to apply changes'
        if has_curve:
            (general, curves) = data
        else:
            (general,) = data
        (title, xmin, xmax, xlabel, xscale, ymin, ymax, ylabel, yscale, generate_legend) = general
        axes.set_xscale(xscale)
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
        if has_curve:
            for (index, curve) in enumerate(curves):
                line = linedict[curvelabels[index]]
                (label, linestyle, drawstyle, linewidth, color, marker, markersize, markerfacecolor, markeredgecolor) = curve
                line.set_label(label)
                line.set_linestyle(linestyle)
                line.set_drawstyle(drawstyle)
                line.set_linewidth(linewidth)
                line.set_color(color)
                if (marker is not 'none'):
                    line.set_marker(marker)
                    line.set_markersize(markersize)
                    line.set_markerfacecolor(markerfacecolor)
                    line.set_markeredgecolor(markeredgecolor)
        if generate_legend:
            draggable = None
            ncol = 1
            if (axes.legend_ is not None):
                old_legend = axes.get_legend()
                draggable = (old_legend._draggable is not None)
                ncol = old_legend._ncol
            new_legend = axes.legend(ncol=ncol)
            if new_legend:
                new_legend.draggable(draggable)
        figure = axes.get_figure()
        figure.canvas.draw()
    data = formlayout.fedit(datalist, title='Figure options', parent=parent, icon=get_icon('qt4_editor_options.svg'), apply=apply_callback)
    if (data is not None):
        apply_callback(data)
