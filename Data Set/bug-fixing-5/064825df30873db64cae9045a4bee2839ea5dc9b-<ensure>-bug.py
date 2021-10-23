def ensure(self):
    'Manage statistics for a vCenter server'
    result = dict(changed=False, msg='')
    past_day_enabled = self.params['interval_past_day'].get('enabled', True)
    past_day_seconds = (self.params['interval_past_day'].get('interval_minutes', 5) * 60)
    past_day_save_for_seconds = (self.params['interval_past_day'].get('save_for_days', 1) * 86400)
    past_day_level = self.params['interval_past_day'].get('level', 1)
    past_week_enabled = self.params['interval_past_week'].get('enabled', True)
    past_week_seconds = (self.params['interval_past_week'].get('interval_minutes', 30) * 60)
    past_week_save_for_seconds = (self.params['interval_past_week'].get('save_for_weeks', 1) * 604800)
    past_week_level = self.params['interval_past_week'].get('level', 1)
    past_month_enabled = self.params['interval_past_month'].get('enabled', True)
    past_month_seconds = (self.params['interval_past_month'].get('interval_hours', 2) * 3600)
    past_month_save_for_seconds = (self.params['interval_past_month'].get('save_for_months', 1) * 2592000)
    past_month_level = self.params['interval_past_month'].get('level', 1)
    past_year_enabled = self.params['interval_past_year'].get('enabled', True)
    past_year_seconds = (self.params['interval_past_year'].get('interval_days', 1) * 86400)
    past_year_save_for_seconds = (self.params['interval_past_year'].get('save_for_years', 1) * 31536000)
    past_year_level = self.params['interval_past_year'].get('level', 1)
    if (past_year_level > past_month_level):
        self.module.fail_json(msg="The statistics level for past year can't be higher than past month!")
    if (past_month_level > past_week_level):
        self.module.fail_json(msg="The statistics level for past month can't be higher than past week!")
    if (past_week_level > past_day_level):
        self.module.fail_json(msg="The statistics level for past week can't be higher than past day!")
    if ((not past_day_enabled) and (past_week_enabled or past_month_enabled or past_year_enabled)):
        self.module.fail_json(msg='The intervals past week, month, and year need to be disabled as well!')
    if ((not past_week_enabled) and (past_month_enabled or past_year_enabled)):
        self.module.fail_json(msg='The intervals past month, and year need to be disabled as well!')
    if ((not past_month_enabled) and past_year_enabled):
        self.module.fail_json(msg='The interval past year need to be disabled as well!')
    if (past_year_enabled and ((not past_day_enabled) or (not past_week_enabled) or (not past_month_enabled))):
        self.module.fail_json(msg='The intervals past day, week, and month need to be enabled as well!')
    if (past_month_enabled and ((not past_day_enabled) or (not past_week_enabled))):
        self.module.fail_json(msg='The intervals past day, and week need to be enabled as well!')
    if (past_week_enabled and (not past_day_enabled)):
        self.module.fail_json(msg='The intervals past day need to be enabled as well!')
    changed = False
    changed_list = []
    result['past_day_enabled'] = past_day_enabled
    result['past_day_interval'] = int((past_day_seconds / 60))
    result['past_day_save_for'] = int((past_day_save_for_seconds / 86400))
    result['past_day_level'] = past_day_level
    result['past_week_enabled'] = past_week_enabled
    result['past_week_interval'] = int((past_week_seconds / 60))
    result['past_week_save_for'] = int((past_week_save_for_seconds / 604800))
    result['past_week_level'] = past_week_level
    result['past_month_enabled'] = past_month_enabled
    result['past_month_interval'] = int((past_month_seconds / 3600))
    result['past_month_save_for'] = int((past_month_save_for_seconds / 2592000))
    result['past_month_level'] = past_month_level
    result['past_year_enabled'] = past_year_enabled
    result['past_year_interval'] = int((past_year_seconds / 86400))
    result['past_year_save_for'] = int((past_year_save_for_seconds / 31536000))
    result['past_year_level'] = past_year_level
    change_statistics_list = []
    increase_level = decrease_level = False
    perf_manager = self.content.perfManager
    for historical_interval in perf_manager.historicalInterval:
        if ((historical_interval.name == 'Past day') and ((historical_interval.samplingPeriod != past_day_seconds) or (historical_interval.length != past_day_save_for_seconds) or (historical_interval.level != past_day_level) or (historical_interval.enabled != past_day_enabled))):
            changed = True
            changed_list.append('Past day interval')
            if (historical_interval.enabled != past_day_enabled):
                result['past_day_enabled_previous'] = historical_interval.enabled
            if (historical_interval.samplingPeriod != past_day_seconds):
                result['past_day_interval_previous'] = int((historical_interval.samplingPeriod / 60))
            if (historical_interval.length != past_day_save_for_seconds):
                result['past_day_save_for_previous'] = int((historical_interval.length / 86400))
            if (historical_interval.level != past_day_level):
                result['past_day_level_previous'] = historical_interval.level
                if (historical_interval.level < past_day_level):
                    increase_level = True
                elif (historical_interval.level > past_day_level):
                    decrease_level = True
            change_statistics_list.append(vim.HistoricalInterval(key=1, samplingPeriod=past_day_seconds, name='Past day', length=past_day_save_for_seconds, level=past_day_level, enabled=past_day_enabled))
        if ((historical_interval.name == 'Past week') and ((historical_interval.samplingPeriod != past_week_seconds) or (historical_interval.length != past_week_save_for_seconds) or (historical_interval.level != past_week_level) or (historical_interval.enabled != past_week_enabled))):
            changed = True
            changed_list.append('Past week interval')
            if (historical_interval.enabled != past_week_enabled):
                result['past_week_enabled_previous'] = historical_interval.enabled
            if (historical_interval.samplingPeriod != past_week_seconds):
                result['past_week_interval_previous'] = int((historical_interval.samplingPeriod / 60))
            if (historical_interval.length != past_week_save_for_seconds):
                result['past_week_save_for_previous'] = int((historical_interval.length / 604800))
            if (historical_interval.level != past_week_level):
                result['past_week_level_previous'] = historical_interval.level
                if (historical_interval.level < past_week_level):
                    increase_level = True
                elif (historical_interval.level > past_week_level):
                    decrease_level = True
            change_statistics_list.append(vim.HistoricalInterval(key=2, samplingPeriod=past_week_seconds, name='Past week', length=past_week_save_for_seconds, level=past_week_level, enabled=past_week_enabled))
        if ((historical_interval.name == 'Past month') and ((historical_interval.samplingPeriod != past_month_seconds) or (historical_interval.length != past_month_save_for_seconds) or (historical_interval.level != past_month_level) or (historical_interval.enabled != past_month_enabled))):
            changed = True
            changed_list.append('Past month interval')
            if (historical_interval.enabled != past_month_enabled):
                result['past_month_enabled_previous'] = historical_interval.enabled
            if (historical_interval.samplingPeriod != past_month_seconds):
                result['past_month_interval_previous'] = int((historical_interval.samplingPeriod / 3600))
            if (historical_interval.length != past_month_save_for_seconds):
                result['past_month_save_for_previous'] = int((historical_interval.length / 2592000))
            if (historical_interval.level != past_month_level):
                result['past_month_level_previous'] = historical_interval.level
                if (historical_interval.level < past_month_level):
                    increase_level = True
                elif (historical_interval.level > past_month_level):
                    decrease_level = True
            change_statistics_list.append(vim.HistoricalInterval(key=3, samplingPeriod=past_month_seconds, name='Past month', length=past_month_save_for_seconds, level=past_month_level, enabled=past_month_enabled))
        if ((historical_interval.name == 'Past year') and ((historical_interval.samplingPeriod != past_year_seconds) or (historical_interval.length != past_year_save_for_seconds) or (historical_interval.level != past_year_level) or (historical_interval.enabled != past_year_enabled))):
            changed = True
            changed_list.append('Past year interval')
            if (historical_interval.enabled != past_year_enabled):
                result['past_year_enabled_previous'] = historical_interval.enabled
            if (historical_interval.samplingPeriod != past_year_seconds):
                result['past_year_interval_previous'] = int((historical_interval.samplingPeriod / 86400))
            if (historical_interval.length != past_year_save_for_seconds):
                result['past_year_save_for_previous'] = int((historical_interval.length / 31536000))
            if (historical_interval.level != past_year_level):
                result['past_year_level_previous'] = historical_interval.level
                if (historical_interval.level < past_year_level):
                    increase_level = True
                elif (historical_interval.level > past_year_level):
                    decrease_level = True
            change_statistics_list.append(vim.HistoricalInterval(key=4, samplingPeriod=past_year_seconds, name='Past year', length=past_year_save_for_seconds, level=past_year_level, enabled=past_year_enabled))
    message = 'vCenter statistics already configured properly'
    if changed:
        if self.module.check_mode:
            changed_suffix = ' would be changed'
        else:
            changed_suffix = ' changed'
        if (len(changed_list) > 2):
            message = ((', '.join(changed_list[:(- 1)]) + ', and ') + str(changed_list[(- 1)]))
        elif (len(changed_list) == 2):
            message = ' and '.join(changed_list)
        elif (len(changed_list) == 1):
            message = changed_list[0]
        message += changed_suffix
        if (not self.module.check_mode):
            if increase_level:
                for statistic in change_statistics_list:
                    self.update_perf_interval(perf_manager, statistic)
            if decrease_level:
                for statistic in change_statistics_list[::(- 1)]:
                    self.update_perf_interval(perf_manager, statistic)
    result['changed'] = changed
    result['msg'] = message
    self.module.exit_json(**result)