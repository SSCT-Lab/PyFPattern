def add_newdoc(place, obj, doc):
    "\n    Add documentation to an existing object, typically one defined in C\n\n    The purpose is to allow easier editing of the docstrings without requiring\n    a re-compile. This exists primarily for internal use within numpy itself.\n\n    Parameters\n    ----------\n    place : str\n        The absolute name of the module to import from\n    obj : str\n        The name of the object to add documentation to, typically a class or\n        function name\n    doc : {str, Tuple[str, str], List[Tuple[str, str]]}\n        If a string, the documentation to apply to `obj`\n\n        If a tuple, then the first element is interpreted as an attribute of\n        `obj` and the second as the docstring to apply - ``(method, docstring)``\n\n        If a list, then each element of the list should be a tuple of length\n        two - ``[(method1, docstring1), (method2, docstring2), ...]``\n\n    Notes\n    -----\n    This routine never raises an error if the docstring can't be written, but\n    will raise an error if the object being documented does not exist.\n\n    This routine cannot modify read-only docstrings, as appear\n    in new-style classes or built-in functions. Because this\n    routine never raises an error the caller must check manually\n    that the docstrings were changed.\n\n    Since this function grabs the ``char *`` from a c-level str object and puts\n    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of\n    C-API best-practices, by:\n\n    - modifying a `PyTypeObject` after calling `PyType_Ready`\n    - calling `Py_INCREF` on the str and losing the reference, so the str\n      will never be released\n\n    If possible it should be avoided.\n    "
    new = getattr(__import__(place, globals(), {
        
    }, [obj]), obj)
    if isinstance(doc, str):
        _add_docstring(new, doc.strip())
    elif isinstance(doc, tuple):
        (attr, docstring) = doc
        _add_docstring(getattr(new, attr), docstring.strip())
    elif isinstance(doc, list):
        for (attr, docstring) in doc:
            _add_docstring(getattr(new, attr), docstring.strip())