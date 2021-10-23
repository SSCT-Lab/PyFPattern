def register(explicit=True):
    '\n    Register Pandas Formatters and Converters with matplotlib\n\n    This function modifies the global ``matplotlib.units.registry``\n    dictionary. Pandas adds custom converters for\n\n    * pd.Timestamp\n    * pd.Period\n    * np.datetime64\n    * datetime.datetime\n    * datetime.date\n    * datetime.time\n\n    See Also\n    --------\n    deregister_matplotlib_converter\n    '
    plot_backend = _get_plot_backend('matplotlib')
    plot_backend.register(explicit=explicit)