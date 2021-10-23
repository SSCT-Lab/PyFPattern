def days_hours_minutes_seconds(self, runtime):
    minutes = ((runtime.seconds // 60) % 60)
    r_seconds = (runtime.seconds - (minutes * 60))
    return (runtime.days, (runtime.seconds // 3600), minutes, r_seconds)