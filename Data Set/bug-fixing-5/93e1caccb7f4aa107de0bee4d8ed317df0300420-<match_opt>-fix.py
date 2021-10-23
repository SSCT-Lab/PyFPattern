def match_opt(option, line):
    option = re.escape(option)
    return (re.match(('( |\t)*%s( |\t)*=' % option), line) or re.match(('#( |\t)*%s( |\t)*=' % option), line) or re.match((';( |\t)*%s( |\t)*=' % option), line))