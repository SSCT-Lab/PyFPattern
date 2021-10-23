

def test_offset_pagination(self):
    self.setup_project_and_rules()
    date_added = before_now(minutes=1)
    self.one_alert_rule = self.create_alert_rule(projects=self.projects, date_added=date_added.replace(tzinfo=pytz.UTC))
    self.two_alert_rule = self.create_alert_rule(projects=self.projects, date_added=date_added.replace(tzinfo=pytz.UTC))
    self.three_alert_rule = self.create_alert_rule(projects=self.projects)
    with self.feature('organizations:incidents'):
        request_data = {
            'limit': '2',
        }
        response = self.client.get(path=self.combined_rules_url, data=request_data, content_type='application/json')
    assert (response.status_code == 200)
    result = json.loads(response.content)
    assert (len(result) == 2)
    self.assert_alert_rule_serialized(self.three_alert_rule, result[0], skip_dates=True)
    self.assert_alert_rule_serialized(self.one_alert_rule, result[1], skip_dates=True)
    links = requests.utils.parse_header_links(response.get('link').rstrip('>').replace('>,<', ',<'))
    next_cursor = links[1]['cursor']
    assert (next_cursor.split(':')[1] == '1')
    with self.feature('organizations:incidents'):
        request_data = {
            'cursor': next_cursor,
            'limit': '2',
        }
        response = self.client.get(path=self.combined_rules_url, data=request_data, content_type='application/json')
    assert (response.status_code == 200)
    result = json.loads(response.content)
    assert (len(result) == 2)
    self.assert_alert_rule_serialized(self.two_alert_rule, result[0], skip_dates=True)
    self.assert_alert_rule_serialized(self.yet_another_alert_rule, result[1], skip_dates=True)
