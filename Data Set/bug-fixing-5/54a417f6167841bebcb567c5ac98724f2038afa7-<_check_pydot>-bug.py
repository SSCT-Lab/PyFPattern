def _check_pydot():
    if (not (pydot and pydot.find_graphviz())):
        raise ImportError('Failed to import pydot. You must install pydot and graphviz for `pydotprint` to work.')