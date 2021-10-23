def _parse_char_metrics(fh):
    '\n    Return a character metric dictionary.  Keys are the ASCII num of\n    the character, values are a (*wx*, *name*, *bbox*) tuple, where\n    *wx* is the character width, *name* is the postscript language\n    name, and *bbox* is a (*llx*, *lly*, *urx*, *ury*) tuple.\n\n    This function is incomplete per the standard, but thus far parses\n    all the sample afm files tried.\n    '
    ascii_d = {
        
    }
    name_d = {
        
    }
    for line in fh:
        line = _to_str(line.rstrip())
        if line.startswith('EndCharMetrics'):
            return (ascii_d, name_d)
        vals = dict((s.strip().split(' ', 1) for s in line.split(';') if s))
        if (not {'C', 'WX', 'N', 'B'}.issubset(vals)):
            raise RuntimeError(('Bad char metrics line: %s' % line))
        num = _to_int(vals['C'])
        wx = _to_float(vals['WX'])
        name = vals['N']
        bbox = _to_list_of_floats(vals['B'])
        bbox = list(map(int, bbox))
        if (name == 'Euro'):
            num = 128
        if (num != (- 1)):
            ascii_d[num] = (wx, name, bbox)
        name_d[name] = (wx, bbox)
    raise RuntimeError('Bad parse')