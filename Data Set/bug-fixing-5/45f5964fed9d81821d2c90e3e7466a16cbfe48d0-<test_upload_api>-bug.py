def test_upload_api(monkeypatch):

    class FakeConnection():

        def put_rest_api(self, *args, **kwargs):
            assert (kwargs['body'] == 'the-swagger-text-is-fake')
            return {
                'msg': 'success!',
            }

    def return_fake_connection(*args, **kwargs):
        return FakeConnection()
    monkeypatch.setattr(agw, 'boto3_conn', return_fake_connection)
    monkeypatch.setattr(agw.AnsibleModule, 'exit_json', fake_exit_json)
    set_module_args({
        'api_id': 'fred',
        'state': 'present',
        'swagger_text': 'the-swagger-text-is-fake',
        'region': 'mars-north-1',
    })
    with pytest.raises(SystemExit):
        agw.main()
    assert exit_return_dict['changed']