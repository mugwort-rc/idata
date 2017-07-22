class TypeBase:
    def repr_value(self, value):
        return repr(value)


class ObjectType(TypeBase):
    pass


class StrType(TypeBase):
    pass


class IntType(TypeBase):
    pass


class FloatType(TypeBase):
    pass
