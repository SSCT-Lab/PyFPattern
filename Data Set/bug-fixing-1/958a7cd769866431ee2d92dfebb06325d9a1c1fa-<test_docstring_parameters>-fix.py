

def test_docstring_parameters():
    try:
        import numpydoc
        assert (sys.version_info >= (3, 5))
    except (ImportError, AssertionError):
        raise SkipTest('numpydoc is required to test the docstrings, as well as python version >= 3.5')
    from numpydoc import docscrape
    incorrect = []
    for name in PUBLIC_MODULES:
        if (name.startswith('_') or (name.split('.')[1] in IGNORED_MODULES)):
            continue
        with warnings.catch_warnings(record=True):
            module = importlib.import_module(name)
        classes = inspect.getmembers(module, inspect.isclass)
        classes = [cls for cls in classes if (cls[1].__module__ == name)]
        for (cname, cls) in classes:
            this_incorrect = []
            if ((cname in _DOCSTRING_IGNORES) or cname.startswith('_')):
                continue
            if isabstract(cls):
                continue
            with warnings.catch_warnings(record=True) as w:
                cdoc = docscrape.ClassDoc(cls)
            if len(w):
                raise RuntimeError(('Error for __init__ of %s in %s:\n%s' % (cls, name, w[0])))
            cls_init = getattr(cls, '__init__', None)
            if _is_deprecated(cls_init):
                continue
            elif (cls_init is not None):
                this_incorrect += check_docstring_parameters(cls.__init__, cdoc, class_name=cname)
            for method_name in cdoc.methods:
                method = getattr(cls, method_name)
                if _is_deprecated(method):
                    continue
                param_ignore = None
                if (method_name in _METHODS_IGNORE_NONE_Y):
                    sig = signature(method)
                    if (('y' in sig.parameters) and (sig.parameters['y'].default is None)):
                        param_ignore = ['y']
                result = check_docstring_parameters(method, ignore=param_ignore, class_name=cname)
                this_incorrect += result
            incorrect += this_incorrect
        functions = inspect.getmembers(module, inspect.isfunction)
        functions = [fn for fn in functions if (fn[1].__module__ == name)]
        for (fname, func) in functions:
            if fname.startswith('_'):
                continue
            if ((fname == 'configuration') and name.endswith('setup')):
                continue
            name_ = _get_func_name(func)
            if ((not any(((d in name_) for d in _DOCSTRING_IGNORES))) and (not _is_deprecated(func))):
                incorrect += check_docstring_parameters(func)
    msg = ('\n' + '\n'.join(sorted(list(set(incorrect)))))
    if (len(incorrect) > 0):
        raise AssertionError(('Docstring Error: ' + msg))
