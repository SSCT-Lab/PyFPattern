def switch_backend(newbackend):
    '\n    Close all open figures and set the Matplotlib backend.\n\n    The argument is case-insensitive.  Switching to an interactive backend is\n    possible only if no event loop for another interactive backend has started.\n    Switching to and from non-interactive backends is always possible.\n\n    Parameters\n    ----------\n    newbackend : str\n        The name of the backend to use.\n    '
    close('all')
    if (newbackend is rcsetup._auto_backend_sentinel):
        for candidate in ['macosx', 'qt5agg', 'qt4agg', 'gtk3agg', 'gtk3cairo', 'tkagg', 'wxagg', 'agg', 'cairo']:
            try:
                switch_backend(candidate)
            except ImportError:
                continue
            else:
                rcParamsOrig['backend'] = candidate
                return
    backend_name = (newbackend[9:] if newbackend.startswith('module://') else 'matplotlib.backends.backend_{}'.format(newbackend.lower()))
    backend_mod = importlib.import_module(backend_name)
    Backend = type('Backend', (matplotlib.backends._Backend,), vars(backend_mod))
    _log.debug('Loaded backend %s version %s.', newbackend, Backend.backend_version)
    required_framework = Backend.required_interactive_framework
    if (required_framework is not None):
        current_framework = matplotlib.backends._get_running_interactive_framework()
        if (current_framework and required_framework and (current_framework != required_framework)):
            raise ImportError('Cannot load backend {!r} which requires the {!r} interactive framework, as {!r} is currently running'.format(newbackend, required_framework, current_framework))
    rcParams['backend'] = rcParamsDefault['backend'] = newbackend
    global _backend_mod, new_figure_manager, draw_if_interactive, _show
    _backend_mod = backend_mod
    new_figure_manager = Backend.new_figure_manager
    draw_if_interactive = Backend.draw_if_interactive
    _show = Backend.show
    matplotlib.backends.backend = newbackend