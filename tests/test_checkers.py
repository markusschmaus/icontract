#!/usr/bin/env python3

# pylint: disable=protected-access
# pylint: disable=missing-docstring

import functools
import unittest

import icontract._checkers
from icontract._globals import CallableT


def decorator_plus_1(func: CallableT) -> CallableT:
    def wrapper(*args, **kwargs):  # type: ignore
        return func(*args, **kwargs) + 1

    functools.update_wrapper(wrapper=wrapper, wrapped=func)

    return wrapper  # type: ignore


def decorator_plus_2(func: CallableT) -> CallableT:
    def wrapper(*args, **kwargs):  # type: ignore
        return func(*args, **kwargs) + 2

    functools.update_wrapper(wrapper=wrapper, wrapped=func)

    return wrapper  # type: ignore


class TestUnwindDecoratorStack(unittest.TestCase):
    def test_wo_decorators(self) -> None:
        def func() -> int:
            return 0

        self.assertListEqual([0], [a_func() for a_func in icontract._checkers._walk_decorator_stack(func)])

    def test_with_single_decorator(self) -> None:
        @decorator_plus_1
        def func() -> int:
            return 0

        self.assertListEqual([1, 0], [a_func() for a_func in icontract._checkers._walk_decorator_stack(func)])

    def test_with_double_decorator(self) -> None:
        @decorator_plus_2
        @decorator_plus_1
        def func() -> int:
            return 0

        self.assertListEqual([3, 1, 0], [a_func() for a_func in icontract._checkers._walk_decorator_stack(func)])


if __name__ == '__main__':
    unittest.main()
