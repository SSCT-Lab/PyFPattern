

@instrumented_task(name='sentry.tasks.integrations.migrate_repo', queue='integrations', default_retry_delay=(60 * 5), max_retries=5)
@retry(exclude=(Integration.DoesNotExist, Repository.DoesNotExist, Organization.DoesNotExist))
def migrate_repo(repo_id, integration_id, organization_id):
    integration = Integration.objects.get(id=integration_id)
    installation = integration.get_installation(organization_id=organization_id)
    repo = Repository.objects.get(id=repo_id)
    if installation.has_repo_access(repo):
        repo.integration_id = integration_id
        repo.provider = 'integrations:github'
        repo.save()
        PluginMigrator(integration, Organization.objects.get(id=organization_id)).call()
