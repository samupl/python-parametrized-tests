class ClassNotDecorated(BaseException):
    pass


def is_parametrized(obj):
    if hasattr(obj, 'parametrized') and obj.parametrized:
        return True
    return False


def generate_method_name(method, iteration, params):
    return 'test_' + method.parametrized_name.format(
                    method_name=method.__name__,
                    iter=iteration,
                    **method.parametrized_fmt_func(params)
                )


def parametrized_test_case(cls):
    """
    A decorator that marks the specified TestCase as parametrized.

    When a class is marked as parametrized, the interpreter searches for
methods marked with the @parametrized
    decorator.

    For each method that's found as being marked with @parametrized, a
stub test method will be generated, and that
    generated test method will be picked up by test runners.

    :param cls: Class to be decorated
    :type cls: object
    """
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)

        if not is_parametrized(attr):
            continue

        for i, params in enumerate(attr.parameters):
            if type(params) not in (list, tuple) or len(params) == 0:
                params = [params]

            def generate_test(base_test_method, args):
                def test(self):
                    try:
                        return base_test_method(self, *args)
                    except TypeError:
                        raise
                return test

            setattr(
                cls,
                generate_method_name(attr, i, params),
                generate_test(attr, params)
            )
    return cls


def parametrized(args, method_fmt='{method_name}_{iter}',
                 method_fmt_func=lambda params: {}):
    """
    Mark a test method as parametrized.

    For each method that's found as being marked with @parametrized, a
stub test method will be generated, and that
    generated test method will be picked up by test runners.

    Each of those test methods will call the original decorated function
with the args specified in the decorator.

    The args parameter should be a list or tuple of arguments that will
be passed to your tempalte method.

    By altering the `method_fmt` parameter (string) you can alter how
each generated test method will be called.
    The default is "{method_name}_{iter}", so if your parametrized test
method is called 'example', then
    your generated test methods will be called 'test_example_0',
'test_example_1', etc. The 'test_' prefix is always
    added automatically, so your parametrized method should not start
with 'test_' (this prevents test runners from
    picking up your template method as a real test method, which would
obviously fail).

    The `method_fmt` string is then processed by the .format() method.
There are always two keywords passed to this
    method: `method_name` (how your template test method is called) and
`iter` (the number of generated function).

    You can also provide a callable to `method_fmt_func`, that should
accept one parameter, which will be your args.
    This callable should return a dictionary, that will be further
passed to `method_fmt` format method. If your args
    is a list of two-value tuples, like [('test_string',
'expected_string'), ('test_string2', 'expected_string2')],
    then you can pass a simple lambda to include the first item in each
tuple in the name of each generated method:

    method_fmt='{method_name}_{expected}',
    method_fmt_func=lambda params: {'expected': params[0]}

    :param args: Arguments that the decorated function will be called
with.
    :type args: list or tuple
    :param method_fmt: The formatter that determines each generated test
method name
    :type method_fmt: str
    :param method_fmt_func: A function that should return a dictionary
to be passed to method_fmt for further formatting
    :type method_fmt_func: callable
    """

    def decorator(f):
        f.parametrized = True
        f.parameters = args
        f.parametrized_name = method_fmt
        f.parametrized_fmt_func = method_fmt_func
        return f
    return decorator
