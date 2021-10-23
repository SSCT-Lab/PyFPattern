def _parse_field(self, data_json, item_id, field_name, section_title=None):
    data = json.loads(data_json)
    if ('documentAttributes' in data['details']):
        document = self._run(['get', 'document', data['overview']['title']])
        return {
            'document': document[0].strip(),
        }
    elif (field_name in data['details']):
        return {
            field_name: data['details'][field_name],
        }
    else:
        if (section_title is None):
            for field_data in data['details'].get('fields', []):
                if (field_data.get('name').lower() == field_name.lower()):
                    return {
                        field_name: field_data.get('value', ''),
                    }
        for section_data in data['details'].get('sections', []):
            if ((section_title is not None) and (section_title.lower() != section_data['title'].lower())):
                continue
            for field_data in section_data.get('fields', []):
                if (field_data.get('t').lower() == field_name.lower()):
                    return {
                        field_name: field_data.get('v', ''),
                    }
    optional_section_title = ('' if (section_title is None) else (" in the section '%s'" % section_title))
    module.fail_json(msg=("Unable to find an item in 1Password named '%s' with the field '%s'%s." % (item_id, field_name, optional_section_title)))