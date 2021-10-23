

def get_team_info(self, access_token):
    payload = {
        'token': access_token,
    }
    session = http.build_session()
    resp = session.get('https://slack.com/api/team.info', data=payload)
    resp.raise_for_status()
    resp = resp.json()
    return resp['team']
