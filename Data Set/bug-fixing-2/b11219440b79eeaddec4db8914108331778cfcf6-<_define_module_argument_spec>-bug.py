

@staticmethod
def _define_module_argument_spec():
    '\n        Define the argument spec for the ansible module\n        :return: argument spec dictionary\n        '
    argument_spec = dict(location=dict(required=True), source_account_alias=dict(required=True, default=None), destination_account_alias=dict(default=None), firewall_policy_id=dict(default=None), ports=dict(default=None, type='list'), source=dict(defualt=None, type='list'), destination=dict(defualt=None, type='list'), wait=dict(default=True), state=dict(default='present', choices=['present', 'absent']), enabled=dict(defualt=True, choices=[True, False]))
    return argument_spec
