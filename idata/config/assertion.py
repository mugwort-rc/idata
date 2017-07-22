from . import expression


class AssertionBase:
    pass


class RowAssertion(AssertionBase):
    def __init__(self, config, assert_config):
        assert assert_config["type"] == "row"
        self.config = config
        self.assert_config = assert_config

    def check(self, data):
        if self.type == "eq":
            return self.assertEqual(data)
        elif self.type == "in":
            return self.assertIn(data)
        raise NotImplementedError

    def error_message(self, data):
        if self.type == "eq":
            source = self.get(self.args_source, data)
            return "{} != {}".format(source, repr(self.args_value))
        elif self.type == "in":
            source = self.get(self.args_source, data)
            return "{} not in {}".format(repr(self.args_value), source)
        raise NotImplementedError

    def assertEqual(self, data):
        source = self.get(self.args_source, data)
        value = self.args_value
        return source == value

    def assertIn(self, data):
        value = self.args_value
        source = self.get(self.args_source, data)
        return value in source

    def get(self, item, data):
        if isinstance(item, int):
            return data[item]
        elif isinstance(item, str) and expression.is_slice(item):
            s = expression.to_slice(item)
            return data[s]
        raise NotImplementedError

    @property
    def type(self):
        return self.assert_config["f"]

    @property
    def args_source(self):
        return self.assert_config["args"]["source"]

    @property
    def args_value(self):
        value = self.assert_config["args"]["value"]
        if expression.is_config_expr(value):
            value = self.config.evaluate(value)
        return value
