def compile_messages(self, locations):
    '\n        Locations is a list of tuples: [(directory, file), ...]\n        '
    for (i, (dirpath, f)) in enumerate(locations):
        if (self.verbosity > 0):
            self.stdout.write(('processing file %s in %s\n' % (f, dirpath)))
        po_path = os.path.join(dirpath, f)
        if has_bom(po_path):
            self.stderr.write(('The %s file has a BOM (Byte Order Mark). Django only supports .po files encoded in UTF-8 and without any BOM.' % po_path))
            self.has_errors = True
            continue
        base_path = os.path.splitext(po_path)[0]
        if ((i == 0) and (not is_writable((base_path + '.mo')))):
            self.stderr.write(('The po files under %s are in a seemingly not writable location. mo files will not be updated/created.' % dirpath))
            self.has_errors = True
            return
        args = (([self.program] + self.program_options) + ['-o', (base_path + '.mo'), (base_path + '.po')])
        (output, errors, status) = popen_wrapper(args)
        if status:
            if errors:
                self.stderr.write(('Execution of %s failed: %s.' % (self.program, errors)))
            else:
                self.stderr.write(('Execution of %s failed.' % self.program))
            self.has_errors = True