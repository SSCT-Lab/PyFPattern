def _remake_table(self, model, create_fields=[], delete_fields=[], alter_fields=[]):
    '\n        Shortcut to transform a model from old_model into new_model\n\n        The essential steps are:\n          1. rename the model\'s existing table, e.g. "app_model" to "app_model__old"\n          2. create a table with the updated definition called "app_model"\n          3. copy the data from the old renamed table to the new table\n          4. delete the "app_model__old" table\n        '

    def is_self_referential(f):
        return (f.is_relation and (f.remote_field.model is model))
    body = {f.name: (f.clone() if is_self_referential(f) else f) for f in model._meta.local_concrete_fields}
    mapping = {f.column: self.quote_name(f.column) for f in model._meta.local_concrete_fields}
    rename_mapping = {
        
    }
    restore_pk_field = None
    if (any((f.primary_key for f in create_fields)) or any((n.primary_key for (o, n) in alter_fields))):
        for (name, field) in list(body.items()):
            if field.primary_key:
                field.primary_key = False
                restore_pk_field = field
                if field.auto_created:
                    del body[name]
                    del mapping[field.column]
    for field in create_fields:
        body[field.name] = field
        if ((not field.many_to_many) and field.concrete):
            mapping[field.column] = self.quote_value(self.effective_default(field))
    for (old_field, new_field) in alter_fields:
        body.pop(old_field.name, None)
        mapping.pop(old_field.column, None)
        body[new_field.name] = new_field
        if (old_field.null and (not new_field.null)):
            case_sql = ('coalesce(%(col)s, %(default)s)' % {
                'col': self.quote_name(old_field.column),
                'default': self.quote_value(self.effective_default(new_field)),
            })
            mapping[new_field.column] = case_sql
        else:
            mapping[new_field.column] = self.quote_name(old_field.column)
        rename_mapping[old_field.name] = new_field.name
    for field in delete_fields:
        del body[field.name]
        del mapping[field.column]
        if (field.many_to_many and field.remote_field.through._meta.auto_created):
            return self.delete_model(field.remote_field.through)
    apps = Apps()
    body = copy.deepcopy(body)
    unique_together = [[rename_mapping.get(n, n) for n in unique] for unique in model._meta.unique_together]
    index_together = [[rename_mapping.get(n, n) for n in index] for index in model._meta.index_together]
    meta_contents = {
        'app_label': model._meta.app_label,
        'db_table': model._meta.db_table,
        'unique_together': unique_together,
        'index_together': index_together,
        'apps': apps,
    }
    meta = type('Meta', tuple(), meta_contents)
    body['Meta'] = meta
    body['__module__'] = model.__module__
    temp_model = type(model._meta.object_name, model.__bases__, body)

    @contextlib.contextmanager
    def altered_table_name(model, temporary_table_name):
        original_table_name = model._meta.db_table
        model._meta.db_table = temporary_table_name
        (yield)
        model._meta.db_table = original_table_name
    with altered_table_name(model, (model._meta.db_table + '__old')):
        self.alter_db_table(model, temp_model._meta.db_table, model._meta.db_table)
        self.deferred_sql = [x for x in self.deferred_sql if (temp_model._meta.db_table not in x)]
        self.create_model(temp_model)
        field_maps = list(mapping.items())
        self.execute(('INSERT INTO %s (%s) SELECT %s FROM %s' % (self.quote_name(temp_model._meta.db_table), ', '.join((self.quote_name(x) for (x, y) in field_maps)), ', '.join((y for (x, y) in field_maps)), self.quote_name(model._meta.db_table))))
        self.delete_model(model, handle_autom2m=False)
    for sql in self.deferred_sql:
        self.execute(sql)
    self.deferred_sql = []
    if restore_pk_field:
        restore_pk_field.primary_key = True