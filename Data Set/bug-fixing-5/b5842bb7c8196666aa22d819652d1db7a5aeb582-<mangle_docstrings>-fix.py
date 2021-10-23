def mangle_docstrings(app, what, name, obj, options, lines, reference_offset=[0]):
    cfg = dict(use_plots=app.config.numpydoc_use_plots, show_class_members=app.config.numpydoc_show_class_members, class_members_toctree=app.config.numpydoc_class_members_toctree)
    no_autosummary = ['.Categorical', 'CategoricalIndex', 'IntervalIndex', 'RangeIndex', 'Int64Index', 'UInt64Index', 'Float64Index']
    if ((what == 'class') and any((name.endswith(n) for n in no_autosummary))):
        cfg['class_members_list'] = False
    if (what == 'module'):
        title_re = re.compile(sixu('^\\s*[#*=]{4,}\\n[a-z0-9 -]+\\n[#*=]{4,}\\s*'), (re.I | re.S))
        lines[:] = title_re.sub(sixu(''), sixu('\n').join(lines)).split(sixu('\n'))
    else:
        doc = get_doc_object(obj, what, sixu('\n').join(lines), config=cfg)
        if (sys.version_info[0] >= 3):
            doc = str(doc)
        else:
            doc = unicode(doc)
        lines[:] = doc.split(sixu('\n'))
    if (app.config.numpydoc_edit_link and hasattr(obj, '__name__') and obj.__name__):
        if hasattr(obj, '__module__'):
            v = dict(full_name=(sixu('%s.%s') % (obj.__module__, obj.__name__)))
        else:
            v = dict(full_name=obj.__name__)
        lines += [sixu(''), sixu('.. htmlonly::'), sixu('')]
        lines += [(sixu('    %s') % x) for x in (app.config.numpydoc_edit_link % v).split('\n')]
    references = []
    for line in lines:
        line = line.strip()
        m = re.match(sixu('^.. \\[([a-z0-9_.-])\\]'), line, re.I)
        if m:
            references.append(m.group(1))
    references.sort(key=(lambda x: (- len(x))))
    if references:
        for (i, line) in enumerate(lines):
            for r in references:
                if re.match(sixu('^\\d+$'), r):
                    new_r = (sixu('R%d') % (reference_offset[0] + int(r)))
                else:
                    new_r = (sixu('%s%d') % (r, reference_offset[0]))
                lines[i] = lines[i].replace((sixu('[%s]_') % r), (sixu('[%s]_') % new_r))
                lines[i] = lines[i].replace((sixu('.. [%s]') % r), (sixu('.. [%s]') % new_r))
    reference_offset[0] += len(references)