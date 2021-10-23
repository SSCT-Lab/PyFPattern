def srccoms_extract(srcfile, status_all, wlist):
    '\n    Given a source file ``srcfile``, this function will\n    extract its API(doc comments) and run sample codes in the\n    API.\n\n    Args:\n        srcfile(file): the source file\n        status_all(dict): record all the sample code execution states.\n        wlist(list): white list\n\n    Returns:\n\n        string: the length of __all__ list in srcfile versus the exact number of\n                analysed API to make sure no API is missed in this srcfile and it\n                is useful for statistic practices.\n    '
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
                        status_all[((srcfile.name + '/') + opname)] = [(- 2)]
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
                    status = sampcd_extract_and_run(opcom, opname, 'def', opname)
                    api_count += 1
                    status_all[((srcfile.name + '/') + opname)] = status
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
                        status_all[((srcfile.name + '/') + fn)] = [(- 2)]
                        continue
                    fcombody = single_defcom_extract(i, srcls)
                    if (fcombody == ''):
                        print_header('def', fn)
                        print('WARNING: no comments in function ', fn, ', but it deserves.')
                        status_all[((srcfile.name + '/') + fn)] = [(- 1)]
                        print(status_all[((srcfile.name + '/') + fn)])
                        continue
                    else:
                        status = sampcd_extract_and_run(fcombody, fn, 'def', fn)
                        status_all[((srcfile.name + '/') + fn)] = status
            if srcls[i].startswith('class '):
                c_header = srcls[i].replace(' ', '')
                cn = c_header[len('class'):c_header.find('(')]
                if (cn in handled):
                    continue
                if (cn in alllist):
                    api_count += 1
                    if ((cn in wlist) or (((cn + '@') + srcfile.name) in wlist)):
                        status_all[((srcfile.name + '/') + cn)] = [(- 2)]
                        continue
                    classcom = single_defcom_extract(i, srcls, True)
                    if (classcom != ''):
                        status = sampcd_extract_and_run(classcom, cn, 'class', cn)
                        status_all[((srcfile.name + '/') + cn)] = status
                    else:
                        print('WARNING: no comments in class itself ', cn, ', but it deserves.\n')
                        status_all[((srcfile.name + '/') + cn)] = [(- 1)]
                        print(status_all[((srcfile.name + '/') + cn)])
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
                                    status_all[((srcfile.name + '/') + name)] = [(- 2)]
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
                                    status = sampcd_extract_and_run(thismtdcom, name, 'method', name)
                                    status_all[((srcfile.name + '/') + name)] = status
    return [((srcfile.name + ' all list length: ') + str(api_alllist_count)), ('analysed api count: ' + str(api_count))]