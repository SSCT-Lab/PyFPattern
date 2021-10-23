def srccoms_extract(srcfile, wlist):
    '\n    Given a source file ``srcfile``, this function will\n    extract its API(doc comments) and run sample codes in the\n    API.\n\n    Args:\n        srcfile(file): the source file\n        wlist(list): white list\n\n    Returns:\n    result: True or False\n    '
    process_result = True
    srcc = srcfile.read()
    srcfile.seek(0, 0)
    srcls = srcfile.readlines()
    allidx = srcc.find('__all__')
    if (allidx != (- 1)):
        alllist = []
        if (srcfile.name.find('ops.py') != (- 1)):
            for ai in range(0, len(srcls)):
                if srcls[ai].startswith('__all__'):
                    lb = srcls[ai].find('[')
                    rb = srcls[ai].find(']')
                    if (lb == (- 1)):
                        continue
                    allele = srcls[ai][(lb + 1):rb].replace("'", '').replace(' ', '').replace('"', '')
                    alllist.append(allele)
            if ('' in alllist):
                alllist.remove('')
        else:
            alllist_b = (allidx + len('__all__'))
            allstr = srcc[((alllist_b + srcc[alllist_b:].find('[')) + 1):(alllist_b + srcc[alllist_b:].find(']'))]
            allstr = allstr.replace('\n', '').replace(' ', '').replace("'", '').replace('"', '')
            alllist = allstr.split(',')
            if ('' in alllist):
                alllist.remove('')
        api_alllist_count = len(alllist)
        api_count = 0
        handled = []
        if (srcfile.name.find('ops.py') != (- 1)):
            for i in range(0, len(srcls)):
                if (srcls[i].find('__doc__') != (- 1)):
                    opname = srcls[i][:(srcls[i].find('__doc__') - 1)]
                    if (opname in wlist):
                        continue
                    comstart = i
                    for j in range(i, len(srcls)):
                        if (srcls[j].find('"""') != (- 1)):
                            comstart = i
                    opcom = ''
                    for j in range((comstart + 1), len(srcls)):
                        opcom += srcls[j]
                        if (srcls[j].find('"""') != (- 1)):
                            break
                    process_result = sampcd_extract_and_run(opcom, opname, 'def', opname)
                    api_count += 1
                    handled.append(opname)
        for i in range(0, len(srcls)):
            if srcls[i].startswith('def '):
                f_header = srcls[i].replace(' ', '')
                fn = f_header[len('def'):f_header.find('(')]
                if (fn in handled):
                    continue
                if (fn in alllist):
                    api_count += 1
                    if ((fn in wlist) or (((fn + '@') + srcfile.name) in wlist)):
                        continue
                    fcombody = single_defcom_extract(i, srcls)
                    if (fcombody == ''):
                        print_header('def', fn)
                        print('WARNING: no comments in function ', fn, ', but it deserves.')
                        continue
                    elif (not sampcd_extract_and_run(fcombody, fn, 'def', fn)):
                        process_result = False
            if srcls[i].startswith('class '):
                c_header = srcls[i].replace(' ', '')
                cn = c_header[len('class'):c_header.find('(')]
                if (cn in handled):
                    continue
                if (cn in alllist):
                    api_count += 1
                    if ((cn in wlist) or (((cn + '@') + srcfile.name) in wlist)):
                        continue
                    classcom = single_defcom_extract(i, srcls, True)
                    if (classcom != ''):
                        if (not sampcd_extract_and_run(classcom, cn, 'class', cn)):
                            process_result = False
                    else:
                        print('WARNING: no comments in class itself ', cn, ', but it deserves.\n')
                    for x in range((i + 1), len(srcls)):
                        if (srcls[x].startswith('def ') or srcls[x].startswith('class ')):
                            break
                        else:
                            srcls[x] = srcls[x].replace('\t', '    ')
                            if srcls[x].startswith('    def '):
                                thisl = srcls[x]
                                indent = (len(thisl) - len(thisl.lstrip()))
                                mn = thisl[(indent + len('def ')):thisl.find('(')]
                                name = ((cn + '.') + mn)
                                if mn.startswith('_'):
                                    continue
                                if ((name in wlist) or (((name + '@') + srcfile.name) in wlist)):
                                    continue
                                thismethod = [thisl[indent:]]
                                for y in range((x + 1), len(srcls)):
                                    srcls[y] = srcls[y].replace('\t', '    ')
                                    if (srcls[y].startswith('def ') or srcls[y].startswith('class ')):
                                        break
                                    elif srcls[y].startswith('    def '):
                                        break
                                    else:
                                        thismethod.append(srcls[y][indent:])
                                thismtdcom = single_defcom_extract(0, thismethod)
                                if (thismtdcom != ''):
                                    if (not sampcd_extract_and_run(thismtdcom, name, 'method', name)):
                                        process_result = False
    return process_result