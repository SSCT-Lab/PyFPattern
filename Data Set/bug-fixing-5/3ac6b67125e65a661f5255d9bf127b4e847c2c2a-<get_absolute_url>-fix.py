def get_absolute_url(self, params=None):
    from sentry import features
    if features.has('organizations:sentry10', self.organization):
        url = reverse('sentry-organization-issue', args=[self.organization.slug, self.id])
        params = ({
            
        } if (params is None) else params)
        params['project'] = self.project.id
    else:
        url = reverse('sentry-group', args=[self.organization.slug, self.project.slug, self.id])
    if params:
        url = ((url + '?') + urlencode(params))
    return absolute_uri(url)