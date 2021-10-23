def do_until_success_or_timeout(self, action, reboot_timeout, action_desc):
    max_end_time = (datetime.utcnow() + timedelta(seconds=reboot_timeout))
    fail_count = 0
    max_fail_sleep = 12
    while (datetime.utcnow() < max_end_time):
        try:
            action()
            if action_desc:
                display.debug(('%s: %s success' % (self._task.action, action_desc)))
            return
        except Exception as e:
            random_int = (random.randint(0, 1000) / 1000)
            fail_sleep = ((2 ** fail_count) + random_int)
            if (fail_sleep > max_fail_sleep):
                fail_sleep = (max_fail_sleep + random_int)
            if action_desc:
                display.debug("{0}: {1} fail '{2}', retrying in {3:.4} seconds...".format(self._task.action, action_desc, to_text(e), fail_sleep))
            fail_count += 1
            time.sleep(fail_sleep)
    raise TimedOutException(('Timed out waiting for %s (timeout=%s)' % (action_desc, reboot_timeout)))