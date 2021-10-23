

def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)
