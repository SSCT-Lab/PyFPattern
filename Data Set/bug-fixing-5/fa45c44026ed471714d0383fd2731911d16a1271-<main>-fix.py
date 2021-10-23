def main():
    args = parse_args()
    try:
        sys.stdout = StringIO()
        config_files = (cloud_config.CONFIG_FILES + CONFIG_FILES)
        sdk.enable_logging(debug=args.debug)
        inventory_args = dict(refresh=args.refresh, config_files=config_files, private=args.private, cloud=args.cloud)
        if hasattr(sdk_inventory.OpenStackInventory, 'extra_config'):
            inventory_args.update(dict(config_key='ansible', config_defaults={
                'use_hostnames': False,
                'expand_hostvars': True,
                'fail_on_errors': True,
            }))
        inventory = sdk_inventory.OpenStackInventory(**inventory_args)
        sys.stdout = sys.__stdout__
        if args.list:
            output = get_host_groups(inventory, refresh=args.refresh, cloud=args.cloud)
        elif args.host:
            output = to_json(inventory.get_host(args.host))
        print(output)
    except sdk.exceptions.OpenStackCloudException as e:
        sys.stderr.write(('%s\n' % e.message))
        sys.exit(1)
    sys.exit(0)