def _alter_many_to_many(self, model, old_field, new_field, strict):
    '\n        Alters M2Ms to repoint their to= endpoints.\n        '
    if (old_field.remote_field.through._meta.db_table == new_field.remote_field.through._meta.db_table):
        self._remake_table(old_field.remote_field.through, alter_fields=[(old_field.remote_field.through._meta.get_field(old_field.m2m_reverse_field_name()), new_field.remote_field.through._meta.get_field(new_field.m2m_reverse_field_name()))], override_uniques=(new_field.m2m_field_name(), new_field.m2m_reverse_field_name()))
        return
    self.create_model(new_field.remote_field.through)
    self.execute(('INSERT INTO %s (%s) SELECT %s FROM %s' % (self.quote_name(new_field.remote_field.through._meta.db_table), ', '.join(['id', new_field.m2m_column_name(), new_field.m2m_reverse_name()]), ', '.join(['id', old_field.m2m_column_name(), old_field.m2m_reverse_name()]), self.quote_name(old_field.remote_field.through._meta.db_table))))
    self.delete_model(old_field.remote_field.through)