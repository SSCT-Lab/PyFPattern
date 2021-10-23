def _forwards(self, orm):
    idps = orm.IdentityProvider.objects.filter(external_id=None)
    for r in RangeQuerySetWrapperWithProgressBar(idps):
        try:
            integration = orm.Integration.objects.filter(organizations=r.organization_id)[0]
        except IndexError:
            continue
        orm.IdentityProvider.objects.filter(id=r.id, external_id=None).update(external_id=integration.external_id)