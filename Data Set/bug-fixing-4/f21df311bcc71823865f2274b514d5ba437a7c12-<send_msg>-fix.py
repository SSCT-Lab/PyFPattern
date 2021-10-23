def send_msg(self, msg, msg_format='text', color='yellow', notify=False):
    'Method for sending a message to HipChat'
    params = {
        
    }
    params['room_id'] = self.room
    params['from'] = self.from_name[:15]
    params['message'] = msg
    params['message_format'] = msg_format
    params['color'] = color
    params['notify'] = int((self.allow_notify and notify))
    url = ('%s?auth_token=%s' % (self.msg_uri, self.token))
    try:
        response = open_url(url, data=urllib.urlencode(params))
        return response.read()
    except:
        self._display.warning('Could not submit message to hipchat')