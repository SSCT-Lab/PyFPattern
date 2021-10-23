

@scenario('CreateNewOrganizationReleaseWithCommits')
def create_new_org_release_commit_scenario(runner):
    runner.request(method='POST', path=('/organizations/%s/releases/' % (runner.org.slug,)), data={
        'version': '2.0rc2',
        'projects': [runner.default_project.slug],
        'commits': [{
            'patch_set': [{
                'path': 'path/to/added-file.html',
                'type': 'A',
            }, {
                'path': 'path/to/modified-file.html',
                'type': 'M',
            }, {
                'path': 'path/to/deleted-file.html',
                'type': 'D',
            }],
            'repository': 'owner-name/repo-name',
            'author_name': 'Author Name',
            'author_email': 'author_email@example.com',
            'timestamp': '2018-09-20T11:50:22+03:00',
            'message': 'This is the commit message.',
            'id': '8371445ab8a9facd271df17038ff295a48accae7',
        }],
    })
