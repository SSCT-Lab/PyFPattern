

def main():
    module = AnsibleModule(argument_spec=dict(host=dict(default='127.0.0.1'), timeout=dict(default=300, type='int'), connect_timeout=dict(default=5, type='int'), delay=dict(default=0, type='int'), port=dict(default=None, type='int'), active_connection_states=dict(default=['ESTABLISHED', 'SYN_SENT', 'SYN_RECV', 'FIN_WAIT1', 'FIN_WAIT2', 'TIME_WAIT'], type='list'), path=dict(default=None, type='path'), search_regex=dict(default=None), state=dict(default='started', choices=['started', 'stopped', 'present', 'absent', 'drained']), exclude_hosts=dict(default=None, type='list'), sleep=dict(default=1, type='int')))
    params = module.params
    host = params['host']
    timeout = params['timeout']
    connect_timeout = params['connect_timeout']
    delay = params['delay']
    port = params['port']
    state = params['state']
    path = params['path']
    search_regex = params['search_regex']
    if (search_regex is not None):
        compiled_search_re = re.compile(search_regex, re.MULTILINE)
    else:
        compiled_search_re = None
    if (port and path):
        module.fail_json(msg='port and path parameter can not both be passed to wait_for')
    if (path and (state == 'stopped')):
        module.fail_json(msg='state=stopped should only be used for checking a port in the wait_for module')
    if (path and (state == 'drained')):
        module.fail_json(msg='state=drained should only be used for checking a port in the wait_for module')
    if ((params['exclude_hosts'] is not None) and (state != 'drained')):
        module.fail_json(msg='exclude_hosts should only be with state=drained')
    for _connection_state in params['active_connection_states']:
        try:
            get_connection_state_id(_connection_state)
        except:
            module.fail_json(msg=(('unknown active_connection_state (' + _connection_state) + ') defined'))
    start = datetime.datetime.now()
    if delay:
        time.sleep(delay)
    if ((not port) and (not path) and (state != 'drained')):
        time.sleep(timeout)
    elif (state in ['stopped', 'absent']):
        end = (start + datetime.timedelta(seconds=timeout))
        while (datetime.datetime.now() < end):
            if path:
                try:
                    f = open(path)
                    f.close()
                except IOError:
                    break
            elif port:
                try:
                    s = _create_connection(host, port, connect_timeout)
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                except:
                    break
            time.sleep(params['sleep'])
        else:
            elapsed = (datetime.datetime.now() - start)
            if port:
                module.fail_json(msg=('Timeout when waiting for %s:%s to stop.' % (host, port)), elapsed=elapsed.seconds)
            elif path:
                module.fail_json(msg=('Timeout when waiting for %s to be absent.' % path), elapsed=elapsed.seconds)
    elif (state in ['started', 'present']):
        end = (start + datetime.timedelta(seconds=timeout))
        while (datetime.datetime.now() < end):
            if path:
                try:
                    os.stat(path)
                except OSError:
                    e = get_exception()
                    if (e.errno != 2):
                        elapsed = (datetime.datetime.now() - start)
                        module.fail_json(msg=('Failed to stat %s, %s' % (path, e.strerror)), elapsed=elapsed.seconds)
                else:
                    if (not compiled_search_re):
                        break
                    try:
                        f = open(path)
                        try:
                            if re.search(compiled_search_re, f.read()):
                                break
                        finally:
                            f.close()
                    except IOError:
                        pass
            elif port:
                alt_connect_timeout = math.ceil(_timedelta_total_seconds((end - datetime.datetime.now())))
                try:
                    s = _create_connection(host, port, min(connect_timeout, alt_connect_timeout))
                except:
                    pass
                else:
                    if compiled_search_re:
                        data = ''
                        matched = False
                        while (datetime.datetime.now() < end):
                            max_timeout = math.ceil(_timedelta_total_seconds((end - datetime.datetime.now())))
                            (readable, w, e) = select.select([s], [], [], max_timeout)
                            if (not readable):
                                continue
                            response = s.recv(1024)
                            if (not response):
                                break
                            data += to_native(response, errors='surrogate_or_strict')
                            if re.search(compiled_search_re, data):
                                matched = True
                                break
                        s.shutdown(socket.SHUT_RDWR)
                        s.close()
                        if matched:
                            break
                    else:
                        s.shutdown(socket.SHUT_RDWR)
                        s.close()
                        break
            time.sleep(params['sleep'])
        else:
            elapsed = (datetime.datetime.now() - start)
            if port:
                if search_regex:
                    module.fail_json(msg=('Timeout when waiting for search string %s in %s:%s' % (search_regex, host, port)), elapsed=elapsed.seconds)
                else:
                    module.fail_json(msg=('Timeout when waiting for %s:%s' % (host, port)), elapsed=elapsed.seconds)
            elif path:
                if search_regex:
                    module.fail_json(msg=('Timeout when waiting for search string %s in %s' % (search_regex, path)), elapsed=elapsed.seconds)
                else:
                    module.fail_json(msg=('Timeout when waiting for file %s' % path), elapsed=elapsed.seconds)
    elif (state == 'drained'):
        end = (start + datetime.timedelta(seconds=timeout))
        tcpconns = TCPConnectionInfo(module)
        while (datetime.datetime.now() < end):
            try:
                if (tcpconns.get_active_connections_count() == 0):
                    break
            except IOError:
                pass
            time.sleep(params['sleep'])
        else:
            elapsed = (datetime.datetime.now() - start)
            module.fail_json(msg=('Timeout when waiting for %s:%s to drain' % (host, port)), elapsed=elapsed.seconds)
    elapsed = (datetime.datetime.now() - start)
    module.exit_json(state=state, port=port, search_regex=search_regex, path=path, elapsed=elapsed.seconds)
