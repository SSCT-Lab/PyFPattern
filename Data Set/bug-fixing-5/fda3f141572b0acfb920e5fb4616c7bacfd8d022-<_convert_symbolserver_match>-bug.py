def _convert_symbolserver_match(self, instruction_addr, symbolserver_match, obj):
    'Symbolizes a frame with system symbols only.'
    if (symbolserver_match is None):
        return []
    symbol = symbolserver_match['symbol']
    if (symbol[:1] == '_'):
        symbol = symbol[1:]
    return [self._process_frame(LineInfo(sym_addr=parse_addr(symbolserver_match['addr']), instr_addr=parse_addr(instruction_addr), line=None, symbol=symbol), obj, package=symbolserver_match['object_name'])]