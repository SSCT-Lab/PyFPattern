def compare_listeners(connection, module, current_listeners, new_listeners, purge_listeners):
    '\n    Compare listeners and return listeners to add, listeners to modify and listeners to remove\n    Listeners are compared based on port\n\n    :param current_listeners:\n    :param new_listeners:\n    :param purge_listeners:\n    :return:\n    '
    listeners_to_modify = []
    listeners_to_delete = []
    for current_listener in current_listeners:
        current_listener_passed_to_module = False
        for new_listener in new_listeners[:]:
            if (current_listener['Port'] == new_listener['Port']):
                current_listener_passed_to_module = True
                new_listeners.remove(new_listener)
                modified_listener = compare_listener(current_listener, new_listener)
                if modified_listener:
                    modified_listener['Port'] = current_listener['Port']
                    modified_listener['ListenerArn'] = current_listener['ListenerArn']
                    listeners_to_modify.append(modified_listener)
                break
        if ((not current_listener_passed_to_module) and purge_listeners):
            listeners_to_delete.append(current_listener['ListenerArn'])
    listeners_to_add = new_listeners
    return (listeners_to_add, listeners_to_modify, listeners_to_delete)