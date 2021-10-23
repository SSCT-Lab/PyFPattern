def _check_pydot():
    try:
        pydot.Dot.create(pydot.Dot())
    except Exception:
        raise ImportError('Failed to import pydot. You must install pydot and graphviz for `pydotprint` to work.')