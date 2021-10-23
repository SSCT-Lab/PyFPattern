def test_field_string_value(self):
    '\n        Initialization of a geometry field with a valid/empty/invalid string.\n        Only the invalid string should trigger an error log entry.\n        '

    class PointForm(forms.Form):
        pt1 = forms.PointField(srid=4326)
        pt2 = forms.PointField(srid=4326)
        pt3 = forms.PointField(srid=4326)
    form = PointForm({
        'pt1': 'SRID=4326;POINT(7.3 44)',
        'pt2': '',
        'pt3': 'PNT(0)',
    })
    with patch_logger('django.contrib.gis', 'error') as logger_calls:
        output = str(form)
    self.assertInHTML('<textarea id="id_pt1" class="vSerializedField required" cols="150" rows="10" name="pt1">POINT (7.3 44)</textarea>', output)
    self.assertInHTML('<textarea id="id_pt2" class="vSerializedField required" cols="150" rows="10" name="pt2"></textarea>', output)
    self.assertInHTML('<textarea id="id_pt3" class="vSerializedField required" cols="150" rows="10" name="pt3"></textarea>', output)
    self.assertEqual(len(logger_calls), 1)
    self.assertEqual(logger_calls[0], "Error creating geometry from value 'PNT(0)' (String or unicode input unrecognized as WKT EWKT, and HEXEWKB.)")