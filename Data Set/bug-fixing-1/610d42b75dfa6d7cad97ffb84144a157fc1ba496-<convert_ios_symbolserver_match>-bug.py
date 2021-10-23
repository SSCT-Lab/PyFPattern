

def convert_ios_symbolserver_match(instruction_addr, symbolserver_match):
    if (not symbolserver_match):
        return []
    symbol = symbolserver_match['symbol']
    if (symbol[:1] == '_'):
        symbol = symbol[1:]
    line_info = LineInfo(sym_addr=parse_addr(symbolserver_match['addr']), instr_addr=parse_addr(instruction_addr), line=None, lang=None, symbol=symbol)
    function = line_info.function_name
    package = symbolserver_match['object_name']
    return {
        'sym_addr': ('0x%x' % (line_info.sym_addr,)),
        'instruction_addr': ('0x%x' % (line_info.instr_addr,)),
        'function': function,
        'symbol': (symbol if (function != symbol) else None),
        'filename': trim(line_info.rel_path, 256),
        'abs_path': trim(line_info.abs_path, 256),
        'package': package,
    }
