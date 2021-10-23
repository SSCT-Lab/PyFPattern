

def create_environment(self, **kwargs):
    project = kwargs.get('project', self.project)
    name = kwargs.get('name', petname.Generate(3, ' ', letters=10)[:64])
    env = Environment.objects.create(organization_id=project.organization_id, project_id=project.id, name=name)
    env.add_project(project)
    return env
