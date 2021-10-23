def list_elbs(self):
    (elb_array, token) = ([], None)
    get_elb_with_backoff = AWSRetry.backoff(tries=5, delay=5, backoff=2.0)(self.connection.get_all_load_balancers)
    while True:
        all_elbs = get_elb_with_backoff(marker=token)
        token = all_elbs.next_marker
        if all_elbs:
            if self.names:
                for existing_lb in all_elbs:
                    if (existing_lb.name in self.names):
                        elb_array.append(existing_lb)
            else:
                elb_array.extend(all_elbs)
        else:
            break
        if (token is None):
            break
    return list(map(self._get_elb_info, elb_array))