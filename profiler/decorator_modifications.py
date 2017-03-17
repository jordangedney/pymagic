def compose_decorators(decorator_list):
    """
    Combine multiple decorators together- order is important.
    compose_decorators(dec1, dec2) is the same as doing:

    @dec1
    @dec2
    def function_here()
    """
    def composed_decorators(func):
        for decorator in reversed(decorator_list):
            func = decorator(func)
        return func
    return composed_decorators

def decorate_methods_in_class(cls, decorator):
    """
    Takes a single decorator, or a list of decorators, and applies them to
    every method in the class.
    """
    if isinstance(decorator, list):
        decorator = compose_decorators(decorator)

    for name, obj in inspect.getmembers(cls, inspect.ismethod):
        setattr(cls, name, decorator(obj))

def decorate_class(cls, decorator):
    """
    Convenience Class decorator for decorating every method inside a class.
    This is equivalent to running decorate_methods_in_class(class_name,
    decorators) after the class definition.
    """
    @wraps(cls)
    def wrapper(*args, **kargs):
        decorate_methods_in_class(cls, decorator)
        return cls(*args, **kargs)
    return wrapper

def decorate_classes(module_name, decorator):
    """
    Takes a decorator, or a list of decorators, and applies them to every
    method in every class *in the defined module*.
    """
    clsmembers = inspect.getmembers(sys.modules[module_name],
            lambda member: inspect.isclass(member) and
                           member.__module__ == module_name)

    for _, cls in clsmembers:
        decorate_methods_in_class(cls, decorator)


def decorate_everything(module_name, decorator):
    """
    Takes a decorator, or a list of decorators, and applies them to every
    method in *every class defined*.
    """
    clsmembers = inspect.getmembers(
                     sys.modules[module_name],
                     lambda member: inspect.isclass(member))

    for _, cls in clsmembers:
        decorate_methods_in_class(cls, decorator)
