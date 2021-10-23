def common_subscribe_to_streams(self, email, streams, extra_post_data={
    
}, invite_only=False, **kwargs):
    post_data = {
        'subscriptions': ujson.dumps([{
            'name': stream,
        } for stream in streams]),
        'invite_only': ujson.dumps(invite_only),
    }
    post_data.update(extra_post_data)
    kw = kwargs.copy()
    kw.update(self.api_auth(email))
    result = self.client_post('/api/v1/users/me/subscriptions', post_data, **kw)
    return result