UNDEFINED = object()


def js_to_string(val):
    if val is UNDEFINED:
        return "undefined"
    if val is None:
        return "null"
    if val is True:
        return "true"
    if val is False:
        return "false"
    if isinstance(val, float):
        if val != val:
            return "NaN"
        if val == float('inf'):
            return "Infinity"
        if val == float('-inf'):
            return "-Infinity"
        if val == int(val):
            return str(int(val))
        return str(val)
    if isinstance(val, int):
        return str(val)
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        return ",".join(js_to_string(item) for item in val)
    if isinstance(val, dict):
        return "[object Object]"
    if callable(val):
        return "function"
    return str(val)


def js_to_boolean(val):
    if val is UNDEFINED or val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        if val != val:  # NaN
            return False
        return val != 0
    if isinstance(val, str):
        return len(val) > 0
    return True
