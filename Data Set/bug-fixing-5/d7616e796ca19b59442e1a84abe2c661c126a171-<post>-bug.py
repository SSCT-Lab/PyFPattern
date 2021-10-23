def post(self, request):
    changesets = request.relay_request_data.get('changesets')
    if changesets:
        change_set.execute_changesets(request.relay, changesets)
    queries = request.relay_request_data.get('queries')
    if queries:
        query_response = query.execute_queries(request.relay, queries)
    else:
        query_response = {
            
        }
    return Response({
        'queryResults': query_response,
    }, status=200)