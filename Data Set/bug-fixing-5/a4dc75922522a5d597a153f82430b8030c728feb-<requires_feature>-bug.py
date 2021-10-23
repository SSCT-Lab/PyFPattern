def requires_feature(feature, any_org=None):
    "\n    Require a feature flag to access an endpoint.\n\n    If ``any_org`` is ``True``, this will check all of the request User's\n    Organizations for the flag. If any are flagged in, the endpoint is accessible.\n\n    Without ``any_org=True``, the endpoint must resolve an Organization via\n    ``convert_args`` (and therefor be in ``kwargs``). The resolved Org must have\n    the passed feature.\n\n    If any failure case, the API returns a 404.\n\n    Example:\n        >>> @requires_feature('organizations:internal-catchall')\n        >>> def get(self, request, organization):\n        >>>     return Response()\n    "

    def decorator(func):

        def wrapped(self, request, *args, **kwargs):
            if any_org:
                if (not any((features.has(feature, org) for org in request.user.get_orgs()))):
                    return Response(status=404)
                return func(self, request, *args, **kwargs)
            else:
                if ('organization' not in kwargs):
                    return Response(status=404)
                if (not features.has(feature, kwargs['organization'])):
                    return Response(status=404)
                return func(self, request, *args, **kwargs)
        return wrapped
    return decorator