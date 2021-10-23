

def main():
    parser = create_parser()
    args = parser.parse_args()
    if (not hasattr(args.func)):
        parser.error('too few arguments')
    args.func(args)
