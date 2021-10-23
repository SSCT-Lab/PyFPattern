def mandatory(a):
    from jinja2.runtime import Undefined
    ' Make a variable mandatory '
    if isinstance(a, Undefined):
        raise AnsibleFilterError('Mandatory variable not defined.')
    return a