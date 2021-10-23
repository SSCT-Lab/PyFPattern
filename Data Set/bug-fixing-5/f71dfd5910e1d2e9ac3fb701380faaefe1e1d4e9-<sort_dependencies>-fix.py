def sort_dependencies():
    "\n    Similar to Django's except that we discard the important of natural keys\n    when sorting dependencies (i.e. it works without them).\n    "
    from django.apps import apps
    model_dependencies = []
    models = set()
    for app_config in apps.get_app_configs():
        model_list = app_config.get_models()
        for model in model_list:
            models.add(model)
            if hasattr(model, 'natural_key'):
                deps = getattr(model.natural_key, 'dependencies', [])
                if deps:
                    deps = [apps.get_model(*d.split('.')) for d in deps]
            else:
                deps = []
            for field in model._meta.fields:
                if hasattr(field.rel, 'to'):
                    rel_model = field.rel.to
                    if (rel_model != model):
                        deps.append(rel_model)
            for field in model._meta.many_to_many:
                rel_model = field.rel.to
                if (rel_model != model):
                    deps.append(rel_model)
            model_dependencies.append((model, deps))
    model_dependencies.reverse()
    model_list = []
    while model_dependencies:
        skipped = []
        changed = False
        while model_dependencies:
            (model, deps) = model_dependencies.pop()
            found = True
            for candidate in (((d not in models) or (d in model_list)) for d in deps):
                if (not candidate):
                    found = False
            if found:
                model_list.append(model)
                changed = True
            else:
                skipped.append((model, deps))
        if (not changed):
            raise RuntimeError(("Can't resolve dependencies for %s in serialized app list." % ', '.join((('%s.%s' % (model._meta.app_label, model._meta.object_name)) for (model, deps) in sorted(skipped, key=(lambda obj: obj[0].__name__))))))
        model_dependencies = skipped
    return model_list