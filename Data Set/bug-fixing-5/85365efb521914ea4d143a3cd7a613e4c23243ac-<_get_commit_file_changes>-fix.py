def _get_commit_file_changes(commits, path_name_set):
    filenames = {next(tokenize_path(path), None) for path in path_name_set}
    filenames = {path for path in filenames if (path is not None)}
    if (not len(filenames)):
        return []
    path_query = reduce(operator.or_, (Q(filename__endswith=path) for path in filenames))
    commit_file_change_matches = CommitFileChange.objects.filter(path_query, commit__in=commits)
    return list(commit_file_change_matches)