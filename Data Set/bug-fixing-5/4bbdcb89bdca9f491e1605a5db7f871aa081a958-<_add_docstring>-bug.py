def _add_docstring(obj, doc):
    try:
        add_docstring(obj, doc)
    except Exception:
        pass