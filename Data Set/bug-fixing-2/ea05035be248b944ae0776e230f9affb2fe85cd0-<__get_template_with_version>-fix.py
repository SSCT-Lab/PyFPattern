

def __get_template_with_version(self):
    "\n        oVirt/RHV in version 4.1 doesn't support search by template+version_number,\n        so we need to list all templates with specific name and then iterate\n        through it's version until we find the version we look for.\n        "
    template = None
    if self.param('template'):
        templates_service = self._connection.system_service().templates_service()
        templates = templates_service.list(search=('name=%s' % self.param('template')))
        if self.param('template_version'):
            templates = [t for t in templates if (t.version.version_number == self.param('template_version'))]
        if (not templates):
            raise ValueError(("Template with name '%s' and version '%s' was not found'" % (self.param('template'), self.param('template_version'))))
        template = sorted(templates, key=(lambda t: t.version.version_number), reverse=True)[0]
    return template
