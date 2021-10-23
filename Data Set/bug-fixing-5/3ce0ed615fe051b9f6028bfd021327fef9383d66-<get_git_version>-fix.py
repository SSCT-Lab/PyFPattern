def get_git_version(git_base_path, git_tag_override):
    "Get the git version from the repository.\n\n  This function runs `git describe ...` in the path given as `git_base_path`.\n  This will return a string of the form:\n  <base-tag>-<number of commits since tag>-<shortened sha hash>\n\n  For example, 'v0.10.0-1585-gbb717a6' means v0.10.0 was the last tag when\n  compiled. 1585 commits are after that commit tag, and we can get back to this\n  version by running `git checkout gbb717a6`.\n\n  Args:\n    git_base_path: where the .git directory is located\n    git_tag_override: Override the value for the git tag. This is useful for\n      releases where we want to build the release before the git tag is\n      created.\n  Returns:\n    A bytestring representing the git version\n  "
    unknown_label = b'unknown'
    try:
        val = bytes(subprocess.check_output(['git', str(('--git-dir=%s/.git' % git_base_path)), str(('--work-tree=' + git_base_path)), 'describe', '--long', '--tags']).strip())
        version_separator = b'-'
        if (git_tag_override and val):
            split_val = val.split(version_separator)
            if (len(split_val) < 3):
                raise Exception(("Expected git version in format 'TAG-COMMITS AFTER TAG-HASH' but got '%s'" % val))
            abbrev_commit = split_val[(- 1)]
            val = version_separator.join([as_bytes(git_tag_override), b'0', abbrev_commit])
        return (val if val else unknown_label)
    except (subprocess.CalledProcessError, OSError):
        return unknown_label