def _add_docstring(obj, doc, warn_on_python):
    if (warn_on_python and (not _needs_add_docstring(obj))):
        warnings.warn('add_newdoc was used on a pure-python object {}. Prefer to attach it directly to the source.'.format(obj), UserWarning, stacklevel=3)
    try:
        add_docstring(obj, doc)
    except Exception:
        pass