

def main():
    args = parse_args()
    for config_file in CONFIG_FILES:
        if os.path.exists(config_file):
            break
    else:
        sys.stdout.write('unable to locate config file at /etc/ansible/infoblox.yaml\n')
        sys.exit((- 1))
    try:
        loader = DataLoader()
        config = loader.load_from_file(config_file)
        provider = (config.get('provider') or {
            
        })
        wapi = WapiInventory(provider)
    except Exception as exc:
        sys.stdout.write(to_text(exc))
        sys.exit((- 1))
    if args.host:
        host_filter = {
            'name': args.host,
        }
    else:
        host_filter = {
            
        }
    config_filters = config.get('filters')
    if (config_filters.get('view') is not None):
        host_filter['view'] = config_filters['view']
    if config_filters.get('extattrs'):
        extattrs = normalize_extattrs(config_filters['extattrs'])
    else:
        extattrs = {
            
        }
    hostvars = {
        
    }
    inventory = {
        '_meta': {
            'hostvars': hostvars,
        },
    }
    return_fields = ['name', 'view', 'extattrs', 'ipv4addrs']
    hosts = wapi.get_object('record:host', host_filter, extattrs=extattrs, return_fields=return_fields)
    if hosts:
        for item in hosts:
            view = item['view']
            name = item['name']
            if (view not in inventory):
                inventory[view] = {
                    'hosts': [],
                }
            inventory[view]['hosts'].append(name)
            hostvars[name] = {
                'view': view,
            }
            if item.get('extattrs'):
                for (key, value) in iteritems(flatten_extattrs(item['extattrs'])):
                    if key.startswith('ansible_'):
                        hostvars[name][key] = value
                    else:
                        if ('extattrs' not in hostvars):
                            hostvars[name]['extattrs'] = {
                                
                            }
                        hostvars[name]['extattrs'][key] = value
    sys.stdout.write(json.dumps(inventory, indent=4))
    sys.exit(0)
