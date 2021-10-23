def _load_files(self, filename, validate_extensions=False):
    ' Loads a file and converts the output into a valid Python dict.\n        Args:\n            filename (str): The source file.\n\n        Returns:\n            Tuple (bool, str, dict)\n        '
    results = dict()
    failed = False
    err_msg = ''
    if (validate_extensions and (not self._is_valid_file_ext(filename))):
        failed = True
        err_msg = '{0} does not have a valid extension: {1}'.format(filename, ', '.join(self.valid_extensions))
    else:
        (b_data, show_content) = self._loader._get_file_contents(filename)
        data = to_text(b_data, errors='surrogate_or_strict')
        self.show_content = show_content
        data = self._loader.load(data, file_name=filename, show_content=show_content)
        if (not data):
            data = dict()
        if (not isinstance(data, dict)):
            failed = True
            err_msg = '{0} must be stored as a dictionary/hash'.format(filename)
        else:
            self.included_files.append(filename)
            results.update(data)
    return (failed, err_msg, results)