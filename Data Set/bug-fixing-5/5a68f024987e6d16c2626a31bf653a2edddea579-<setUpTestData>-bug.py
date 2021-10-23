@classmethod
def setUpTestData(cls):
    cls.objs = [NullableUUIDModel.objects.create(field=uuid.uuid4()), NullableUUIDModel.objects.create(field='550e8400e29b41d4a716446655440000'), NullableUUIDModel.objects.create(field=None)]