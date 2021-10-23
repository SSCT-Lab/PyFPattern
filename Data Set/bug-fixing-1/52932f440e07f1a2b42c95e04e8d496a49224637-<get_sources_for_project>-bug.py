

def get_sources_for_project(project):
    '\n    Returns a list of symbol sources for this project.\n    '
    sources = []
    project_source = get_internal_source(project)
    sources.append(project_source)
    sources_config = project.get_option('sentry:symbol_sources')
    if sources_config:
        try:
            custom_sources = parse_sources(sources_config)
            sources.extend(custom_sources)
        except InvalidSourcesError:
            logger.error('Invalid symbolicator source config', exc_info=True)
    builtin_sources = (project.get_option('sentry:builtin_symbol_sources') or [])
    for (key, source) in six.iteritems(BUILTIN_SOURCES):
        if (key in builtin_sources):
            sources.push(source)
    return sources
