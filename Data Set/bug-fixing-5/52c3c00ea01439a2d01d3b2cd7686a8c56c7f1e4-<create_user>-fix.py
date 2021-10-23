def create_user(client):
    request = {
        'email': 'newbie@zulip.com',
        'password': 'temp',
        'full_name': 'New User',
        'short_name': 'newbie',
    }
    result = client.create_user(request)
    fixture = FIXTURES['successful-response-empty']
    test_against_fixture(result, fixture)
    result = client.create_user(request)
    fixture = FIXTURES['email_already_used_error']
    test_against_fixture(result, fixture)