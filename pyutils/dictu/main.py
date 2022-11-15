def nested_get(data: dict, keys: list, default=None):
    """
    Get data from nested dictionary. Example:
    >>> x = {'a': {'b': 1, 'd': {'e': 3}, 'f': [{'g': 4}]}, 'c': 2}
    >>> nested_get(x, ['a', 'f', 0, 'g'])
    >>> nested_get(x, "a.f.0.g")
    """
    try:
        result = data
        if isinstance(keys, int):
            keys = [keys]
        elif isinstance(keys, str):
            keys = keys.split(".")
        if not isinstance(keys, (list, tuple)):
            # print("Warning - Invalid key: %s" % (keys))
            return default
        for key in keys:
            if isinstance(result, list):
                if isinstance(key, int):
                    pass
                elif isinstance(key, str) and key.isnumeric():
                    key = int(key)
                else:
                    # print("Warning - Invalid key: %s" % (key))
                    return default
            result = result[key]
        return result
    except (IndexError, KeyError, TypeError):
        return default


def nested_set(data: dict, keys: list, val):
    """
    Set data from nested dictionary. Example:
    >>> x = {}
    >>> nested_get(x, ['a', 'f', 0, 'g'], 1)
    >>> nested_get(x, "a.f.0.g")
    """
    if isinstance(keys, int):
        keys = [keys]
    elif isinstance(keys, str):
        keys = keys.split(".")
    try:
        for i, key in enumerate(keys):
            if i == len(keys) - 1:
                data[key] = val
                return True
            if key not in data:
                data[key] = {}
            data = data[key]
    except TypeError:
        pass
    return False


def nested_find_key(data: dict, target_key: str):
    stack = [data]
    while stack:
        data = stack.pop()
        try:
            items = data.items()
        except AttributeError:
            continue
        for key, value in items:
            if key == target_key:
                yield value
            else:
                stack.append(value)


def stringify(obj):
    if isinstance(obj, (str, int, float)):
        return str(obj)
    if isinstance(obj, list):
        return ", ".join(map(stringify, obj))
    if isinstance(obj, dict):
        values = []
        for key, val in obj.items():
            values.append("%s: %s" % (key, stringify(val)))
        return "{ "  + ", ".join(values) + " }"
    return ""