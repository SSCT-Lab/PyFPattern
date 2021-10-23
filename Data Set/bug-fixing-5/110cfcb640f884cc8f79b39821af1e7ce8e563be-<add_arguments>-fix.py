def add_arguments(self, parser):
    parser.add_argument('emails', metavar='<emails>', type=str, nargs='*', help='email address to spelunk')
    parser.add_argument('--all', action='store_true', dest='all', default=False, help='fix all users in specified realm')
    self.add_realm_args(parser)