def render_template_from_field(self, content, context, jinja_env):
    '\n        Renders a template from a field. If the field is a string, it will\n        simply render the string and return the result. If it is a collection or\n        nested set of collections, it will traverse the structure and render\n        all strings in it.\n        '
    rt = self.render_template
    if isinstance(content, six.string_types):
        result = jinja_env.from_string(content).render(**context)
    elif isinstance(content, (list, tuple)):
        result = [rt(e, context) for e in content]
    elif isinstance(content, dict):
        result = {k: rt(v, context) for (k, v) in list(content.items())}
    else:
        param_type = type(content)
        msg = "Type '{param_type}' used for parameter '{attr}' is not supported for templating".format(**locals())
        raise AirflowException(msg)
    return result