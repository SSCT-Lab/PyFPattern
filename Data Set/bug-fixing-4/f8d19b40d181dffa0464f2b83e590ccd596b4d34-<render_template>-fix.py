def render_template(self, attr, content, context):
    '\n        Renders a template either from a file or directly in a field, and returns\n        the rendered result.\n        '
    jinja_env = (self.dag.get_template_env() if hasattr(self, 'dag') else jinja2.Environment(cache_size=0))
    exts = self.__class__.template_ext
    if (isinstance(content, six.string_types) and any([content.endswith(ext) for ext in exts])):
        return jinja_env.get_template(content).render(**context)
    else:
        return self.render_template_from_field(attr, content, context, jinja_env)