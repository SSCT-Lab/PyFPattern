

def get_geom_placeholder(self, f, value, compiler):
    '\n        Provide a proper substitution value for Geometries or rasters that are\n        not in the SRID of the field. Specifically, this routine will\n        substitute in the ST_Transform() function call.\n        '
    transform_func = self.spatial_function_name('Transform')
    if hasattr(value, 'as_sql'):
        if (value.field.srid == f.srid):
            placeholder = '%s'
        else:
            placeholder = ('%s(%%s, %s)' % (transform_func, f.srid))
        return placeholder
    if (value is None):
        value_srid = None
    else:
        value_srid = value.srid
    if ((value_srid is None) or (value_srid == f.srid)):
        placeholder = '%s'
    else:
        placeholder = ('%s(%%s, %s)' % (transform_func, f.srid))
    return placeholder
