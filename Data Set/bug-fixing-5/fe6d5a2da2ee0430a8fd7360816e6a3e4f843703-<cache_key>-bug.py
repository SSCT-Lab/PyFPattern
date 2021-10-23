def cache_key(self, template_name, skip=None):
    '\n        Generate a cache key for the template name, dirs, and skip.\n\n        If skip is provided, only origins that match template_name are included\n        in the cache key. This ensures each template is only parsed and cached\n        once if contained in different extend chains like:\n\n            x -> a -> a\n            y -> a -> a\n            z -> a -> a\n        '
    dirs_prefix = ''
    skip_prefix = ''
    if skip:
        matching = [origin.name for origin in skip if (origin.template_name == template_name)]
        if matching:
            skip_prefix = self.generate_hash(matching)
    return '-'.join((s for s in (str(template_name), skip_prefix, dirs_prefix) if s))