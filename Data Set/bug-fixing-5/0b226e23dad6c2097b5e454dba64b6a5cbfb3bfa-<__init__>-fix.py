def __init__(self, activity):
    super(ReleaseActivityEmail, self).__init__(activity)
    self.organization = self.project.organization
    self.user_id_team_lookup = None
    try:
        self.deploy = Deploy.objects.get(id=activity.data['deploy_id'])
    except Deploy.DoesNotExist:
        self.deploy = None
    try:
        self.release = Release.objects.get(organization_id=self.project.organization_id, version=activity.data['version'])
    except Release.DoesNotExist:
        self.release = None
        self.repos = []
        self.projects = []
    else:
        self.projects = list(self.release.projects.all())
        self.commit_list = [rc.commit for rc in ReleaseCommit.objects.filter(release=self.release).select_related('commit', 'commit__author')]
        repos = {r['id']: {
            'name': r['name'],
            'commits': [],
        } for r in Repository.objects.filter(organization_id=self.project.organization_id, id__in={c.repository_id for c in self.commit_list}).values('id', 'name')}
        self.email_list = set([c.author.email for c in self.commit_list if c.author])
        if self.email_list:
            users = {ue.email: ue.user for ue in UserEmail.objects.filter(in_iexact('email', self.email_list), is_verified=True, user__sentry_orgmember_set__organization=self.organization).select_related('user')}
        else:
            users = {
                
            }
        for commit in self.commit_list:
            repos[commit.repository_id]['commits'].append((commit, (users.get(commit.author.email) if commit.author_id else None)))
        self.repos = repos.values()
        self.environment = (Environment.objects.get(id=self.deploy.environment_id).name or 'Default Environment')
        self.group_counts_by_project = {row['project']: row['num_groups'] for row in Group.objects.filter(project__in=self.projects, id__in=GroupCommitResolution.objects.filter(commit_id__in=ReleaseCommit.objects.filter(release=self.release).values_list('commit_id', flat=True)).values_list('group_id', flat=True)).values('project').annotate(num_groups=Count('id'))}