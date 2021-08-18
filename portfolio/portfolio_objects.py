class DictObj:
    def get_dict(self, **kwargs):
        obj = {}
        for key, value in kwargs.items():
            obj[key] = value
        return obj