def format_actor_option(actor):
    if isinstance(actor, User):
        return {
            'text': actor.get_display_name(),
            'value': 'user:{}'.format(actor.id),
        }
    if isinstance(actor, Team):
        return {
            'text': '#{}'.format(actor.slug),
            'value': 'team:{}'.format(actor.id),
        }
    raise NotImplementedError