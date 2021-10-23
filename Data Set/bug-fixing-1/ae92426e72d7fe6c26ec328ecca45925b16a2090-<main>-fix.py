

def main():
    module = AnsibleModule(argument_spec=dict(host=dict(type='str', default='127.0.0.1'), timeout=dict(type='int', default=300), connect_timeout=dict(type='int', default=5), delay=dict(type='int', default=0), port=dict(type='int'), active_connection_states=dict(type='list', default=['ESTABLISHED', 'FIN_WAIT1', 'FIN_WAIT2', 'SYN_RECV', 'SYN_SENT', 'TIME_WAIT']), path=dict(type='path'), search_regex=dict(type='str'), state=dict(type='str', default='started', choices=['absent', 'drained', 'present', 'started', 'stopped']), exclude_hosts=dict(type='list'), sleep=dict(type='int', default=1), msg=dict(type='str')))
    host = module.params['host']
    timeout = module.params['timeout']
    connect_timeout = module.params['connect_timeout']
    delay = module.params['delay']
    port = module.params['port']
    state = module.params['state']
    path = module.params['path']
    search_regex = module.params['search_regex']
    msg = module.params['msg']
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
    if ((module.params['exclude_hosts'] is not None) and (state != 'drained')):
        module.fail_json(msg='exclude_hosts should only be with state=drained')
    for _connection_state in module.params['active_connection_states']:
        try:
            get_connection_state_id(_connection_state)
        except:
            module.fail_json(msg=('unknown active_connection_state (%s) defined' % _connection_state))
    start = datetime.datetime.utcnow()
    if delay:
        time.sleep(delay)
    if ((not port) and (not path) and (state != 'drained')):
        time.sleep(timeout)
    elif (state in ['absent', 'stopped']):
        end = (start + datetime.timedelta(seconds=timeout))
        while (datetime.datetime.utcnow() < end):
            if path:
                try:
                    if (not os.access(path, os.F_OK)):
                        break
                except IOError:
                    break
            elif port:
                try:
                    s = _create_connection(host, port, connect_timeout)
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                except:
                    break
            time.sleep(module.params['sleep'])
        else:
            elapsed = (datetime.datetime.utcnow() - start)
            if port:
                module.fail_json(msg=(msg or ('Timeout when waiting for %s:%s to stop.' % (host, port))), elapsed=elapsed.seconds)
            elif path:
                module.fail_json(msg=(msg or ('Timeout when waiting for %s to be absent.' % path)), elapsed=elapsed.seconds)
    elif (state in ['started', 'present']):
        end = (start + datetime.timedelta(seconds=timeout))
        while (datetime.datetime.utcnow() < end):
            if path:
                try:
                    os.stat(path)
                except OSError as e:
                    if (e.errno != 2):
                        elapsed = (datetime.datetime.utcnow() - start)
                        module.fail_json(msg=(msg or ('Failed to stat %s, %s' % (path, e.strerror))), elapsed=elapsed.seconds)
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
                alt_connect_timeout = math.ceil(_timedelta_total_seconds((end - datetime.datetime.utcnow())))
                try:
                    s = _create_connection(host, port, min(connect_timeout, alt_connect_timeout))
                except:
                    pass
                else:
                    if compiled_search_re:
                        data = ''
                        matched = False
                        while (datetime.datetime.utcnow() < end):
                            max_timeout = math.ceil(_timedelta_total_seconds((end - datetime.datetime.utcnow())))
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
                        try:
                            s.shutdown(socket.SHUT_RDWR)
                        except socket.error as e:
                            if (e.errno != errno.ENOTCONN):
                                raise
                        else:
                            s.close()
                        if matched:
                            break
                    else:
                        try:
                            s.shutdown(socket.SHUT_RDWR)
                        except socket.error as e:
                            if (e.errno != errno.ENOTCONN):
                                raise
                        else:
                            s.close()
                        break
            time.sleep(module.params['sleep'])
        else:
            elapsed = (datetime.datetime.utcnow() - start)
            if port:
                if search_regex:
                    module.fail_json(msg=(msg or ('Timeout when waiting for search string %s in %s:%s' % (search_regex, host, port))), elapsed=elapsed.seconds)
                else:
                    module.fail_json(msg=(msg or ('Timeout when waiting for %s:%s' % (host, port))), elapsed=elapsed.seconds)
            elif path:
                if search_regex:
                    module.fail_json(msg=(msg or ('Timeout when waiting for search string %s in %s' % (search_regex, path))), elapsed=elapsed.seconds)
                else:
                    module.fail_json(msg=(msg or ('Timeout when waiting for file %s' % path)), elapsed=elapsed.seconds)
    elif (state == 'drained'):
        end = (start + datetime.timedelta(seconds=timeout))
        tcpconns = TCPConnectionInfo(module)
        while (datetime.datetime.utcnow() < end):
            try:
                if (tcpconns.get_active_connections_count() == 0):
                    break
            except IOError:
                pass
            time.sleep(module.params['sleep'])
        else:
            elapsed = (datetime.datetime.utcnow() - start)
            module.fail_json(msg=(msg or ('Timeout when waiting for %s:%s to drain' % (host, port))), elapsed=elapsed.seconds)
    elapsed = (datetime.datetime.utcnow() - start)
    module.exit_json(state=state, port=port, search_regex=search_regex, path=path, elapsed=elapsed.seconds)
