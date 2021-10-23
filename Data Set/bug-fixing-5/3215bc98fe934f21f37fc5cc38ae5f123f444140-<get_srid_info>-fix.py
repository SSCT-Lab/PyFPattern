def get_srid_info(srid, connection):
    '\n    Returns the units, unit name, and spheroid WKT associated with the\n    given SRID from the `spatial_ref_sys` (or equivalent) spatial database\n    table for the given database connection.  These results are cached.\n    '
    from django.contrib.gis.gdal import SpatialReference
    global _srid_cache
    try:
        SpatialRefSys = connection.ops.spatial_ref_sys()
    except NotImplementedError:
        SpatialRefSys = None
    (alias, get_srs) = ((connection.alias, (lambda srid: SpatialRefSys.objects.using(connection.alias).get(srid=srid).srs)) if SpatialRefSys else (None, SpatialReference))
    if (srid not in _srid_cache[alias]):
        srs = get_srs(srid)
        (units, units_name) = srs.units
        sphere_name = srs['spheroid']
        spheroid = ('SPHEROID["%s",%s,%s]' % (sphere_name, srs.semi_major, srs.inverse_flattening))
        _srid_cache[alias][srid] = (units, units_name, spheroid)
    return _srid_cache[alias][srid]