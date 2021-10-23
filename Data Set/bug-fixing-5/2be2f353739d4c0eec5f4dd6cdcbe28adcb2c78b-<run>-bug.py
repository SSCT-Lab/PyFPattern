def run(self):
    super(DocCLI, self).run()
    if (self.options.module_path is not None):
        for i in self.options.module_path.split(os.pathsep):
            module_loader.add_directory(i)
    if self.options.list_dir:
        paths = module_loader._get_paths()
        for path in paths:
            self.find_modules(path)
        self.pager(self.get_module_list_text())
        return 0
    if (len(self.args) == 0):
        raise AnsibleOptionsError('Incorrect options passed')
    text = ''
    for module in self.args:
        try:
            filename = module_loader.find_plugin(module, mod_type='.py')
            if (filename is None):
                display.warning(('module %s not found in %s\n' % (module, DocCLI.print_paths(module_loader))))
                continue
            if any((filename.endswith(x) for x in C.BLACKLIST_EXTS)):
                continue
            try:
                (doc, plainexamples, returndocs) = module_docs.get_docstring(filename, verbose=(self.options.verbosity > 0))
            except:
                display.vvv(traceback.print_exc())
                display.error(('module %s has a documentation error formatting or is missing documentation\nTo see exact traceback use -vvv' % module))
                continue
            if (doc is not None):
                if (module in action_loader):
                    doc['action'] = True
                else:
                    doc['action'] = False
                all_keys = []
                for (k, v) in iteritems(doc['options']):
                    all_keys.append(k)
                all_keys = sorted(all_keys)
                doc['option_keys'] = all_keys
                doc['filename'] = filename
                doc['docuri'] = doc['module'].replace('_', '-')
                doc['now_date'] = datetime.date.today().strftime('%Y-%m-%d')
                doc['plainexamples'] = plainexamples
                doc['returndocs'] = returndocs
                if self.options.show_snippet:
                    text += self.get_snippet_text(doc)
                else:
                    text += self.get_man_text(doc)
            else:
                raise AnsibleError('Parsing produced an empty object.')
        except Exception as e:
            display.vvv(traceback.print_exc())
            raise AnsibleError(('module %s missing documentation (or could not parse documentation): %s\n' % (module, str(e))))
    self.pager(text)
    return 0