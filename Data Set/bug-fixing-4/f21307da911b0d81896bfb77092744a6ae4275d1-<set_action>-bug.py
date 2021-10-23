def set_action(self):
    super(GalaxyCLI, self).set_action()
    if (self.action == 'delete'):
        self.parser.set_usage('usage: %prog delete [options] github_user github_repo')
    elif (self.action == 'import'):
        self.parser.set_usage('usage: %prog import [options] github_user github_repo')
        self.parser.add_option('--no-wait', dest='wait', action='store_false', default=True, help="Don't wait for import results.")
        self.parser.add_option('--branch', dest='reference', help="The name of a branch to import. Defaults to the repository's default branch (usually master)")
        self.parser.add_option('--role-name', dest='role_name', help='The name the role should have, if different than the repo name')
        self.parser.add_option('--status', dest='check_status', action='store_true', default=False, help='Check the status of the most recent import request for given github_user/github_repo.')
    elif (self.action == 'info'):
        self.parser.set_usage('usage: %prog info [options] role_name[,version]')
    elif (self.action == 'init'):
        self.parser.set_usage('usage: %prog init [options] role_name')
        self.parser.add_option('--init-path', dest='init_path', default='./', help='The path in which the skeleton role will be created. The default is the current working directory.')
        self.parser.add_option('--type', dest='role_type', action='store', default='default', help="Initialize using an alternate role type. Valid types include: 'container', 'apb' and 'network'.")
        self.parser.add_option('--role-skeleton', dest='role_skeleton', default=C.GALAXY_ROLE_SKELETON, help='The path to a role skeleton that the new role should be based upon.')
    elif (self.action == 'install'):
        self.parser.set_usage('usage: %prog install [options] [-r FILE | role_name(s)[,version] | scm+role_repo_url[,version] | tar_file(s)]')
        self.parser.add_option('-i', '--ignore-errors', dest='ignore_errors', action='store_true', default=False, help='Ignore errors and continue with the next specified role.')
        self.parser.add_option('-n', '--no-deps', dest='no_deps', action='store_true', default=False, help="Don't download roles listed as dependencies")
        self.parser.add_option('-r', '--role-file', dest='role_file', help='A file containing a list of roles to be imported')
        self.parser.add_option('-g', '--keep-scm-meta', dest='keep_scm_meta', action='store_true', default=False, help='Use tar instead of the scm archive option when packaging the role')
    elif (self.action == 'remove'):
        self.parser.set_usage('usage: %prog remove role1 role2 ...')
    elif (self.action == 'list'):
        self.parser.set_usage('usage: %prog list [role_name]')
    elif (self.action == 'login'):
        self.parser.set_usage('usage: %prog login [options]')
        self.parser.add_option('--github-token', dest='token', default=None, help='Identify with github token rather than username and password.')
    elif (self.action == 'search'):
        self.parser.set_usage('usage: %prog search [searchterm1 searchterm2] [--galaxy-tags galaxy_tag1,galaxy_tag2] [--platforms platform1,platform2] [--author username]')
        self.parser.add_option('--platforms', dest='platforms', help='list of OS platforms to filter by')
        self.parser.add_option('--galaxy-tags', dest='galaxy_tags', help='list of galaxy tags to filter by')
        self.parser.add_option('--author', dest='author', help='GitHub username')
    elif (self.action == 'setup'):
        self.parser.set_usage('usage: %prog setup [options] source github_user github_repo secret')
        self.parser.add_option('--remove', dest='remove_id', default=None, help='Remove the integration matching the provided ID value. Use --list to see ID values.')
        self.parser.add_option('--list', dest='setup_list', action='store_true', default=False, help='List all of your integrations.')
    if (self.action in ['init', 'info']):
        self.parser.add_option('--offline', dest='offline', default=False, action='store_true', help="Don't query the galaxy API when creating roles")
    if (self.action not in ('delete', 'import', 'init', 'login', 'setup')):
        self.parser.add_option('-p', '--roles-path', dest='roles_path', action='callback', callback=CLI.unfrack_paths, default=C.DEFAULT_ROLES_PATH, help='The path to the directory containing your roles. The default is the roles_path configured in your ansible.cfg file (/etc/ansible/roles if not configured)', type='str')
    if (self.action in ('init', 'install')):
        self.parser.add_option('-f', '--force', dest='force', action='store_true', default=False, help='Force overwriting an existing role')