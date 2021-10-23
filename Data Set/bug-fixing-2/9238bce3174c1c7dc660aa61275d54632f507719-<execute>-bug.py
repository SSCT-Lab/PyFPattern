

def execute(self, context):
    '\n        Call the SparkSqlHook to run the provided sql query\n        '
    self.hook = SlackWebhookHook(self.http_conn_id, self.webhook_token, self.message, self.channel, self.username, self.icon_emoji, self.link_names, self.proxy)
    self.hook.execute()
