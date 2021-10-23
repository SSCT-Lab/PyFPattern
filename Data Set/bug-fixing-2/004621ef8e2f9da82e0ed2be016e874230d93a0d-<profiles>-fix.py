

@property
def profiles(self):
    'Returns a list of profiles from the API\n\n        The profiles are formatted so that they are usable in this module and\n        are able to be compared by the Difference engine.\n\n        Returns:\n             list (:obj:`list` of :obj:`dict`): List of profiles.\n\n             Each dictionary in the list contains the following three (3) keys.\n\n             * name\n             * context\n             * fullPath\n\n        Raises:\n            F5ModuleError: If the specified context is a value other that\n                ``all``, ``server-side``, or ``client-side``.\n        '
    if ('items' not in self._values['profiles']):
        return None
    result = []
    for item in self._values['profiles']['items']:
        context = item['context']
        if (context == 'serverside'):
            context = 'server-side'
        elif (context == 'clientside'):
            context = 'client-side'
        name = item['name']
        if (context in ['all', 'server-side', 'client-side']):
            result.append(dict(name=name, context=context, full_path=item['fullPath']))
        else:
            raise F5ModuleError("Unknown profile context found: '{0}'".format(context))
    return result
