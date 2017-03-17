import time, types, itertools, inspect
from functools import wraps

from decorator_tools import decorate_classes, decorate_everything

'''
Contains two types of functions:

Decorators which log function information
Rules which apply said decorators
'''

# Decorators ------------------------------------------------------------------

@decorator_or_function
def log_entry_and_exit(func=None, log_func=print):
    '''Decorator which logs when entering and exiting a function.'''
    @wraps(func)
    def wrapper(*args, **kargs):
        try:
            class_name = args[0].__class__.__name__
        except:
            s = inspect.stack()
            class_name = inspect.getmodulename(s[1][1])

        func_name = func.__name__
        log_func('{}: Entering function {}'.format(class_name, func_name))
        result = func(*args, **kargs)
        log_func('{}: Exiting function {}'.format(class_name, func_name))
        return result
    return wrapper

def log_entry_and_exit_times(func=None, log_func=print):
    '''Decorator which logs when entering and exiting a function.'''
    @wraps(func)
    def wrapper(*args, **kargs):
        start_time = time.time()
        result = func(*args, **kargs)
        end_time = time.time()
        function_time = end_time - start_time
        log_func('Function took: {} seconds'.format(int(function_time)))
        return result
    return wrapper

def log_args(func=None, log_func=print):
    '''Decorator which logs the arguments and kargs passed to a function.'''
    @wraps(func)
    def wrapper(*args, **kargs):
        var_names = func.__code__.co_varnames
        keyword_and_args = zip(var_names[1:], args[1:])
        var_string = ", ".join('{}={}'.format(*k) for k in keyword_and_args)
        args_string = 'Args: ' + var_string if var_string else ''
        if kargs: args_string += ' Kargs: ' + str(kargs)
        if args_string: log_func(args_string)
        return func(*args, **kargs)
    return wrapper

def log_formatted_args(func=None, log_func=print):
    '''Decorator which logs a shortened version of a functions arguments.'''
    @wraps(func)
    def wrapper(*args, **kargs):
        var_names = func.__code__.co_varnames
        args_copy = [itertools.tee(arg)
                     if isinstance(arg, types.GeneratorType)
                     else arg for arg in args]
        pretty_args = []
        for arg in args_copy:
            if isinstance(arg, types.GeneratorType):
                arg = [i.next() for i in range(3)] + ['...']

            if isinstance(arg, set):
                arg = list(arg)

            if isinstance(arg, list) and len(arg) > 5:
                pretty_arg = arg[:3]
                pretty_arg.append('...')
                pretty_arg.append(arg[-1])
                pretty_args.append(pretty_arg)
            else:
                pretty_args.append(arg)

        keyword_and_args = zip(var_names[1:], pretty_args[1:])
        var_string = ", ".join('{}={}'.format(*k) for k in keyword_and_args)
        args_string = 'Args: ' + var_string if var_string else ''
        if kargs: args_string += ' Kargs: ' + str(kargs)
        if args_string: log_func(args_string)
        return func(*args, **kargs)
    return wrapper

# Applicators -----------------------------------------------------------------

def log_classes(module_name,
                decorator=( log_entry_and_exit
                          , log_formatted_args
                          )):
    '''
    Usage: Add the line log_classes(__name__) to the bottom of a file.
    For every class defined in the current file,
    For every function in that class, ...
    '''
    decorate_classes(module_name, decorator)

def profiler(module_name,
            decorator=( log_entry_and_exit
                      , log_formatted_args
                      , log_entry_and_exit_times
                      )):
    '''
    Usage: Add the line profiler(__name__) to the bottom of a file.
    For every class defined,
    For every function in that class, ... 
    '''
    decorate_everything(module_name, decorator)

