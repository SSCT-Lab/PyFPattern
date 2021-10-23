@scenario('CreateServiceHook')
def create_hook_scenario(runner):
    runner.request(method='POST', path=('/projects/%s/%s/hooks/' % (runner.org.slug, runner.default_project.slug)), data={
        'name': 'Fabulous Key',
    })