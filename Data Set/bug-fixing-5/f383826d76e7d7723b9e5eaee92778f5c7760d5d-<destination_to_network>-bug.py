def destination_to_network(self):
    destination = self._values['destination']
    if destination.startswith('default%'):
        destination = '0.0.0.0%{0}/0'.format(destination.split('%')[1])
    elif destination.startswith('default-inet6%'):
        destination = '::%{0}/::'.format(destination.split('%')[1])
    elif destination.startswith('default-inet6'):
        destination = '::/::'
    elif destination.startswith('default'):
        destination = '0.0.0.0/0'
    return destination