def render_to_string(template, context=None, request=None):
    if (context and ('team' in context) and isinstance(context['team'], Team)):
        team = context['team']
    else:
        team = None
    default_context = get_default_context(request, context, team=team)
    if (context is None):
        context = default_context
    else:
        context = dict(context)
        context.update(default_context)
    return loader.render_to_string(template, context=context, request=request)