

def do_ini(module, filename, section=None, option=None, value=None, state='present', backup=False, no_extra_spaces=False, create=False):
    diff = {
        'before': '',
        'after': '',
        'before_header': ('%s (content)' % filename),
        'after_header': ('%s (content)' % filename),
    }
    if (not os.path.exists(filename)):
        if (not create):
            module.fail_json(rc=257, msg=('Destination %s does not exist !' % filename))
        destpath = os.path.dirname(filename)
        if ((not os.path.exists(destpath)) and (not module.check_mode)):
            os.makedirs(destpath)
        ini_lines = []
    else:
        ini_file = open(filename, 'r')
        try:
            ini_lines = ini_file.readlines()
        finally:
            ini_file.close()
    if module._diff:
        diff['before'] = ''.join(ini_lines)
    ini_lines.append('[')
    within_section = (not section)
    section_start = 0
    changed = False
    msg = 'OK'
    if no_extra_spaces:
        assignment_format = '%s=%s\n'
    else:
        assignment_format = '%s = %s\n'
    for (index, line) in enumerate(ini_lines):
        if line.startswith(('[%s]' % section)):
            within_section = True
            section_start = index
        elif line.startswith('['):
            if within_section:
                if (state == 'present'):
                    for i in range(index, 0, (- 1)):
                        if (not re.match('^[ \\t]*([#;].*)?$', ini_lines[(i - 1)])):
                            ini_lines.insert(i, (assignment_format % (option, value)))
                            msg = 'option added'
                            changed = True
                            break
                elif ((state == 'absent') and (not option)):
                    del ini_lines[section_start:index]
                    msg = 'section removed'
                    changed = True
                break
        elif (within_section and option):
            if (state == 'present'):
                if match_opt(option, line):
                    newline = (assignment_format % (option, value))
                    changed = (ini_lines[index] != newline)
                    if changed:
                        msg = 'option changed'
                    ini_lines[index] = newline
                    if changed:
                        index = (index + 1)
                        while (index < len(ini_lines)):
                            line = ini_lines[index]
                            if line.startswith('['):
                                break
                            if match_active_opt(option, line):
                                del ini_lines[index]
                            else:
                                index = (index + 1)
                    break
            elif (state == 'absent'):
                if match_active_opt(option, line):
                    del ini_lines[index]
                    changed = True
                    msg = 'option changed'
                    break
    del ini_lines[(- 1):]
    if ((not within_section) and option and (state == 'present')):
        ini_lines.append(('[%s]\n' % section))
        ini_lines.append((assignment_format % (option, value)))
        changed = True
        msg = 'section and option added'
    if module._diff:
        diff['after'] = ''.join(ini_lines)
    backup_file = None
    if (changed and (not module.check_mode)):
        if backup:
            backup_file = module.backup_local(filename)
        ini_file = open(filename, 'w')
        try:
            ini_file.writelines(ini_lines)
        finally:
            ini_file.close()
    return (changed, backup_file, diff, msg)
