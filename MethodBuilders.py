ARITHMETIC_OVERLOADS = ['__add__', '__sub__', '__mul__', '__div__', '__mod__', '__divmod__']


def operator_override_loop(obj: object, attr: str, operator_list: List = []):
    for operator in operator_list:
        setattr(
            self,
            self.getattr(operator),
            lambda: operator_type_validator(obj, attr, operator)
            )


def operator_type_validator(obj: object, attr: str, operator: str):
    """
    Given an object, a representative attribute, and a target operator to override:
        return a new function which:
            takes an argument,
            identifies a proper order of operations:
                if the argument's type is the target type, proceed as normal
                if the argument's type matches the object's type, fetch the target attribute from it then operate
                finally try to cast the argument into the target type. If that fails throw a TypeError
            performs the passed operation on the object and argument,
            and returns a new instance of the passed object's type constructed from the result of operation
    """

    def convert_to_attr_type(a):
        try:
            return type(getattr(obj, attr))(a)
        except (ValueError, TypeError):
            #Handles a unique exception when trying to convert a string expression to int
            if type(a) == str:
                try: type(getattr(obj, attr))(eval(a))
                except: pass
            raise TypeError

    #Escape clause in case of derp
    if attr not in obj.__dir__():
        raise KeyError


    #formally defining these variables to make the return lambda easier to read
    obj_attr_val = getattr(obj, attr)
    attr_type = type(obj_attr_val)
    op = getattr(attr_type, operator)


    return lambda arg: {
        attr_type: type(obj)(op(obj_attr_val, arg)),
        type(obj): type(obj)(op(obj_attr_val, getattr(arg, attr))),
        object: type(obj)(op(obj_attr_val, convert_to_attr_type(arg))),
        }[type(arg)]

