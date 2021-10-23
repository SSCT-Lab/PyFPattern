

def _check_list_display_item(self, obj, model, item, label):
    if callable(item):
        return []
    elif hasattr(obj, item):
        return []
    elif hasattr(model, item):
        try:
            field = model._meta.get_field(item)
        except FieldDoesNotExist:
            try:
                field = getattr(model, item)
            except AttributeError:
                field = None
        if (field is None):
            return [checks.Error(("The value of '%s' refers to '%s', which is not a callable, an attribute of '%s', or an attribute or method on '%s.%s'." % (label, item, obj.__class__.__name__, model._meta.app_label, model._meta.object_name)), obj=obj.__class__, id='admin.E108')]
        elif isinstance(field, models.ManyToManyField):
            return [checks.Error(("The value of '%s' must not be a ManyToManyField." % label), obj=obj.__class__, id='admin.E109')]
        else:
            return []
    else:
        try:
            model._meta.get_field(item)
        except FieldDoesNotExist:
            return [checks.Error(("The value of '%s' refers to '%s', which is not a callable, an attribute of '%s', or an attribute or method on '%s.%s'." % (label, item, obj.__class__.__name__, model._meta.app_label, model._meta.object_name)), obj=obj.__class__, id='admin.E108')]
        else:
            return []
