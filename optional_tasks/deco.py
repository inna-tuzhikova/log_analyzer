#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper, reduce
from typing import Callable


def disable(fun: Callable):
    """
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    """
    return fun


def decorator(decorator_fun: Callable):
    """
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    """
    def decorator_wrapper(fun):
        wrapper = decorator_fun(fun)
        return update_wrapper(wrapper=wrapper, wrapped=fun)

    return update_wrapper(wrapper=decorator_wrapper, wrapped=decorator_fun)


@decorator
def countcalls(fun: Callable):
    """Decorator that counts calls made to the function decorated."""

    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return fun(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


@decorator
def memo(fun: Callable):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """
    cached = {}

    def get_args_key(args, kwargs) -> tuple:
        return *args, *kwargs.items()

    def wrapper(*args, **kwargs):
        key = get_args_key(args, kwargs)
        if key not in cached:
            cached[key] = fun(*args, **kwargs)
        return cached[key]

    return wrapper


@decorator
def n_ary(fun: Callable):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """
    def wrapper(*args):
        if len(args) == 0:
            raise ValueError(f'{fun.__name__} accepts at least one arg')
        if len(args) == 1:
            return args[0]
        elif len(args) == 2:
            return fun(*args)
        else:
            return reduce(fun, args)

    return wrapper


def trace(tab: str):
    """Trace calls made to function decorated.

    @trace('____')
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    """

    prefix = ['']

    def args_to_str(args, kwargs):
        return ', '.join(map(str, args))

    @decorator
    def wrapped_decorator(fun: Callable):
        def wrapped(*args, **kwargs):
            args_str = args_to_str(args, kwargs)
            print(f'{prefix[0]} --> {fun.__name__}({args_str})')
            prefix[0] += tab
            result = fun(*args, **kwargs)
            prefix[0] = prefix[0][:-len(tab)]
            print(f'{prefix[0]} <-- {fun.__name__}({args_str}) == {result}')
            return result
        return wrapped
    return wrapped_decorator


@countcalls
@memo
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace('####')
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print('foo was called', foo.calls, 'times')

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print('bar was called', bar.calls, 'times')

    print(fib.__doc__)
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
