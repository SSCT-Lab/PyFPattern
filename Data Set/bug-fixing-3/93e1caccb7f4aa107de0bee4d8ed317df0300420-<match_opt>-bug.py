def match_opt(option, line):
    option = re.escape(option)
    return (re.match((' *%s( |\t)*=' % option), line) or re.match(('# *%s( |\t)*=' % option), line) or re.match(('; *%s( |\t)*=' % option), line))