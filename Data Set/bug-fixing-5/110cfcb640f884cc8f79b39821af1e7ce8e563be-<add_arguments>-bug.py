def add_arguments(self, parser):
    parser.add_argument('email', metavar='<email>', type=str, help='email address to spelunk')
    self.add_realm_args(parser)