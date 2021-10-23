def key_press_handler(event, canvas, toolbar=None):
    '\n    Implement the default mpl key bindings for the canvas and toolbar\n    described at :ref:`key-event-handling`\n\n    Parameters\n    ----------\n    event : :class:`KeyEvent`\n        a key press/release event\n    canvas : :class:`FigureCanvasBase`\n        the backend-specific canvas instance\n    toolbar : :class:`NavigationToolbar2`\n        the navigation cursor toolbar\n\n    '
    if (event.key is None):
        return
    fullscreen_keys = rcParams['keymap.fullscreen']
    home_keys = rcParams['keymap.home']
    back_keys = rcParams['keymap.back']
    forward_keys = rcParams['keymap.forward']
    pan_keys = rcParams['keymap.pan']
    zoom_keys = rcParams['keymap.zoom']
    save_keys = rcParams['keymap.save']
    quit_keys = rcParams['keymap.quit']
    grid_keys = rcParams['keymap.grid']
    grid_minor_keys = rcParams['keymap.grid_minor']
    toggle_yscale_keys = rcParams['keymap.yscale']
    toggle_xscale_keys = rcParams['keymap.xscale']
    all_keys = rcParams['keymap.all_axes']
    if (event.key in fullscreen_keys):
        try:
            canvas.manager.full_screen_toggle()
        except AttributeError:
            pass
    if (event.key in quit_keys):
        Gcf.destroy_fig(canvas.figure)
    if (toolbar is not None):
        if (event.key in home_keys):
            toolbar.home()
        elif (event.key in back_keys):
            toolbar.back()
        elif (event.key in forward_keys):
            toolbar.forward()
        elif (event.key in pan_keys):
            toolbar.pan()
            toolbar._set_cursor(event)
        elif (event.key in zoom_keys):
            toolbar.zoom()
            toolbar._set_cursor(event)
        elif (event.key in save_keys):
            toolbar.save_figure()
    if (event.inaxes is None):
        return

    def _get_uniform_gridstate(ticks):
        if all((tick.gridOn for tick in ticks)):
            return True
        elif (not any((tick.gridOn for tick in ticks))):
            return False
        else:
            return None
    ax = event.inaxes
    if ((event.key in grid_keys) and (None not in [_get_uniform_gridstate(ax.xaxis.minorTicks), _get_uniform_gridstate(ax.yaxis.minorTicks)])):
        x_state = _get_uniform_gridstate(ax.xaxis.majorTicks)
        y_state = _get_uniform_gridstate(ax.yaxis.majorTicks)
        cycle = [(False, False), (True, False), (True, True), (False, True)]
        try:
            (x_state, y_state) = cycle[((cycle.index((x_state, y_state)) + 1) % len(cycle))]
        except ValueError:
            pass
        else:
            ax.grid(x_state, which=('major' if x_state else 'both'), axis='x')
            ax.grid(y_state, which=('major' if y_state else 'both'), axis='y')
            canvas.draw_idle()
    if ((event.key in grid_minor_keys) and (None not in [_get_uniform_gridstate(ax.xaxis.majorTicks), _get_uniform_gridstate(ax.yaxis.majorTicks)])):
        x_state = _get_uniform_gridstate(ax.xaxis.minorTicks)
        y_state = _get_uniform_gridstate(ax.yaxis.minorTicks)
        cycle = [(False, False), (True, False), (True, True), (False, True)]
        try:
            (x_state, y_state) = cycle[((cycle.index((x_state, y_state)) + 1) % len(cycle))]
        except ValueError:
            pass
        else:
            ax.grid(x_state, which='both', axis='x')
            ax.grid(y_state, which='both', axis='y')
            canvas.draw_idle()
    elif (event.key in toggle_yscale_keys):
        scale = ax.get_yscale()
        if (scale == 'log'):
            ax.set_yscale('linear')
            ax.figure.canvas.draw_idle()
        elif (scale == 'linear'):
            try:
                ax.set_yscale('log')
            except ValueError as exc:
                warnings.warn(str(exc))
                ax.set_yscale('linear')
            ax.figure.canvas.draw_idle()
    elif (event.key in toggle_xscale_keys):
        scalex = ax.get_xscale()
        if (scalex == 'log'):
            ax.set_xscale('linear')
            ax.figure.canvas.draw_idle()
        elif (scalex == 'linear'):
            try:
                ax.set_xscale('log')
            except ValueError as exc:
                warnings.warn(str(exc))
                ax.set_xscale('linear')
            ax.figure.canvas.draw_idle()
    elif ((event.key.isdigit() and (event.key != '0')) or (event.key in all_keys)):
        if (not (event.key in all_keys)):
            n = (int(event.key) - 1)
        for (i, a) in enumerate(canvas.figure.get_axes()):
            if ((event.x is not None) and (event.y is not None) and a.in_axes(event)):
                if (event.key in all_keys):
                    a.set_navigate(True)
                else:
                    a.set_navigate((i == n))