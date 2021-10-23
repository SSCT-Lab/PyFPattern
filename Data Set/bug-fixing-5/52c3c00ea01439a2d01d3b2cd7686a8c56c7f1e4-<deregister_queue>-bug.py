def deregister_queue(client, queue_id):
    result = client.deregister(queue_id)
    fixture = FIXTURES['delete-queue']['successful_response']
    test_against_fixture(result, fixture)
    result = client.deregister(queue_id)
    fixture = FIXTURES['delete-queue']['bad_event_queue_id_error']
    test_against_fixture(result, fixture, check_if_equal=['code', 'result'], check_if_exists=['queue_id', 'msg'])