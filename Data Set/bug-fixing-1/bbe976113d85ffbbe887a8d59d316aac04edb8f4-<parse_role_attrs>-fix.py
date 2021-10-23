

def parse_role_attrs(cursor, role_attr_flags):
    '\n    Parse role attributes string for user creation.\n    Format:\n\n        attributes[,attributes,...]\n\n    Where:\n\n        attributes := CREATEDB,CREATEROLE,NOSUPERUSER,...\n        [ "[NO]SUPERUSER","[NO]CREATEROLE", "[NO]CREATEDB",\n                            "[NO]INHERIT", "[NO]LOGIN", "[NO]REPLICATION",\n                            "[NO]BYPASSRLS" ]\n\n    Note: "[NO]BYPASSRLS" role attribute introduced in 9.5\n    Note: "[NO]CREATEUSER" role attribute is deprecated.\n\n    '
    flags = frozenset((role.upper() for role in role_attr_flags.split(',') if role))
    valid_flags = frozenset(itertools.chain(FLAGS, get_valid_flags_by_version(cursor)))
    valid_flags = frozenset(itertools.chain(valid_flags, (('NO%s' % flag) for flag in valid_flags)))
    if (not flags.issubset(valid_flags)):
        raise InvalidFlagsError(('Invalid role_attr_flags specified: %s' % ' '.join(flags.difference(valid_flags))))
    return ' '.join(flags)
