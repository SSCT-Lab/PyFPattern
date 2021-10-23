

def get_wagtail_site(self):
    site = getattr(self.request, 'site', None)
    if (site is None):
        return Site.objects.select_related('root_page').get(is_default_site=True)
    return site
