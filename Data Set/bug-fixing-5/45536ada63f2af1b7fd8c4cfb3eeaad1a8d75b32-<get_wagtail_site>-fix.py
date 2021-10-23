def get_wagtail_site(self):
    site = getattr(self.request, 'site', None)
    if (site is None):
        from wagtail.core.models import Site
        return Site.objects.select_related('root_page').get(is_default_site=True)
    return site