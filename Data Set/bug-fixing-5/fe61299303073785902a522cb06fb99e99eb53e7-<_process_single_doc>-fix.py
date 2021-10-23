def _process_single_doc(self, single_doc):
    'Extract self.single_doc (base name) and self.single_doc_type from\n        passed single_doc kwarg.\n\n        '
    self.include_api = False
    if ((single_doc == 'api.rst') or (single_doc == 'api')):
        self.single_doc_type = 'api'
        self.single_doc = 'api'
    elif os.path.exists(os.path.join(SOURCE_PATH, single_doc)):
        self.single_doc_type = 'rst'
        self.single_doc = os.path.splitext(os.path.basename(single_doc))[0]
    elif os.path.exists(os.path.join(SOURCE_PATH, '{}.rst'.format(single_doc))):
        self.single_doc_type = 'rst'
        self.single_doc = single_doc
    elif (single_doc is not None):
        try:
            obj = pandas
            for name in single_doc.split('.'):
                obj = getattr(obj, name)
        except AttributeError:
            raise ValueError('Single document not understood, it should be a file in doc/source/*.rst (e.g. "contributing.rst" or a pandas function or method (e.g. "pandas.DataFrame.head")')
        else:
            self.single_doc_type = 'docstring'
            if single_doc.startswith('pandas.'):
                self.single_doc = single_doc[len('pandas.'):]
            else:
                self.single_doc = single_doc