def group_models_by_index(backend, models):
    '\n    This takes a search backend and a list of models. By calling the\n    get_index_for_model method on the search backend, it groups the models into\n    the indices that they will be indexed into.\n\n    It returns an ordered mapping of indices to lists of models within each\n    index.\n\n    For example, Elasticsearch 2 requires all page models to be together, but\n    separate from other content types (eg, images and documents) to prevent\n    field mapping collisions (eg, images and documents):\n\n    >>> group_models_by_index(elasticsearch2_backend, [\n    ...     wagtailcore.Page,\n    ...     myapp.HomePage,\n    ...     myapp.StandardPage,\n    ...     wagtailimages.Image\n    ... ])\n    {\n        <Index wagtailcore_page>: [wagtailcore.Page, myapp.HomePage, myapp.StandardPage],\n        <Index wagtailimages_image>: [wagtailimages.Image],\n    }\n    '
    indices = {
        
    }
    models_by_index = collections.OrderedDict()
    for model in models:
        index = backend.get_index_for_model(model)
        if index:
            indices.setdefault(index.name, index)
            models_by_index.setdefault(index.name, [])
            models_by_index[index.name].append(model)
    return collections.OrderedDict([(indices[index_name], index_models) for (index_name, index_models) in models_by_index.items()])