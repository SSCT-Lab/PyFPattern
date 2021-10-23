def render_templates(self):
    task = self.task
    jinja_context = self.get_template_context()
    if (hasattr(self, 'task') and hasattr(self.task, 'dag')):
        if self.task.dag.user_defined_macros:
            jinja_context.update(self.task.dag.user_defined_macros)
    rt = self.task.render_template
    for attr in task.__class__.template_fields:
        content = getattr(task, attr)
        if content:
            rendered_content = rt(content, jinja_context)
            setattr(task, attr, rendered_content)