def deprecated(since, *, message='', name='', alternative='', pending=False, obj_type=None, addendum='', removal=''):
    "\n    Decorator to mark a function, a class, or a property as deprecated.\n\n    When deprecating a classmethod, a staticmethod, or a property, the\n    ``@deprecated`` decorator should go *under* the ``@classmethod``, etc.\n    decorator (i.e., `deprecated` should directly decorate the underlying\n    callable).\n\n    Parameters\n    ----------\n    since : str\n        The release at which this API became deprecated.\n\n    message : str, optional\n        Override the default deprecation message.  The format\n        specifier `%(name)s` may be used for the name of the object,\n        and `%(alternative)s` may be used in the deprecation message\n        to insert the name of an alternative to the deprecated\n        object.\n\n    name : str, optional\n        The name used in the deprecation message; if not provided, the name\n        is automatically determined from the deprecated object.\n\n    alternative : str, optional\n        An alternative API that the user may use in place of the deprecated\n        API.  The deprecation warning will tell the user about this alternative\n        if provided.\n\n    pending : bool, optional\n        If True, uses a PendingDeprecationWarning instead of a\n        DeprecationWarning.  Cannot be used together with *removal*.\n\n    obj_type : str, optional\n        The object type being deprecated; by default, 'class' if decorating\n        a class, 'attribute' if decorating a property, 'function' otherwise.\n\n    addendum : str, optional\n        Additional text appended directly to the final message.\n\n    removal : str, optional\n        The expected removal version.  With the default (an empty string), a\n        removal version is automatically computed from *since*.  Set to other\n        Falsy values to not schedule a removal date.  Cannot be used together\n        with *pending*.\n\n    Examples\n    --------\n    Basic example::\n\n        @deprecated('1.4.0')\n        def the_function_to_deprecate():\n            pass\n    "

    def deprecate(obj, message=message, name=name, alternative=alternative, pending=pending, obj_type=obj_type, addendum=addendum):
        if isinstance(obj, type):
            if (obj_type is None):
                obj_type = 'class'
            func = obj.__init__
            name = (name or obj.__name__)
            old_doc = obj.__doc__

            def finalize(wrapper, new_doc):
                try:
                    obj.__doc__ = new_doc
                except AttributeError:
                    pass
                obj.__init__ = wrapper
                return obj
        elif isinstance(obj, property):
            obj_type = 'attribute'
            func = None
            name = (name or obj.fget.__name__)
            old_doc = obj.__doc__

            class _deprecated_property(property):

                def __get__(self, instance, owner):
                    if (instance is not None):
                        from . import _warn_external
                        _warn_external(warning)
                    return super().__get__(instance, owner)

                def __set__(self, instance, value):
                    if (instance is not None):
                        from . import _warn_external
                        _warn_external(warning)
                    return super().__set__(instance, value)

                def __delete__(self, instance):
                    if (instance is not None):
                        from . import _warn_external
                        _warn_external(warning)
                    return super().__delete__(instance)

            def finalize(_, new_doc):
                return _deprecated_property(fget=obj.fget, fset=obj.fset, fdel=obj.fdel, doc=new_doc)
        else:
            if (obj_type is None):
                obj_type = 'function'
            func = obj
            name = (name or obj.__name__)
            old_doc = func.__doc__

            def finalize(wrapper, new_doc):
                wrapper = functools.wraps(func)(wrapper)
                wrapper.__doc__ = new_doc
                return wrapper
        warning = _generate_deprecation_warning(since, message, name, alternative, pending, obj_type, addendum, removal=removal)

        def wrapper(*args, **kwargs):
            from . import _warn_external
            _warn_external(warning)
            return func(*args, **kwargs)
        old_doc = inspect.cleandoc((old_doc or '')).strip('\n')
        notes_header = '\nNotes\n-----'
        new_doc = f'''[*Deprecated*] {old_doc}
{(notes_header if (notes_header not in old_doc) else '')}
.. deprecated:: {since}
   {message.strip()}'''
        if (not old_doc):
            new_doc += '\\ '
        return finalize(wrapper, new_doc)
    return deprecate