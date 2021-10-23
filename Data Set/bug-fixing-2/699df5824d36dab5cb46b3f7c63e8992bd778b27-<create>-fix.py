

def create(self, entity=None, result_state=None, fail_condition=(lambda e: False), search_params=None, update_params=None, **kwargs):
    "\n        Method which is called when state of the entity is 'present'. If user\n        don't provide `entity` parameter the entity is searched using\n        `search_params` parameter. If entity is found it's updated, whether\n        the entity should be updated is checked by `update_check` method.\n        The corresponding updated entity is build by `build_entity` method.\n\n        Function executed after entity is created can optionally be specified\n        in `post_create` parameter. Function executed after entity is updated\n        can optionally be specified in `post_update` parameter.\n\n        :param entity: Entity we want to update, if exists.\n        :param result_state: State which should entity has in order to finish task.\n        :param fail_condition: Function which checks incorrect state of entity, if it returns `True` Exception is raised.\n        :param search_params: Dictionary of parameters to be used for search.\n        :param update_params: The params which should be passed to update method.\n        :param kwargs: Additional parameters passed when creating entity.\n        :return: Dictionary with values returned by Ansible module.\n        "
    if (entity is None):
        entity = self.search_entity(search_params)
    self.pre_create(entity)
    if entity:
        entity_service = self._service.service(entity.id)
        if (not self.update_check(entity)):
            new_entity = self.build_entity()
            if (not self._module.check_mode):
                update_params = (update_params or {
                    
                })
                updated_entity = entity_service.update(new_entity, **update_params)
                self.post_update(entity)
            if self._module._diff:
                before = get_dict_of_struct(entity, self._connection, fetch_nested=True, attributes=['name'])
                after = before.copy()
                self.diff_update(after, get_dict_of_struct(new_entity))
                self._diff['before'] = before
                self._diff['after'] = after
            self.changed = True
    else:
        if (not self._module.check_mode):
            entity = self._service.add(self.build_entity(), **kwargs)
            self.post_create(entity)
        self.changed = True
    entity_service = self._service.service(entity.id)
    state_condition = (lambda entity: entity)
    if result_state:
        state_condition = (lambda entity: (entity and (entity.status == result_state)))
    wait(service=entity_service, condition=state_condition, fail_condition=fail_condition, wait=self._module.params['wait'], timeout=self._module.params['timeout'], poll_interval=self._module.params['poll_interval'])
    return {
        'changed': self.changed,
        'id': entity.id,
        type(entity).__name__.lower(): get_dict_of_struct(struct=entity, connection=self._connection, fetch_nested=self._module.params.get('fetch_nested'), attributes=self._module.params.get('nested_attributes')),
        'diff': self._diff,
    }
