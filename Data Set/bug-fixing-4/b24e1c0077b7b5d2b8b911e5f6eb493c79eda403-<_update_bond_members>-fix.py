def _update_bond_members(self, key, want, have):
    commands = []
    want_members = (want.get(key) or [])
    have_members = (have.get(key) or [])
    members_diff = list_diff_have_only(want_members, have_members)
    if members_diff:
        for member in members_diff:
            commands.append(self._compute_command(member['member'], 'bond-group', have['name'], True, 'ethernet'))
    return commands