def run_commands(self, commands):
    responses = list()
    for cmd in commands:
        meth = getattr(self, cmd.args.get('command_type'))
        responses.append(meth(str(cmd), output=cmd.output))
    for (index, cmd) in enumerate(commands):
        if (cmd.output == 'xml'):
            responses[index] = xml_to_json(responses[index])
        elif (cmd.args.get('command_type') == 'rpc'):
            responses[index] = str(responses[index].text).strip()
    return responses