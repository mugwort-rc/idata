import re


SLICE_RE = re.compile(r"^((?:\+|-)?\d+)?:((?:_1)?(?:\+|-)?\d+)?(?::((?:\+|-)?\d+)?)?$")


def is_slice(s):
    """
    >>> is_slice("")
    False
    >>> is_slice("0")
    False
    >>> is_slice(":")
    True
    >>> is_slice("0:")
    True
    >>> is_slice(":1")
    True
    >>> is_slice("0:1")
    True
    >>> is_slice("::")
    True
    >>> is_slice("0::")
    True
    >>> is_slice(":1:")
    True
    >>> is_slice("::2")
    True
    >>> is_slice("0:1:")
    True
    >>> is_slice(":1:2")
    True
    >>> is_slice("0::2")
    True
    >>> is_slice("0:1:2")
    True
    >>> is_slice("+0:+1:+2")
    True
    >>> is_slice("-0:-1:-2")
    True
    >>> is_slice("+0:_1+1:+2")
    True
    """
    return bool(SLICE_RE.match(s))


def to_slice(s):
    """
    >>> to_slice("0:1:2")
    slice(0, 1, 2)
    >>> to_slice("3:_1+7")
    slice(3, 10, None)
    """
    assert is_slice(s)
    m = SLICE_RE.match(s)
    start = m.group(1)
    end = m.group(2)
    step = m.group(3)
    if start is not None:
        start = int(start)
    if end is not None:
        if end.startswith("_1"):
            end = start + int(end[2:])
        else:
            end = int(end)
    if step is not None:
        step = int(step)
    return slice(start, end, step)


def is_expr(s):
    return s.startswith("$")


def is_config_expr(s):
    """
    >>> is_config_expr("$config@hoge@fuga")
    True
    >>> is_config_expr("$ctx.hoge")
    False
    """
    return s.startswith("$config@")


def evaluate_value(args, exprs):
    """
    >>> evaluate_value(dict(a=42), ["a"])
    42
    >>> evaluate_value(dict(a=dict(n=123)), ["a", "n"])
    123
    >>> evaluate_value([{"a": x} for x in range(3)], ["[:]", "a"])
    [0, 1, 2]
    """
    value = None
    expr = exprs[0]
    exprs = exprs[1:]
    if isinstance(args, dict):
        m = re.match(r"^([^\[]+)(\[([^\]]+)\])?$", expr)
        value = args[m.group(1)]
        index = m.group(2)
        if index is not None:
            value = evaluate_value(value, [index])
    elif isinstance(args, list):
        m = re.match(r"^\[([^\]]+)\]$", expr)
        if m:
            index = m.group(1)
            if is_slice(index):
                s = to_slice(index)
                value = args[s]
            else:
                value = args[int(index)]
        else:
            tmp = []
            for item in args:
                tmp.append(evaluate_value(item, [expr]+exprs))
            return tmp
    if exprs:
        return evaluate_value(value, exprs)
    return value
