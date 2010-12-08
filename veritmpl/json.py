try:
    import json
except ImportError:
    import simplejson as json

from veritmpl import runtime


class JSON(runtime.Literal):
    """JSON are unicode()s that are marked as containing JSON data."""
    pass


class JSONEncoder(object):
    def __init__(self, **kwargs):
        """Create a JSONEncoder. All arguments passed to this function are
        passed to json.dump() when values are interpolated.

        """
        self.json_kwargs = kwargs

    def encode(self, value, out):
        if isinstance(value, JSON):
            out.write(value)
        else:
            json.dump(value, out, **self.json_kwargs)


class JSONTemplate(runtime.Template):
    """JSONTemplate is a simple JSON template base for templates that do not
    need special arguments passed to the JSON encoder.

    """
    encode = JSONEncoder()
