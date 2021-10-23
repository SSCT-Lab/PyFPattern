def create_user(client):
    request = {
        'email': 'newbie@zulip.com',
        'password': 'temp',
        'full_name': 'New User',
        'short_name': 'newbie',
    }
    result = client.create_user(request)
    fixture = FIXTURES['create-user']['successful_response']
    test_against_fixture(result, fixture)
    result = client.create_user(request)
    fixture = FIXTURES['create-user']['email_already_used_error']
    test_against_fixture(result, fixture)