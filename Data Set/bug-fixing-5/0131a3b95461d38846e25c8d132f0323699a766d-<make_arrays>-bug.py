def make_arrays(funcdict):
    code1list = []
    code2list = []
    names = sorted(funcdict.keys())
    for name in names:
        uf = funcdict[name]
        funclist = []
        datalist = []
        siglist = []
        k = 0
        sub = 0
        if (uf.nin > 1):
            assert (uf.nin == 2)
            thedict = chartotype2
        else:
            thedict = chartotype1
        for t in uf.type_descriptions:
            if ((t.func_data not in (None, FullTypeDescr)) and (not isinstance(t.func_data, FuncNameSuffix))):
                funclist.append('NULL')
                astype = ''
                if (not (t.astype is None)):
                    astype = ('_As_%s' % thedict[t.astype])
                astr = ('%s_functions[%d] = PyUFunc_%s%s;' % (name, k, thedict[t.type], astype))
                code2list.append(astr)
                if (t.type == 'O'):
                    astr = ('%s_data[%d] = (void *) %s;' % (name, k, t.func_data))
                    code2list.append(astr)
                    datalist.append('(void *)NULL')
                elif (t.type == 'P'):
                    datalist.append(('(void *)"%s"' % t.func_data))
                else:
                    astr = ('%s_data[%d] = (void *) %s;' % (name, k, t.func_data))
                    code2list.append(astr)
                    datalist.append('(void *)NULL')
                sub += 1
            elif (t.func_data is FullTypeDescr):
                tname = english_upper(chartoname[t.type])
                datalist.append('(void *)NULL')
                funclist.append(('%s_%s_%s_%s' % (tname, t.in_, t.out, name)))
            elif isinstance(t.func_data, FuncNameSuffix):
                datalist.append('(void *)NULL')
                tname = english_upper(chartoname[t.type])
                funclist.append(('%s_%s_%s' % (tname, name, t.func_data.suffix)))
            else:
                datalist.append('(void *)NULL')
                tname = english_upper(chartoname[t.type])
                funclist.append(('%s_%s' % (tname, name)))
                if (t.simd is not None):
                    for vt in t.simd:
                        code2list.append('#ifdef HAVE_ATTRIBUTE_TARGET_{ISA}\nif (NPY_CPU_SUPPORTS_{ISA}) {{\n    {fname}_functions[{idx}] = {type}_{fname}_{isa};\n}}\n#endif\n'.format(ISA=vt.upper(), isa=vt, fname=name, type=tname, idx=k))
            for x in (t.in_ + t.out):
                siglist.append(('NPY_%s' % (english_upper(chartoname[x]),)))
            k += 1
        funcnames = ', '.join(funclist)
        signames = ', '.join(siglist)
        datanames = ', '.join(datalist)
        code1list.append(('static PyUFuncGenericFunction %s_functions[] = {%s};' % (name, funcnames)))
        code1list.append(('static void * %s_data[] = {%s};' % (name, datanames)))
        code1list.append(('static char %s_signatures[] = {%s};' % (name, signames)))
    return ('\n'.join(code1list), '\n'.join(code2list))