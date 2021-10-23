

def test_all_gis_lookups_with_rasters(self):
    "\n        Evaluate all possible lookups for all input combinations (i.e.\n        raster-raster, raster-geom, geom-raster) and for projected and\n        unprojected coordinate systems. This test just checks that the lookup\n        can be called, but doesn't check if the result makes logical sense.\n        "
    from django.contrib.gis.db.backends.postgis.operations import PostGISOperations
    rast = GDALRaster(json.loads(JSON_RASTER))
    stx_pnt = GEOSGeometry('POINT (-95.370401017314293 29.704867409475465)', 4326)
    stx_pnt.transform(3086)
    for (name, lookup) in BaseSpatialField.get_lookups().items():
        if (not isinstance(lookup, GISLookup)):
            continue
        combo_keys = [(field + name) for field in ['rast__', 'rast__', 'rastprojected__0__', 'rast__', 'rastprojected__', 'geom__', 'rast__']]
        if issubclass(lookup, DistanceLookupBase):
            combo_values = [(rast, 50, 'spheroid'), (rast, 0, 50, 'spheroid'), (rast, 0, D(km=1)), (stx_pnt, 0, 500), (stx_pnt, D(km=1000)), (rast, 500), (json.loads(JSON_RASTER), 500)]
        elif (name == 'relate'):
            combo_values = [(rast, 'T*T***FF*'), (rast, 0, 'T*T***FF*'), (rast, 0, 'T*T***FF*'), (stx_pnt, 0, 'T*T***FF*'), (stx_pnt, 'T*T***FF*'), (rast, 'T*T***FF*'), (json.loads(JSON_RASTER), 'T*T***FF*')]
        elif (name == 'isvalid'):
            continue
        elif PostGISOperations.gis_operators[name].func:
            combo_values = [rast, (rast, 0), (rast, 0), (stx_pnt, 0), stx_pnt, rast, rast, json.loads(JSON_RASTER)]
        else:
            combo_keys[2] = ('rastprojected__' + name)
            combo_values = [rast, rast, rast, stx_pnt, stx_pnt, rast, rast, json.loads(JSON_RASTER)]
        combos = [{
            x[0]: x[1],
        } for x in zip(combo_keys, combo_values)]
        for combo in combos:
            qs = RasterModel.objects.filter(**combo)
            self.assertIn(qs.count(), [0, 1])
        qs = RasterModel.objects.filter((Q(**combos[0]) & Q(**combos[1])))
        self.assertIn(qs.count(), [0, 1])
