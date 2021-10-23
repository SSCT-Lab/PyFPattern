

def _convert_debug_meta_to_binary_image_row(self, debug_image):
    slide_value = parse_addr(debug_image['image_vmaddr'])
    image_addr = (parse_addr(debug_image['image_addr']) + slide_value)
    return ('%s - %s %s %s  <%s> %s' % (hex(image_addr), hex(((image_addr + debug_image['image_size']) - 1)), image_name(debug_image['name']), self.context['device']['arch'], (debug_image.get('id') or debug_image.get('uuid')).replace('-', '').lower(), debug_image['name']))
