def list_elbs(self):
    (elb_array, token) = ([], None)
    while True:
        try:
            all_elbs = self.connection.get_all_load_balancers(marker=token)
            token = all_elbs.next_token
        except BotoServerError as err:
            self.module.fail_json(msg=('%s: %s' % (err.error_code, err.error_message)), exception=traceback.format_exc())
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