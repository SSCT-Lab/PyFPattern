def get_definitions():
    "Return a list of definitions in the Windows Common Setup\n\n    Each macro definition object has a 'name' and 'value' attribute.\n    "
    import re
    setup_in = open(PATH)
    try:
        deps = []
        match = re.compile('([a-zA-Z0-9_]+) += +(.+)$').match
        for line in setup_in:
            m = match(line)
            if (m is not None):
                deps.append(Definition(m.group(1), m.group(2)))
        return deps
    finally:
        setup_in.close()