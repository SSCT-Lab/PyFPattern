def _sanitize(self, resp, obj=None):
    'Removes elements from the response before returning to the caller'
    cleaned = []
    command = (obj.get('command') if obj else None)
    for line in resp.splitlines():
        if ((command and line.startswith(command.strip())) or self._find_prompt(line)):
            continue
        cleaned.append(line)
    return str('\n'.join(cleaned)).strip()