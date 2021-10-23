def get_text(self, ele, tag):
    try:
        return str(ele.find(tag).text).strip()
    except AttributeError:
        pass