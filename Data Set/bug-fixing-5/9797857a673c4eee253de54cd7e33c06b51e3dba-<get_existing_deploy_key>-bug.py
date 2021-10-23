def get_existing_deploy_key(module, bitbucket):
    '\n    Search for an existing deploy key on Bitbucket\n    with the label specified in module param `label`\n\n    :param module: instance of the :class:`AnsibleModule`\n    :param bitbucket: instance of the :class:`BitbucketHelper`\n    :return: existing deploy key or None if not found\n    :rtype: dict or None\n\n    Return example::\n\n        {\n            "id": 123,\n            "label": "mykey",\n            "created_on": "2019-03-23T10:15:21.517377+00:00",\n            "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADA...AdkTg7HGqL3rlaDrEcWfL7Lu6TnhBdq5",\n            "type": "deploy_key",\n            "comment": "",\n            "last_used": None,\n            "repository": {\n                "links": {\n                    "self": {\n                        "href": "https://api.bitbucket.org/2.0/repositories/mleu/test"\n                    },\n                    "html": {\n                        "href": "https://bitbucket.org/mleu/test"\n                    },\n                    "avatar": {\n                        "href": "..."\n                    }\n                },\n                "type": "repository",\n                "name": "test",\n                "full_name": "mleu/test",\n                "uuid": "{85d08b4e-571d-44e9-a507-fa476535aa98}"\n            },\n            "links": {\n                "self": {\n                    "href": "https://api.bitbucket.org/2.0/repositories/mleu/test/deploy-keys/123"\n                }\n            },\n        }\n    '
    content = {
        'next': BITBUCKET_API_ENDPOINTS['deploy-key-list'].format(username=module.params['username'], repo_slug=module.params['repository']),
    }
    while ('next' in content):
        (info, content) = bitbucket.request(api_url=content['next'], method='GET')
        if (info['status'] == 404):
            module.fail_json(msg=error_messages['invalid_username_or_repo'])
        if (info['status'] == 403):
            module.fail_json(msg=error_messages['required_permission'])
        if (info['status'] != 200):
            module.fail_json(msg='Failed to retrieve the list of deploy keys: {0}'.format(info))
        res = next(filter((lambda v: (v['label'] == module.params['label'])), content['values']), None)
        if (res is not None):
            return res
    return None