def git_commit():
    try:
        cmd = ['git', 'rev-parse', 'HEAD']
        git_commit = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].strip()
    except:
        git_commit = 'Unknown'
    git_commit = git_commit.decode()
    return str(git_commit)