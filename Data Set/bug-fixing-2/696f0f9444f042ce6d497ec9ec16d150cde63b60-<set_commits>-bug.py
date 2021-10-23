

def set_commits(self, commit_list):
    '\n        Bind a list of commits to this release.\n\n        This will clear any existing commit log and replace it with the given\n        commits.\n        '
    commit_list.sort(key=(lambda commit: commit.get('date_added')), reverse=True)
    from sentry.models import Commit, CommitAuthor, Group, GroupLink, GroupResolution, GroupStatus, ReleaseCommit, ReleaseHeadCommit, Repository, PullRequest
    from sentry.plugins.providers.repository import RepositoryProvider
    commit_list = [c for c in commit_list if (not RepositoryProvider.should_ignore_commit(c.get('message', '')))]
    lock_key = type(self).get_lock_key(self.organization_id, self.id)
    lock = locks.get(lock_key, duration=10)
    with TimedRetryPolicy(10)(lock.acquire):
        with transaction.atomic():
            ReleaseCommit.objects.filter(release=self).delete()
            authors = {
                
            }
            repos = {
                
            }
            commit_author_by_commit = {
                
            }
            head_commit_by_repo = {
                
            }
            latest_commit = None
            for (idx, data) in enumerate(commit_list):
                repo_name = (data.get('repository') or 'organization-{}'.format(self.organization_id))
                if (repo_name not in repos):
                    repos[repo_name] = repo = Repository.objects.get_or_create(organization_id=self.organization_id, name=repo_name)[0]
                else:
                    repo = repos[repo_name]
                author_email = data.get('author_email')
                if ((author_email is None) and data.get('author_name')):
                    author_email = (re.sub('[^a-zA-Z0-9\\-_\\.]*', '', data['author_name']).lower() + '@localhost')
                if (not author_email):
                    author = None
                elif (author_email not in authors):
                    authors[author_email] = author = CommitAuthor.objects.get_or_create(organization_id=self.organization_id, email=author_email, defaults={
                        'name': data.get('author_name'),
                    })[0]
                    if (data.get('author_name') and (author.name != data['author_name'])):
                        author.update(name=data['author_name'])
                else:
                    author = authors[author_email]
                defaults = {
                    'message': data.get('message'),
                    'author': author,
                    'date_added': (data.get('timestamp') or timezone.now()),
                }
                (commit, created) = Commit.objects.get_or_create(organization_id=self.organization_id, repository_id=repo.id, key=data['id'], defaults=defaults)
                if (author is None):
                    author = commit.author
                commit_author_by_commit[commit.id] = author
                patch_set = data.get('patch_set', [])
                for patched_file in patch_set:
                    CommitFileChange.objects.get_or_create(organization_id=self.organization.id, commit=commit, filename=patched_file['path'], type=patched_file['type'])
                if (not created):
                    update_kwargs = {
                        
                    }
                    if ((commit.message is None) and (defaults['message'] is not None)):
                        update_kwargs['message'] = defaults['message']
                    if ((commit.author_id is None) and (defaults['author'] is not None)):
                        update_kwargs['author'] = defaults['author']
                    if update_kwargs:
                        commit.update(**update_kwargs)
                ReleaseCommit.objects.create(organization_id=self.organization_id, release=self, commit=commit, order=idx)
                if (latest_commit is None):
                    latest_commit = commit
                head_commit_by_repo.setdefault(repo.id, commit.id)
            self.update(commit_count=len(commit_list), authors=[six.text_type(a_id) for a_id in ReleaseCommit.objects.filter(release=self, commit__author_id__isnull=False).values_list('commit__author_id', flat=True).distinct()], last_commit_id=(latest_commit.id if latest_commit else None))
    for (repo_id, commit_id) in six.iteritems(head_commit_by_repo):
        try:
            with transaction.atomic():
                ReleaseHeadCommit.objects.create(organization_id=self.organization_id, release_id=self.id, repository_id=repo_id, commit_id=commit_id)
        except IntegrityError:
            pass
    release_commits = list(ReleaseCommit.objects.filter(release=self).select_related('commit').values('commit_id', 'commit__key'))
    commit_resolutions = list(GroupLink.objects.filter(linked_type=GroupLink.LinkedType.commit, linked_id__in=[rc['commit_id'] for rc in release_commits]).values_list('group_id', 'linked_id'))
    commit_group_authors = [(cr[0], commit_author_by_commit.get(cr[1])) for cr in commit_resolutions]
    pr_ids_by_merge_commit = list(PullRequest.objects.filter(merge_commit_sha__in=[rc['commit__key'] for rc in release_commits], organization_id=self.organization_id).values_list('id', flat=True))
    pull_request_resolutions = list(GroupLink.objects.filter(relationship=GroupLink.Relationship.resolves, linked_type=GroupLink.LinkedType.pull_request, linked_id__in=pr_ids_by_merge_commit).values_list('group_id', 'linked_id'))
    pr_authors = list(PullRequest.objects.filter(id__in=[prr[1] for prr in pull_request_resolutions]).select_related('author'))
    pr_authors_dict = {pra.id: pra.author for pra in pr_authors}
    pull_request_group_authors = [(prr[0], pr_authors_dict.get(prr[1])) for prr in pull_request_resolutions]
    user_by_author = {
        None: None,
    }
    for (group_id, author) in itertools.chain(commit_group_authors, pull_request_group_authors):
        if (author not in user_by_author):
            try:
                user_by_author[author] = author.find_users()[0]
            except IndexError:
                user_by_author[author] = None
        actor = user_by_author[author]
        with transaction.atomic():
            GroupResolution.objects.create_or_update(group_id=group_id, values={
                'release': self,
                'type': GroupResolution.Type.in_release,
                'status': GroupResolution.Status.resolved,
                'actor_id': (actor.id if actor else None),
            })
            Group.objects.filter(id=group_id).update(status=GroupStatus.RESOLVED)
