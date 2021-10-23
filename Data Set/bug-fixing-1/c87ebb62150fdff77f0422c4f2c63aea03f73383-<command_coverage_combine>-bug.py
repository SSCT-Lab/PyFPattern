

def command_coverage_combine(args):
    'Patch paths in coverage files and merge into a single file.\n    :type args: CoverageConfig\n    '
    coverage = initialize_coverage(args)
    modules = dict(((t.module, t.path) for t in list(walk_module_targets())))
    coverage_files = [os.path.join(COVERAGE_DIR, f) for f in os.listdir(COVERAGE_DIR) if (f.startswith('coverage') and (f != 'coverage'))]
    arc_data = {
        
    }
    ansible_path = (os.path.abspath('lib/ansible/') + '/')
    root_path = (os.getcwd() + '/')
    counter = 0
    for coverage_file in coverage_files:
        counter += 1
        display.info(('[%4d/%4d] %s' % (counter, len(coverage_files), coverage_file)), verbosity=2)
        original = coverage.CoverageData()
        if (os.path.getsize(coverage_file) == 0):
            display.warning(('Empty coverage file: %s' % coverage_file))
            continue
        try:
            original.read_file(coverage_file)
        except Exception as ex:
            display.error(str(ex))
            continue
        for filename in original.measured_files():
            arcs = original.arcs(filename)
            if ('/ansible_modlib.zip/ansible/' in filename):
                new_name = re.sub('^.*/ansible_modlib.zip/ansible/', ansible_path, filename)
                display.info(('%s -> %s' % (filename, new_name)), verbosity=3)
                filename = new_name
            elif ('/ansible_module_' in filename):
                module = re.sub('^.*/ansible_module_(?P<module>.*).py$', '\\g<module>', filename)
                new_name = os.path.abspath(modules[module])
                display.info(('%s -> %s' % (filename, new_name)), verbosity=3)
                filename = new_name
            elif filename.startswith('/root/ansible/'):
                new_name = re.sub('^/.*?/ansible/', root_path, filename)
                display.info(('%s -> %s' % (filename, new_name)), verbosity=3)
                filename = new_name
            if (filename not in arc_data):
                arc_data[filename] = []
            arc_data[filename] += arcs
    updated = coverage.CoverageData()
    for filename in arc_data:
        if (not os.path.isfile(filename)):
            display.warning(('Invalid coverage path: %s' % filename))
            continue
        updated.add_arcs({
            filename: arc_data[filename],
        })
    if (not args.explain):
        updated.write_file(COVERAGE_FILE)
