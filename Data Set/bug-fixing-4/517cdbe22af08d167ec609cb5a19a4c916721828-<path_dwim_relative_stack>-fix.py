def path_dwim_relative_stack(self, paths, dirname, source, is_role=False):
    '\n        find one file in first path in stack taking roles into account and adding play basedir as fallback\n\n        :arg paths: A list of text strings which are the paths to look for the filename in.\n        :arg dirname: A text string representing a directory.  The directory\n            is prepended to the source to form the path to search for.\n        :arg source: A text string which is the filename to search for\n        :rtype: A text string\n        :returns: An absolute path to the filename ``source``\n        '
    b_dirname = to_bytes(dirname)
    b_source = to_bytes(source)
    result = None
    if (source is None):
        display.warning('Invalid request to find a file that matches a "null" value')
    elif (source and (source.startswith('~') or source.startswith(os.path.sep))):
        test_path = unfrackpath(b_source)
        if os.path.exists(to_bytes(test_path, errors='surrogate_or_strict')):
            result = test_path
    else:
        search = []
        display.debug(('evaluation_path:\n\t%s' % '\n\t'.join(paths)))
        for path in paths:
            upath = unfrackpath(path)
            b_upath = to_bytes(upath, errors='surrogate_or_strict')
            b_mydir = os.path.dirname(b_upath)
            if (is_role or self._is_role(path)):
                if b_mydir.endswith(b'tasks'):
                    search.append(os.path.join(os.path.dirname(b_mydir), b_dirname, b_source))
                    search.append(os.path.join(b_mydir, b_source))
                else:
                    if (b_source.split(b'/')[0] != b_dirname):
                        search.append(os.path.join(b_upath, b_dirname, b_source))
                    search.append(os.path.join(b_upath, b_source))
            elif (b_dirname not in b_source.split(b'/')):
                if (b_source.split(b'/')[0] != dirname):
                    search.append(os.path.join(b_upath, b_dirname, b_source))
                search.append(os.path.join(b_upath, b_source))
        if (b_source.split(b'/')[0] != dirname):
            search.append(os.path.join(to_bytes(self.get_basedir()), b_dirname, b_source))
        search.append(os.path.join(to_bytes(self.get_basedir()), b_source))
        display.debug(('search_path:\n\t%s' % to_text(b'\n\t'.join(search))))
        for b_candidate in search:
            display.vvvvv(('looking for "%s" at "%s"' % (source, to_text(b_candidate))))
            if os.path.exists(b_candidate):
                result = to_text(b_candidate)
                break
    return result