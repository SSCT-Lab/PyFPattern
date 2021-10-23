def init_session(ipython=None, pretty_print=True, order=None, use_unicode=None, use_latex=None, quiet=False, auto_symbols=False, auto_int_to_Integer=False, str_printer=None, pretty_printer=None, latex_printer=None, argv=[]):
    "\n    Initialize an embedded IPython or Python session. The IPython session is\n    initiated with the --pylab option, without the numpy imports, so that\n    matplotlib plotting can be interactive.\n\n    Parameters\n    ==========\n\n    pretty_print: boolean\n        If True, use pretty_print to stringify;\n        if False, use sstrrepr to stringify.\n    order: string or None\n        There are a few different settings for this parameter:\n        lex (default), which is lexographic order;\n        grlex, which is graded lexographic order;\n        grevlex, which is reversed graded lexographic order;\n        old, which is used for compatibility reasons and for long expressions;\n        None, which sets it to lex.\n    use_unicode: boolean or None\n        If True, use unicode characters;\n        if False, do not use unicode characters.\n    use_latex: boolean or None\n        If True, use latex rendering if IPython GUI's;\n        if False, do not use latex rendering.\n    quiet: boolean\n        If True, init_session will not print messages regarding its status;\n        if False, init_session will print messages regarding its status.\n    auto_symbols: boolean\n        If True, IPython will automatically create symbols for you.\n        If False, it will not.\n        The default is False.\n    auto_int_to_Integer: boolean\n        If True, IPython will automatically wrap int literals with Integer, so\n        that things like 1/2 give Rational(1, 2).\n        If False, it will not.\n        The default is False.\n    ipython: boolean or None\n        If True, printing will initialize for an IPython console;\n        if False, printing will initialize for a normal console;\n        The default is None, which automatically determines whether we are in\n        an ipython instance or not.\n    str_printer: function, optional, default=None\n        A custom string printer function. This should mimic\n        sympy.printing.sstrrepr().\n    pretty_printer: function, optional, default=None\n        A custom pretty printer. This should mimic sympy.printing.pretty().\n    latex_printer: function, optional, default=None\n        A custom LaTeX printer. This should mimic sympy.printing.latex()\n        This should mimic sympy.printing.latex().\n    argv: list of arguments for IPython\n        See sympy.bin.isympy for options that can be used to initialize IPython.\n\n    See Also\n    ========\n\n    sympy.interactive.printing.init_printing: for examples and the rest of the parameters.\n\n\n    Examples\n    ========\n\n    >>> from sympy import init_session, Symbol, sin, sqrt\n    >>> sin(x) #doctest: +SKIP\n    NameError: name 'x' is not defined\n    >>> init_session() #doctest: +SKIP\n    >>> sin(x) #doctest: +SKIP\n    sin(x)\n    >>> sqrt(5) #doctest: +SKIP\n      ___\n    \\/ 5\n    >>> init_session(pretty_print=False) #doctest: +SKIP\n    >>> sqrt(5) #doctest: +SKIP\n    sqrt(5)\n    >>> y + x + y**2 + x**2 #doctest: +SKIP\n    x**2 + x + y**2 + y\n    >>> init_session(order='grlex') #doctest: +SKIP\n    >>> y + x + y**2 + x**2 #doctest: +SKIP\n    x**2 + y**2 + x + y\n    >>> init_session(order='grevlex') #doctest: +SKIP\n    >>> y * x**2 + x * y**2 #doctest: +SKIP\n    x**2*y + x*y**2\n    >>> init_session(order='old') #doctest: +SKIP\n    >>> x**2 + y**2 + x + y #doctest: +SKIP\n    x + y + x**2 + y**2\n    >>> theta = Symbol('theta') #doctest: +SKIP\n    >>> theta #doctest: +SKIP\n    theta\n    >>> init_session(use_unicode=True) #doctest: +SKIP\n    >>> theta # doctest: +SKIP\n    θ\n    "
    import sys
    in_ipython = False
    if (ipython is not False):
        try:
            import IPython
        except ImportError:
            if (ipython is True):
                raise RuntimeError('IPython is not available on this system')
            ip = None
        else:
            if (V(IPython.__version__) >= '0.11'):
                try:
                    ip = get_ipython()
                except NameError:
                    ip = None
            else:
                ip = IPython.ipapi.get()
                if ip:
                    ip = ip.IP
        in_ipython = bool(ip)
        if (ipython is None):
            ipython = in_ipython
    if (ipython is False):
        ip = init_python_session()
        mainloop = ip.interact
    else:
        if (ip is None):
            ip = init_ipython_session(argv=argv, auto_symbols=auto_symbols, auto_int_to_Integer=auto_int_to_Integer)
        if (V(IPython.__version__) >= '0.11'):
            ip.runsource = (lambda src, symbol='exec': ip.run_cell(src, False))
            try:
                ip.enable_pylab(import_all=False)
            except Exception:
                pass
        if (not in_ipython):
            mainloop = ip.mainloop
    readline = import_module('readline')
    if (auto_symbols and ((not ipython) or (V(IPython.__version__) < '0.11') or (not readline))):
        raise RuntimeError('automatic construction of symbols is possible only in IPython 0.11 or above with readline support')
    if (auto_int_to_Integer and ((not ipython) or (V(IPython.__version__) < '0.11'))):
        raise RuntimeError('automatic int to Integer transformation is possible only in IPython 0.11 or above')
    _preexec_source = preexec_source
    ip.runsource(_preexec_source, symbol='exec')
    init_printing(pretty_print=pretty_print, order=order, use_unicode=use_unicode, use_latex=use_latex, ip=ip, str_printer=str_printer, pretty_printer=pretty_printer, latex_printer=latex_printer)
    message = _make_message(ipython, quiet, _preexec_source)
    if (not in_ipython):
        mainloop(message)
        sys.exit('Exiting ...')
    else:
        ip.write(message)
        import atexit
        atexit.register((lambda ip: ip.write('Exiting ...\n')), ip)