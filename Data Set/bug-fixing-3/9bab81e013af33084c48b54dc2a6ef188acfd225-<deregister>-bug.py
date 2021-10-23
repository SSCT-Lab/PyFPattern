def deregister():
    "\n    Remove pandas' formatters and converters\n\n    Removes the custom converters added by :func:`register`. This\n    attempts to set the state of the registry back to the state before\n    pandas registered its own units. Converters for pandas' own types like\n    Timestamp and Period are removed completely. Converters for types\n    pandas overwrites, like ``datetime.datetime``, are restored to their\n    original value.\n\n    See Also\n    --------\n    deregister_matplotlib_converters\n    "
    plot_backend = _get_plot_backend('matplotlib')
    plot_backend.deregister()