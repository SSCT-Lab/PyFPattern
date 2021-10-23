

def make_ufuncs(funcdict):
    code3list = []
    names = sorted(funcdict.keys())
    for name in names:
        uf = funcdict[name]
        mlist = []
        docstring = textwrap.dedent(uf.docstring).strip()
        if (sys.version_info[0] < 3):
            docstring = docstring.encode('string-escape')
            docstring = docstring.replace('"', '\\"')
        else:
            docstring = docstring.encode('unicode-escape').decode('ascii')
            docstring = docstring.replace('"', '\\"')
            docstring = docstring.replace("'", "\\'")
        docstring = '\\n""'.join(docstring.split('\\n'))
        mlist.append((textwrap.dedent('        f = PyUFunc_FromFuncAndData(%s_functions, %s_data, %s_signatures, %d,\n                                    %d, %d, %s, "%s",\n                                    "%s", 0);') % (name, name, name, len(uf.type_descriptions), uf.nin, uf.nout, uf.identity, name, docstring)))
        if (uf.typereso is not None):
            mlist.append(('((PyUFuncObject *)f)->type_resolver = &%s;' % uf.typereso))
        mlist.append(('PyDict_SetItemString(dictionary, "%s", f);' % name))
        mlist.append('Py_DECREF(f);')
        code3list.append('\n'.join(mlist))
    return '\n'.join(code3list)
