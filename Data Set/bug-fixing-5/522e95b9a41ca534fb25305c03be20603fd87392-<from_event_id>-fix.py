def from_event_id(self, id_or_event_id, project_id):
    '\n        Get an Event by either its id primary key or its hex event_id.\n\n        Will automatically try to infer the type of id, and grab the correct\n        event.  If the provided id is a hex event_id, the project_id must also\n        be provided to disambiguate it.\n\n        Returns None if the event cannot be found under either scheme.\n        '
    event = None
    if (id_or_event_id.isdigit() and (int(id_or_event_id) <= BoundedBigIntegerField.MAX_VALUE)):
        try:
            if (project_id is None):
                event = self.get(id=id_or_event_id)
            else:
                event = self.get(id=id_or_event_id, project_id=project_id)
        except ObjectDoesNotExist:
            pass
    if ((project_id is not None) and (event is None) and is_event_id(id_or_event_id)):
        try:
            event = self.get(event_id=id_or_event_id, project_id=project_id)
        except ObjectDoesNotExist:
            pass
    return event