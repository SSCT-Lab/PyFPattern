

def _get_commit_file_changes(commits, path_name_set):
    path_query = reduce(operator.or_, (Q(filename__endswith=next(tokenize_path(path))) for path in path_name_set))
    commit_file_change_matches = CommitFileChange.objects.filter(path_query, commit__in=commits)
    return list(commit_file_change_matches)
