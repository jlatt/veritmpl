try:
    import json
except ImportError:
    import simplejson as json

from veritmpl import runtime


class JSON(runtime.Literal):
    pass


class JSONFilter(object):
    def __init__(self, **kwargs):
        self.json_kwargs = kwargs

    def __call__(self, value, out):
        if isinstance(value, JSON):
            out.write(value)
        else:
            json.dump(value, out, **self.json_kwargs)
