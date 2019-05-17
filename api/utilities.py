import sys
import traceback
import simplejson as json

from collections import (
    namedtuple,
    OrderedDict,
)

from api import (
    logger,
)


def isnamedtuple(obj):
    """Heuristic check if an object is a namedtuple."""
    return isinstance(obj, tuple) \
           and hasattr(obj, "_fields") \
           and hasattr(obj, "_asdict") \
           and callable(obj._asdict)


def serialize(data):
    """Link tham khao
    http://robotfantastic.org/serializing-python-data-to-json-some-edge-cases.html
    """
    if data is None or isinstance(data, (bool, int, long, float, basestring)):
        return data
    if isinstance(data, list):
        return [serialize(val) for val in data]
    if isinstance(data, OrderedDict):
        return {"py/collections.OrderedDict":
                    [[serialize(k), serialize(v)] for k, v in data.iteritems()]}
    if isnamedtuple(data):
        return {"py/collections.namedtuple": {
            "type": type(data).__name__,
            "fields": list(data._fields),
            "values": [serialize(getattr(data, f)) for f in data._fields]}}
    if isinstance(data, dict):
        if all(isinstance(k, basestring) for k in data):
            return {k: serialize(v) for k, v in data.iteritems()}
        return {"py/dict": [[serialize(k), serialize(v)] for k, v in data.iteritems()]}
    if isinstance(data, tuple):
        return {"py/tuple": [serialize(val) for val in data]}
    if isinstance(data, set):
        return {"py/set": [serialize(val) for val in data]}
    raise TypeError("Type %s not data-serializable" % type(data))


def restore(dct):
    if "py/dict" in dct:
        return dict(dct["py/dict"])
    if "py/tuple" in dct:
        return tuple(dct["py/tuple"])
    if "py/set" in dct:
        return set(dct["py/set"])
    if "py/collections.namedtuple" in dct:
        data = dct["py/collections.namedtuple"]
        return namedtuple(data["type"], data["fields"])(*data["values"])
    if "py/collections.OrderedDict" in dct:
        return OrderedDict(dct["py/collections.OrderedDict"])
    return dct


def data_to_json(data):
    return json.dumps(serialize(data))


def json_to_data(s):
    return json.loads(s, object_hook=restore)


def log_exception(e):
    error = '"Line":"{line}", "Exception_class": "{exception_class}", "Exception_docstring": "{exception_docstring}", "Exception_message": "{exception_message}"'.format(
        exception_class=e.__class__,
        exception_docstring=e.__doc__,
        exception_message=e.message,
        line=extract_function_name())
    logger.error('{%s}' % error)


def extract_function_name():
    tb = sys.exc_info()[-1]
    stk = traceback.extract_tb(tb, 1)
    fname = stk[0][3]
    return fname


def format_msisdn(msisdn):
    """
    :param msisdn:
    :return:
    """
    msisdn = str(msisdn).replace('+', '').strip()
    if msisdn.startswith('84'):
        msisdn = str(msisdn).replace('84', '0', 1).strip()
    if not msisdn.startswith('0'):
        msisdn = '0%s' % msisdn
    return msisdn
