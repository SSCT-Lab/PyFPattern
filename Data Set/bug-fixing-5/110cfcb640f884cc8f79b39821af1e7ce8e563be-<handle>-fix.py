def handle(self, *args, **options):
    realm = self.get_realm(options)
    if options['all']:
        if (realm is None):
            print('You must specify a realm if you choose the --all option.')
            sys.exit(1)
        self.fix_all_users(realm)
        return
    self.fix_emails(realm, options['emails'])