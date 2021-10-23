def _get_init_containers(self, volume_mounts):
    'When using git to retrieve the DAGs, use the GitSync Init Container'
    if self.kube_config.dags_volume_claim:
        return []
    init_environment = [{
        'name': 'GIT_SYNC_REPO',
        'value': self.kube_config.git_repo,
    }, {
        'name': 'GIT_SYNC_BRANCH',
        'value': self.kube_config.git_branch,
    }, {
        'name': 'GIT_SYNC_ROOT',
        'value': os.path.join(self.worker_airflow_dags, self.kube_config.git_subpath),
    }, {
        'name': 'GIT_SYNC_DEST',
        'value': 'dags',
    }, {
        'name': 'GIT_SYNC_ONE_TIME',
        'value': 'true',
    }]
    if self.kube_config.git_user:
        init_environment.append({
            'name': 'GIT_SYNC_USERNAME',
            'value': self.kube_config.git_user,
        })
    if self.kube_config.git_password:
        init_environment.append({
            'name': 'GIT_SYNC_PASSWORD',
            'value': self.kube_config.git_password,
        })
    volume_mounts[0]['readOnly'] = False
    return [{
        'name': self.kube_config.git_sync_init_container_name,
        'image': self.kube_config.git_sync_container,
        'securityContext': {
            'runAsUser': 0,
        },
        'env': init_environment,
        'volumeMounts': volume_mounts,
    }]