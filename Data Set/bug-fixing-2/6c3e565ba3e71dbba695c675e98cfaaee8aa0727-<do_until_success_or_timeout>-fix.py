

def do_until_success_or_timeout(self, what, timeout, connect_timeout, what_desc, sleep=1):
    max_end_time = (datetime.utcnow() + timedelta(seconds=timeout))
    e = None
    while (datetime.utcnow() < max_end_time):
        try:
            what(connect_timeout)
            if what_desc:
                display.debug(('wait_for_connection: %s success' % what_desc))
            return
        except Exception as e:
            error = e
            if what_desc:
                display.debug(('wait_for_connection: %s fail (expected), retrying in %d seconds...' % (what_desc, sleep)))
            time.sleep(sleep)
    raise TimedOutException(('timed out waiting for %s: %s' % (what_desc, error)))
