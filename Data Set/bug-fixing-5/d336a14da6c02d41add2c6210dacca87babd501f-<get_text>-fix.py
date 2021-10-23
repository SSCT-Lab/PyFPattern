def get_text(self, ele, tag):
    try:
        return to_text(ele.find(tag).text).strip()
    except AttributeError:
        pass