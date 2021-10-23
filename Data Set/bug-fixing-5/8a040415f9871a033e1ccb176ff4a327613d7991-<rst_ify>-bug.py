def rst_ify(text):
    ' convert symbols like I(this is in italics) to valid restructured text '
    try:
        t = _ITALIC.sub((('*' + '\\1') + '*'), text)
        t = _BOLD.sub((('**' + '\\1') + '**'), t)
        t = _MODULE.sub(((':ref:`module_docs/' + '\\1 <\\1>') + '`'), t)
        t = _URL.sub('\\1', t)
        t = _CONST.sub((('``' + '\\1') + '``'), t)
    except Exception as e:
        raise AnsibleError(('Could not process (%s) : %s' % (str(text), str(e))))
    return t