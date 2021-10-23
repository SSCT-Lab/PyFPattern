@classmethod
def setUpTestData(cls):
    cls.objs = [NullableUUIDModel.objects.create(field=uuid.UUID('25d405be-4895-4d50-9b2e-d6695359ce47')), NullableUUIDModel.objects.create(field='550e8400e29b41d4a716446655440000'), NullableUUIDModel.objects.create(field=None)]