def _convert_frame_to_apple_string(self, frame, next=None, number=0):
    if (frame.get('instruction_addr') is None):
        return None
    slide_value = self._get_slide_value(frame.get('image_addr'))
    instruction_addr = (slide_value + parse_addr(frame.get('instruction_addr')))
    image_addr = (slide_value + parse_addr(frame.get('image_addr')))
    offset = ''
    if ((frame.get('image_addr') is not None) and ((not self.symbolicated) or ((frame.get('function') or NATIVE_UNKNOWN_STRING) == NATIVE_UNKNOWN_STRING))):
        offset = (' + %s' % ((instruction_addr - slide_value) - parse_addr(frame.get('symbol_addr'))))
    symbol = hex(image_addr)
    if self.symbolicated:
        file = ''
        if (frame.get('filename') and frame.get('lineno')):
            file = (' (%s:%s)' % (posixpath.basename((frame.get('filename') or NATIVE_UNKNOWN_STRING)), frame['lineno']))
        symbol = ('%s%s' % ((frame.get('function') or NATIVE_UNKNOWN_STRING), file))
        if (next and (parse_addr(frame['instruction_addr']) == parse_addr(next['instruction_addr']))):
            symbol = ('[inlined] ' + symbol)
    return ('%s%s%s%s%s' % (str(number).ljust(4, ' '), image_name((frame.get('package') or NATIVE_UNKNOWN_STRING)).ljust(32, ' '), hex(instruction_addr).ljust(20, ' '), symbol, offset))