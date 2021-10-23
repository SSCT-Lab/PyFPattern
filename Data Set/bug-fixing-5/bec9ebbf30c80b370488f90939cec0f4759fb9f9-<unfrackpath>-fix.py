def unfrackpath(path, follow=True):
    "\n    Returns a path that is free of symlinks (if follow=True), environment variables, relative path traversals and symbols (~)\n\n    :arg path: A byte or text string representing a path to be canonicalized\n    :arg follow: A boolean to indicate of symlinks should be resolved or not\n    :raises UnicodeDecodeError: If the canonicalized version of the path\n        contains non-utf8 byte sequences.\n    :rtype: A text string (unicode on pyyhon2, str on python3).\n    :returns: An absolute path with symlinks, environment variables, and tilde\n        expanded.  Note that this does not check whether a path exists.\n\n    example::\n        '$HOME/../../var/mail' becomes '/var/spool/mail'\n    "
    if follow:
        final_path = os.path.normpath(os.path.realpath(os.path.expanduser(os.path.expandvars(to_bytes(path, errors='surrogate_or_strict')))))
    else:
        final_path = os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(to_bytes(path, errors='surrogate_or_strict')))))
    return to_text(final_path, errors='surrogate_or_strict')