def command_coverage_combine(args):
    'Patch paths in coverage files and merge into a single file.\n    :type args: CoverageConfig\n    :rtype: list[str]\n    '
    coverage = initialize_coverage(args)
    modules = dict(((t.module, t.path) for t in list(walk_module_targets()) if t.path.endswith('.py')))
    coverage_files = [os.path.join(COVERAGE_DIR, f) for f in os.listdir(COVERAGE_DIR) if ('=coverage.' in f)]
    ansible_path = (os.path.abspath('lib/ansible/') + '/')
    root_path = (data_context().content.root + '/')
    counter = 0
    groups = {
        
    }
    if (args.all or args.stub):
        sources = sorted((os.path.abspath(target.path) for target in walk_compile_targets()))
    else:
        sources = []
    if args.stub:
        stub_group = []
        stub_groups = [stub_group]
        stub_line_limit = 500000
        stub_line_count = 0
        for source in sources:
            with open(source, 'r') as source_fd:
                source_line_count = len(source_fd.read().splitlines())
            stub_group.append(source)
            stub_line_count += source_line_count
            if (stub_line_count > stub_line_limit):
                stub_line_count = 0
                stub_group = []
                stub_groups.append(stub_group)
        for (stub_index, stub_group) in enumerate(stub_groups):
            if (not stub_group):
                continue
            groups[('=stub-%02d' % (stub_index + 1))] = dict(((source, set()) for source in stub_group))
    if data_context().content.collection:
        collection_search_re = re.compile(('/%s/' % data_context().content.collection.directory))
        collection_sub_re = re.compile(('^.*?/%s/' % data_context().content.collection.directory))
    else:
        collection_search_re = None
        collection_sub_re = None
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
            display.error(('%s' % ex))
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
            elif (collection_search_re and collection_search_re.search(filename)):
                new_name = os.path.abspath(collection_sub_re.sub('', filename))
                display.info(('%s -> %s' % (filename, new_name)), verbosity=3)
                filename = new_name
            elif re.search('/ansible_[^/]+_payload\\.zip/ansible/', filename):
                new_name = re.sub('^.*/ansible_[^/]+_payload\\.zip/ansible/', ansible_path, filename)
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
            elif re.search('/ansible_[^/]+_payload(_[^/]+|\\.zip)/__main__\\.py$', filename):
                module_name = re.sub('^.*/ansible_(?P<module>[^/]+)_payload(_[^/]+|\\.zip)/__main__\\.py$', '\\g<module>', filename).rstrip('_')
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
            elif ('/.ansible/test/tmp/' in filename):
                new_name = re.sub('^.*/\\.ansible/test/tmp/[^/]+/', root_path, filename)
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
    invalid_path_count = 0
    invalid_path_chars = 0
    for group in sorted(groups):
        arc_data = groups[group]
        updated = coverage.CoverageData()
        for filename in arc_data:
            if (not os.path.isfile(filename)):
                if (collection_search_re and collection_search_re.search(filename) and (os.path.basename(filename) == '__init__.py')):
                    continue
                invalid_path_count += 1
                invalid_path_chars += len(filename)
                if (args.verbosity > 1):
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
    if (invalid_path_count > 0):
        display.warning(('Ignored %d characters from %d invalid coverage path(s).' % (invalid_path_chars, invalid_path_count)))
    return sorted(output_files)