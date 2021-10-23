def alter_db_table(self, model, old_db_table, new_db_table):
    from django.contrib.gis.db.models.fields import GeometryField
    for field in model._meta.local_fields:
        if isinstance(field, GeometryField):
            self.execute((self.sql_remove_geometry_metadata % {
                'table': self.quote_name(old_db_table),
                'column': self.quote_name(field.column),
            }))
    super(SpatialiteSchemaEditor, self).alter_db_table(model, old_db_table, new_db_table)
    for geom_table in self.geometry_tables:
        try:
            self.execute((self.sql_update_geometry_columns % {
                'geom_table': geom_table,
                'old_table': self.quote_name(old_db_table),
                'new_table': self.quote_name(new_db_table),
            }))
        except DatabaseError:
            pass
    for field in model._meta.local_fields:
        if isinstance(field, GeometryField):
            self.execute((self.sql_recover_geometry_metadata % {
                'table': self.geo_quote_name(new_db_table),
                'column': self.geo_quote_name(field.column),
                'srid': field.srid,
                'geom_type': self.geo_quote_name(field.geom_type),
                'dim': field.dim,
            }))
        if getattr(field, 'spatial_index', False):
            self.execute((self.sql_rename_table % {
                'old_table': self.quote_name(('idx_%s_%s' % (old_db_table, field.column))),
                'new_table': self.quote_name(('idx_%s_%s' % (new_db_table, field.column))),
            }))