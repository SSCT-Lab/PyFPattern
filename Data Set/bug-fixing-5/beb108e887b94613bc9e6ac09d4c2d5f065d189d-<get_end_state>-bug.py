def get_end_state(self):
    ' Get end state '
    self.check_acl_args()
    self.end_state['acl_info'] = self.cur_acl_cfg['acl_info']
    self.check_advance_rule_args()
    self.end_state['adv_rule_info'] = self.cur_advance_rule_cfg['adv_rule_info']