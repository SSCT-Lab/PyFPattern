@scenario('CreateServiceHook')
def create_hook_scenario(runner):
    runner.request(method='POST', path=('/projects/%s/%s/hooks/' % (runner.org.slug, runner.default_project.slug)), data={
        'url': 'https://example.com/sentry-hook',
        'events': ['event.alert', 'event.created'],
    })