def match_active_opt(option, line):
    option = re.escape(option)
    return re.match((' *%s( |\t)*=' % option), line)