def code_snippet(snippet):
    result = '```python\n'
    result += (snippet.encode('unicode_escape').decode('utf8') + '\n')
    result += '```\n'
    return result