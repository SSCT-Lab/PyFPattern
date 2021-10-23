def _load_files(self, filename):
    ' Loads a file and converts the output into a valid Python dict.\n        Args:\n            filename (str): The source file.\n\n        Returns:\n            Tuple (bool, str, dict)\n        '
    results = dict()
    failed = False
    err_msg = ''
    if (not self._is_valid_file_ext(filename)):
        failed = True
        err_msg = '{0} does not have a valid extension: {1}'.format(filename, ', '.join(self.VALID_FILE_EXTENSIONS))
        return (failed, err_msg, results)
    (data, show_content) = self._loader._get_file_contents(filename)
    self.show_content = show_content
    data = self._loader.load(data, show_content)
    if (not data):
        data = dict()
    if (not isinstance(data, dict)):
        failed = True
        err_msg = '{0} must be stored as a dictionary/hash'.format(filename)
    else:
        results.update(data)
    return (failed, err_msg, results)