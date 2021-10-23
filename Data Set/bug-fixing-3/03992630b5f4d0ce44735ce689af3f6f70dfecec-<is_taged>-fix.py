def is_taged():
    try:
        cmd = ['git', 'describe', '--exact-match', '--tags', 'HEAD', '2>/dev/null']
        git_tag = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd='@PADDLE_SOURCE_DIR@').communicate()[0].strip()
        git_tag = git_tag.decode()
    except:
        return False
    if (str(git_tag).replace('v', '') == '@PADDLE_VERSION@'):
        return True
    else:
        return False