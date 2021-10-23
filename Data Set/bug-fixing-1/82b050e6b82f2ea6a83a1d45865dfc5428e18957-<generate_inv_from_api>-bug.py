

def generate_inv_from_api(config):
    try:
        inventory['all'] = copy.deepcopy(EMPTY_GROUP)
        if config.has_option('auth', 'api_token'):
            auth_token = config.get('auth', 'api_token')
        auth_token = env_or_param('SCALEWAY_TOKEN', param=auth_token)
        if (auth_token is None):
            sys.stderr.write('ERROR: missing authentication token for Scaleway API')
            sys.exit(1)
        if config.has_option('compute', 'regions'):
            regions = config.get('compute', 'regions')
            if (regions == 'all'):
                regions = ScalewayAPI.REGIONS
            else:
                regions = map(str.strip, regions.split(','))
        else:
            regions = [env_or_param('SCALEWAY_REGION', fallback='par1')]
        for region in regions:
            api = ScalewayAPI(auth_token, region)
            for server in api.servers():
                hostname = server['hostname']
                if (config.has_option('defaults', 'public_ip_only') and config.getboolean('defaults', 'public_ip_only')):
                    ip = server['public_ip']['address']
                else:
                    ip = server['private_ip']
                for server_tag in server['tags']:
                    if (server_tag not in inventory):
                        inventory[server_tag] = copy.deepcopy(EMPTY_GROUP)
                    inventory[server_tag]['children'].append(hostname)
                if (region not in inventory):
                    inventory[region] = copy.deepcopy(EMPTY_GROUP)
                inventory[region]['children'].append(hostname)
                inventory['all']['children'].append(hostname)
                inventory[hostname] = []
                inventory[hostname].append(ip)
        return inventory
    except Exception:
        traceback.print_exc()
        return {
            'all': {
                'hosts': [],
            },
            '_meta': {
                'hostvars': {
                    
                },
            },
        }
