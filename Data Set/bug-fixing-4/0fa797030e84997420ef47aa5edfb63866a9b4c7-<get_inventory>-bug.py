def get_inventory(self):
    'Generate Ansible inventory.\n        '
    groups = dict()
    meta = dict()
    meta['hostvars'] = dict()
    instances_api = libbrook.InstancesApi(self.client)
    projects_api = libbrook.ProjectsApi(self.client)
    templates_api = libbrook.TemplatesApi(self.client)
    if (not self.project_id):
        projects = [project.id for project in projects_api.index_projects()]
    else:
        projects = [self.project_id]
    for project_id in projects:
        project = projects_api.show_project(project_id=project_id)
        for instance in instances_api.index_instances(project_id=project_id):
            template = templates_api.show_template(template_id=instance.template)
            try:
                meta['hostvars'][instance.name] = self.hostvars(project, instance, template, instances_api)
            except libbrook.rest.ApiException:
                continue
            project_group = ('project_%s' % project.name)
            if (project_group in groups):
                groups[project_group].append(instance.name)
            else:
                groups[project_group] = [instance.name]
            status_group = ('status_%s' % meta['hostvars'][instance.name]['brook_status'])
            if (status_group in groups):
                groups[status_group].append(instance.name)
            else:
                groups[status_group] = [instance.name]
            tags = meta['hostvars'][instance.name]['brook_tags']
            for tag in tags:
                tag_group = ('tag_%s' % tag)
                if (tag_group in groups):
                    groups[tag_group].append(instance.name)
                else:
                    groups[tag_group] = [instance.name]
    groups['_meta'] = meta
    return groups