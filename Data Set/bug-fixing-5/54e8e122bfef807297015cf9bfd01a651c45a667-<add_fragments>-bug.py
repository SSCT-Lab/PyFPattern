def add_fragments(doc, filename):
    fragments = doc.get('extends_documentation_fragment', [])
    if isinstance(fragments, string_types):
        fragments = [fragments]
    for fragment_slug in fragments:
        fragment_slug = fragment_slug.lower()
        if ('.' in fragment_slug):
            (fragment_name, fragment_var) = fragment_slug.split('.', 1)
            fragment_var = fragment_var.upper()
        else:
            (fragment_name, fragment_var) = (fragment_slug, 'DOCUMENTATION')
        fragment_class = fragment_loader.get(fragment_name)
        if (fragment_class is None):
            raise AnsibleAssertionError('fragment_class is None')
        fragment_yaml = getattr(fragment_class, fragment_var, '{}')
        fragment = AnsibleLoader(fragment_yaml, file_name=filename).get_single_data()
        if ('notes' in fragment):
            notes = fragment.pop('notes')
            if notes:
                if ('notes' not in doc):
                    doc['notes'] = []
                doc['notes'].extend(notes)
        if ('options' not in fragment):
            raise Exception(('missing options in fragment (%s), possibly misformatted?: %s' % (fragment_name, filename)))
        if ('options' in doc):
            try:
                merge_fragment(doc['options'], fragment.pop('options'))
            except Exception as e:
                raise AnsibleError(('%s options (%s) of unknown type: %s' % (to_native(e), fragment_name, filename)))
        try:
            merge_fragment(doc, fragment)
        except Exception as e:
            raise AnsibleError(('%s (%s) of unknown type: %s' % (to_native(e), fragment_name, filename)))