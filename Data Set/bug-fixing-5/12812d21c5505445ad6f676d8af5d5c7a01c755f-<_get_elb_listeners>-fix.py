def _get_elb_listeners(self, listeners):
    listener_list = []
    for listener in listeners:
        listener_dict = {
            'load_balancer_port': listener[0],
            'instance_port': listener[1],
            'protocol': listener[2],
            'instance_protocol': listener[3],
        }
        try:
            ssl_certificate_id = listener[4]
        except IndexError:
            pass
        else:
            if ssl_certificate_id:
                listener_dict['ssl_certificate_id'] = ssl_certificate_id
        listener_list.append(listener_dict)
    return listener_list