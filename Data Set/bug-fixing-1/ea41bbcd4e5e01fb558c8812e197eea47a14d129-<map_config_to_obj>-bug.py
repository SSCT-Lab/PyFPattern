

def map_config_to_obj(module):
    out = run_commands(module, ['show management api http-commands | json'])
    return {
        'http': out[0]['httpServer']['configured'],
        'http_port': out[0]['httpServer']['port'],
        'https': out[0]['httpsServer']['configured'],
        'https_port': out[0]['httpsServer']['port'],
        'local_http': out[0]['localHttpServer']['configured'],
        'local_http_port': out[0]['localHttpServer']['port'],
        'socket': out[0]['unixSocketServer']['configured'],
        'vrf': out[0]['vrf'],
        'state': parse_state(out),
    }
