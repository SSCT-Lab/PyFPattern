

def get_config_diff(module, running=None, candidate=None):
    conn = get_connection(module)
    if is_cliconf(module):
        try:
            response = conn.get('show commit changes diff')
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))
        return response
    elif is_netconf(module):
        if (running and candidate):
            running_data = running.split('\n', 1)[(- 1)].rsplit('\n', 1)[0]
            candidate_data = candidate.split('\n', 1)[(- 1)].rsplit('\n', 1)[0]
            if (running_data != candidate_data):
                d = Differ()
                diff = list(d.compare(running_data.splitlines(), candidate_data.splitlines()))
                return '\n'.join(diff).strip()
    return None
