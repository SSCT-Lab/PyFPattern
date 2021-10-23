def get_create_meta_for_project(self, project):
    params = {
        'expand': 'projects.issuetypes.fields',
        'projectIds': project,
    }
    metas = self.get_cached(self.META_URL, params=params)
    if (not metas):
        return None
    if (len(metas['projects']) > 1):
        raise ApiError('More than one project found.')
    try:
        return metas['projects'][0]
    except IndexError:
        return None