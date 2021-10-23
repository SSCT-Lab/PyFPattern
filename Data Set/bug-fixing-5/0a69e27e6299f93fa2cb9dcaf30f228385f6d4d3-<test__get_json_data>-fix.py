def test__get_json_data(mocker):
    'test the json conversion of _get_url_data'
    timeout = 30
    params = {
        'url': GITHUB_DATA['url'],
        'timeout': timeout,
    }
    module = mocker.Mock()
    module.params = params
    JenkinsPlugin._csrf_enabled = pass_function
    JenkinsPlugin._get_installed_plugins = pass_function
    JenkinsPlugin._get_url_data = mocker.Mock()
    JenkinsPlugin._get_url_data.return_value = BytesIO(GITHUB_DATA['response'])
    jenkins_plugin = JenkinsPlugin(module)
    json_data = jenkins_plugin._get_json_data('{url}'.format(url=GITHUB_DATA['url']), 'CSRF')
    assert isinstance(json_data, collections.Mapping)