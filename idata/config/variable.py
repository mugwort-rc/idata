import re


class VariableExpr:
    def __init__(self, ctx, expr):
        self.ctx = ctx
        self.expr = expr

    def is_variable(self):
        return "$" in self.expr

    def evaluate(self, record):
        tmp = ""
        index = 0
        for m in re.finditer(r"\$\{([^\}]+)\}", self.expr):
            tmp += self.expr[index:m.start()]
            index = m.end()
            tmp += self.ctx.evaluate(m.group(1), record, raw=False)
        tmp += self.expr[index:]
        return tmp


class VariableContext:
    def __init__(self, config):
        self.config = config

    def evaluate(self, name, record, raw=True):
        value = record[name]
        if raw:
            return value
        return self.config.columnType(name).repr_value(value)
