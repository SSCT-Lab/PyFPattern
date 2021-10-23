

def test_key_transform_expression(self):
    self.assertSequenceEqual(JSONModel.objects.filter(field__d__0__isnull=False).annotate(key=KeyTransform('d', 'field')).annotate(chain=KeyTransform('0', 'key'), expr=KeyTransform('0', Cast('key', JSONField()))).filter(chain=F('expr')), [self.objs[8]])
