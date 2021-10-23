def get(self, _, project, event_id):
    '\n        Retrieve Committer information for an event\n        ```````````````````````````````````````````\n\n        Return commiters on an individual event, plus a per-frame breakdown.\n\n        :pparam string project_slug: the slug of the project the event\n                                     belongs to.\n        :pparam string event_id: the hexadecimal ID of the event to\n                                 retrieve (as reported by the raven client).\n        :auth: required\n        '
    try:
        event = Event.objects.get(id=event_id, project_id=project.id)
    except Event.DoesNotExist:
        return Response({
            'detail': 'Event not found',
        }, status=404)
    Event.objects.bind_nodes([event], 'data')
    group = Group.objects.get(id=event.group_id)
    first_release_version = group.get_first_release()
    if (not first_release_version):
        return Response({
            'detail': 'Release not found',
        }, status=404)
    releases = Release.get_closest_releases(project, first_release_version)
    if (not releases):
        return Response({
            'detail': 'Release not found',
        }, status=404)
    commits = self._get_commits(releases)
    if (not commits):
        return Response({
            'detail': 'No Commits found for Release',
        }, status=404)
    frames = self._get_frame_paths(event)
    frame_limit = 15
    app_frames = [frame for frame in frames if frame['in_app']][:frame_limit]
    path_set = {frame['abs_path'] for frame in app_frames}
    file_changes = []
    if path_set:
        file_changes = self._get_commit_file_changes(commits, path_set)
    commit_path_matches = {path: self._match_commits_path(file_changes, path) for path in path_set}
    annotated_frames = [{
        'frame': frame,
        'commits': commit_path_matches[frame['abs_path']],
    } for frame in app_frames]
    relevant_commits = list({commit for match in commit_path_matches for commit in commit_path_matches[match]})
    committers = self._get_committers(annotated_frames, relevant_commits)
    serialized_annotated_frames = [{
        'frame': frame['frame'],
        'commits': serialize(frame['commits']),
    } for frame in annotated_frames]
    data = {
        'committers': committers,
        'annotatedFrames': serialized_annotated_frames,
    }
    return Response(data)