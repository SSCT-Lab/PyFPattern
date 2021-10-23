def get_end_state(self):
    'get end state info'
    rollback_info = self.get_rollback_dict()
    if (not rollback_info):
        self.end_state['RollBackInfos'] = None
    else:
        self.end_state['RollBackInfos'] = rollback_info['RollBackInfos']