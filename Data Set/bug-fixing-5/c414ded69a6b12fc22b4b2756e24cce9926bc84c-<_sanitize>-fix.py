def _sanitize(self, resp, obj=None):
    cleaned = []
    command = (obj.get('command') if obj else None)
    for line in resp.splitlines():
        if ((command and line.startswith(command.strip())) or self._find_prompt(line)):
            continue
        cleaned.append(line)
    return str('\n'.join(cleaned)).strip()