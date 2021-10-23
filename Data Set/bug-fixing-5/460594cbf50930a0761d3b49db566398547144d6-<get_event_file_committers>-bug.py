def get_event_file_committers(project, event, frame_limit=25):
    Event.objects.bind_nodes([event], 'data')
    group = Group.objects.get(id=event.group_id)
    first_release_version = group.get_first_release()
    if (not first_release_version):
        raise Release.DoesNotExist
    releases = get_previous_releases(project, first_release_version)
    if (not releases):
        raise Release.DoesNotExist
    commits = _get_commits(releases)
    if (not commits):
        raise Commit.DoesNotExist
    frames = _get_frame_paths(event)
    app_frames = [frame for frame in frames if frame['in_app']][(- frame_limit):]
    if (not app_frames):
        app_frames = [frame for frame in frames][(- frame_limit):]
    if (event.platform == 'java'):
        for frame in frames:
            if (('/' not in frame.get('filename')) and frame.get('module')):
                frame['filename'] = ((frame['module'].replace('.', '/') + '/') + frame['filename'])
    path_set = {f for f in ((frame.get('filename') or frame.get('abs_path')) for frame in app_frames) if f}
    file_changes = []
    if path_set:
        file_changes = _get_commit_file_changes(commits, path_set)
    commit_path_matches = {path: _match_commits_path(file_changes, path) for path in path_set}
    annotated_frames = [{
        'frame': frame,
        'commits': (commit_path_matches.get((frame.get('filename') or frame.get('abs_path'))) or []),
    } for frame in app_frames]
    relevant_commits = list({match for match in commit_path_matches for match in commit_path_matches[match]})
    committers = _get_committers(annotated_frames, relevant_commits)
    metrics.incr('feature.owners.has-committers', instance=('hit' if committers else 'miss'), skip_internal=False)
    return committers