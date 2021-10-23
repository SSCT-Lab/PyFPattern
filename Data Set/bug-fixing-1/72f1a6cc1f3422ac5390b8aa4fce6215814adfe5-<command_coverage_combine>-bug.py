

def command_coverage_combine(args):
    'Patch paths in coverage files and merge into a single file.\n    :type args: CoverageConfig\n    :rtype: list[str]\n    '
    coverage = initialize_coverage(args)
    modules = dict(((t.module, t.path) for t in list(walk_module_targets())))
    coverage_files = [os.path.join(COVERAGE_DIR, f) for f in os.listdir(COVERAGE_DIR) if ('=coverage.' in f)]
    ansible_path = (os.path.abspath('lib/ansible/') + '/')
    root_path = (os.getcwd() + '/')
    counter = 0
    groups = {
        
    }
    if (args.all or args.stub):
        sources = sorted((os.path.abspath(target.path) for target in walk_compile_targets()))
    else:
        sources = []
    if args.stub:
        groups['=stub'] = dict(((source, set()) for source in sources))
    for coverage_file in coverage_files:
        counter += 1
        display.info(('[%4d/%4d] %s' % (counter, len(coverage_files), coverage_file)), verbosity=2)
        original = coverage.CoverageData()
        group = get_coverage_group(args, coverage_file)
        if (group is None):
            display.warning(('Unexpected name for coverage file: %s' % coverage_file))
            continue
        if (os.path.getsize(coverage_file) == 0):
            display.warning(('Empty coverage file: %s' % coverage_file))
            continue
        try:
            original.read_file(coverage_file)
        except Exception as ex:
            display.error(str(ex))
            continue
        for filename in original.measured_files():
            arcs = set((original.arcs(filename) or []))
            if (not arcs):
                display.warning(('No arcs found for "%s" in coverage file: %s' % (filename, coverage_file)))
                continue
            if ('/ansible_modlib.zip/ansible/' in filename):
                new_name = re.sub('^.*/ansible_modlib.zip/ansible/', ansible_path, filename)
                display.info(('%s -> %s' % (filename, new_name)), verbosity=3)
                filename = new_name
            elif ('/ansible_module_' in filename):
                module_name = re.sub('^.*/ansible_module_(?P<module>.*).py$', '\\g<module>', filename)
                if (module_name not in modules):
                    display.warning(('Skipping coverage of unknown module: %s' % module_name))
                    continue
                new_name = os.path.abspath(modules[module_name])
                display.info(('%s -> %s' % (filename, new_name)), verbosity=3)
                filename = new_name
            elif re.search('^(/.*?)?/root/ansible/', filename):
                new_name = re.sub('^(/.*?)?/root/ansible/', root_path, filename)
                display.info(('%s -> %s' % (filename, new_name)), verbosity=3)
                filename = new_name
            if (group not in groups):
                groups[group] = {
                    
                }
            arc_data = groups[group]
            if (filename not in arc_data):
                arc_data[filename] = set()
            arc_data[filename].update(arcs)
    output_files = []
    for group in sorted(groups):
        arc_data = groups[group]
        updated = coverage.CoverageData()
        for filename in arc_data:
            if (not os.path.isfile(filename)):
                display.warning(('Invalid coverage path: %s' % filename))
                continue
            updated.add_arcs({
                filename: list(arc_data[filename]),
            })
        if args.all:
            updated.add_arcs(dict(((source, []) for source in sources)))
        if (not args.explain):
            output_file = (COVERAGE_FILE + group)
            updated.write_file(output_file)
            output_files.append(output_file)
    return sorted(output_files)
