def get(self, request, project, event_id):
    '\n        Retrieve suggested owners information for an event\n        ``````````````````````````````````````````````````\n\n        :pparam string project_slug: the slug of the project the event\n                                     belongs to.\n        :pparam string event_id: the id of the event.\n        :auth: required\n        '
    event = eventstore.get_event_by_id(project.id, event_id)
    if (event is None):
        return Response({
            'detail': 'Event not found',
        }, status=404)
    event.bind_node_data()
    (owners, rules) = ProjectOwnership.get_owners(project.id, event.data)
    if (owners == ProjectOwnership.Everyone):
        owners = []
    return Response({
        'owners': serialize(Actor.resolve_many(owners), request.user, ActorSerializer()),
        'rule': (rules[0].matcher if rules else None),
        'rules': (rules or []),
    })