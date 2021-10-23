

def write_pot_file(potfile, msgs):
    '\n    Write the `potfile` with the `msgs` contents, making sure its format is\n    valid.\n    '
    pot_lines = msgs.splitlines()
    if os.path.exists(potfile):
        lines = dropwhile(len, pot_lines)
    else:
        lines = []
        (found, header_read) = (False, False)
        for line in pot_lines:
            if ((not found) and (not header_read)):
                found = True
                line = line.replace('charset=CHARSET', 'charset=UTF-8')
            if ((not line) and (not found)):
                header_read = True
            lines.append(line)
    msgs = '\n'.join(lines)
    with open(potfile, 'a', encoding='utf-8') as fp:
        fp.write(msgs)
