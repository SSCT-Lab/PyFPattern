def to_command(self, obj):
    if isinstance(obj, Command):
        cmdobj = dict()
        cmdobj['command'] = obj.command
        cmdobj['response'] = obj.response
        cmdobj['prompt'] = [p.pattern for p in to_list(obj.prompt)]
        return cmdobj
    elif (not isinstance(obj, dict)):
        transform = ComplexDict(dict(command=dict(key=True), prompt=dict(), response=dict(), sendonly=dict(default=False)))
        return transform(obj)
    else:
        return obj