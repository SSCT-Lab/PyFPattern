def create_environment(self, **kwargs):
    project = kwargs.get('project', self.project)
    name = kwargs.get('name', petname.Generate(1, ' ', letters=10))
    return Environment.get_or_create(project=project, name=name)