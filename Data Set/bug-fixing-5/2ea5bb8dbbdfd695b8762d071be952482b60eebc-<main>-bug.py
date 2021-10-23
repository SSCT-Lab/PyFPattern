def main():
    module = AnsibleModule(argument_spec=dict(hwclock=dict(default=None, choices=['UTC', 'local'], aliases=['rtc']), name=dict(default=None)), required_one_of=['hwclock', 'name'], supports_check_mode=True)
    tz = Timezone(module)
    tz.check(phase='before')
    if module.check_mode:
        diff = tz.diff('before', 'planned')
        diff['after'] = diff.pop('planned')
    else:
        tz.change()
        tz.check(phase='after')
        (after, planned) = tz.diff('after', 'planned').values()
        if (after != planned):
            tz.abort('still not desired state, though changes have made')
        diff = tz.diff('before', 'after')
    changed = (diff['before'] != diff['after'])
    if (len(tz.msg) > 0):
        module.exit_json(changed=changed, diff=diff, msg='\n'.join(tz.msg))
    else:
        module.exit_json(changed=changed, diff=diff)