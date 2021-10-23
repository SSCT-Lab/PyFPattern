def mandatory(a):
    from jinja2.runtime import Undefined
    ' Make a variable mandatory '
    if isinstance(a, Undefined):
        if (a._undefined_name is not None):
            name = ("'%s' " % to_text(a._undefined_name))
        else:
            name = ''
        raise AnsibleFilterError(('Mandatory variable %snot defined.' % name))
    return a