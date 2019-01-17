from __future__ import absolute_import
import unittest
from django.test import TestCase
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch
from nose.tools import assert_true
from unittest.mock import create_autospec
from v0.ui.analytics.views import GetLeadsDataGeneric, get_data_analytics, get_details_by_higher_level
from v0.ui.analytics.utils import ranged_data_to_other_groups
import requests, functools


class ArgumentValidationError(ValueError):
    '''
    Raised when the type of an argument to a function is not what it should be.
    '''

    def __init__(self, arg_num, func_name, accepted_arg_type):
        self.error = 'The {0} argument of {1}() is not a {2}'.format(arg_num,
                                                                     func_name,
                                                                     accepted_arg_type)

    def __str__(self):
        return self.error


class InvalidArgumentNumberError(ValueError):
    '''
    Raised when the number of arguments supplied to a function is incorrect.
    Note that this check is only performed from the number of arguments
    specified in the validate_accept() decorator. If the validate_accept()
    call is incorrect, it is possible to have a valid function where this
    will report a false validation.
    '''

    def __init__(self, func_name):
        self.error = 'Invalid number of arguments for {0}()'.format(func_name)

    def __str__(self):
        return self.error


class InvalidReturnType(ValueError):
    '''
    As the name implies, the return value is the wrong type.
    '''

    def __init__(self, return_type, func_name):
        self.error = 'Invalid return type {0} for {1}()'.format(return_type,
                                                                func_name)

    def __str__(self):
        return self.error


def ordinal(num):
    '''
    Returns the ordinal number of a given integer, as a string.
    eg. 1 -> 1st, 2 -> 2nd, 3 -> 3rd, etc.
    '''
    if 10 <= num % 100 < 20:
        return '{0}th'.format(num)
    else:
        ord = {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(num % 10, 'th')
        return '{0}{1}'.format(num, ord)


def accepts(*accepted_arg_types):
    '''
    A decorator to validate the parameter types of a given function.
    It is passed a tuple of types. eg. (<type 'tuple'>, <type 'int'>)

    Note: It doesn't do a deep check, for example checking through a
          tuple of types. The argument passed must only be types.
    '''

    def accept_decorator(validate_function):
        # Check if the number of arguments to the validator
        # function is the same as the arguments provided
        # to the actual function to validate. We don't need
        # to check if the function to validate has the right
        # amount of arguments, as Python will do this
        # automatically (also with a TypeError).
        @functools.wraps(validate_function)
        def decorator_wrapper(*function_args, **function_args_dict):
            if len(accepted_arg_types) is not len(accepted_arg_types):
                raise InvalidArgumentNumberError(validate_function.__name__)

            # We're using enumerate to get the index, so we can pass the
            # argument number with the incorrect type to ArgumentValidationError.
            for arg_num, (actual_arg, accepted_arg_type) in enumerate(zip(function_args, accepted_arg_types)):
                if not type(actual_arg) is accepted_arg_type:
                    ord_num = ordinal(arg_num + 1)
                    raise ArgumentValidationError(ord_num,
                                                  validate_function.__name__,
                                                  accepted_arg_type)

            return validate_function(*function_args)

        return decorator_wrapper

    return accept_decorator


@accepts(int, int)
def add_test(a, b):
    '''
    Adds two numbers. It accepts two
    integers, and returns an integer.
    '''

    return a+b

@accepts(dict,dict,list,list,dict,dict)
def validate_get_data_analytics(scope,point,raw,metrics,lower,higher):
    pass

@accepts(list, list, str, str, str, str, list)
def validate_ranged_data_to_other_groups(base_array, range_array, start_field, end_field,
                                base_value_field, assigned_value_field, other_fields):
    pass


class TestAnalytics(TestCase):

    # test on sample function for failing if system upgrades result in change in functioning of commands
    # if there are problems with function(s) only, this test will always pass
    def test_samples(self):
        add_test(0, 0)
        self.assertEqual(add_test(2,3), 5)

    # generally, a function has the following tests:
    # 1. Returns expected output if all inputs are blank
    # 2. Number of arguments should match the original signature
    # 3. Type of arguments should also match
    # 2 & 3 apply for functions without default values
    # arguments may be replaced by actual values in validate_* functions for testing

    def test_get_data_analytics(self):
        self.assertEqual(get_data_analytics({},{},[],[],{},{}), [])
        validate_get_data_analytics({"data_scope": "mock"}, {"data_point": "mock"}, ['test_raw_data'], ['test_metrics'],
                                    {"stat_info": "mock"}, {"high_level_stat_info": "mock"})
        self.assertEqual(get_details_by_higher_level(None, None, []),[])

    def test_get_details_by_higher_level(self):
        self.assertEqual(get_details_by_higher_level(None, None, []), [])

    def test_ranged_data_to_other_groups(self):
        self.assertEqual(ranged_data_to_other_groups([], [], '', '', '', '', []),[])
        validate_ranged_data_to_other_groups({"base_array": "mock"}, {"range_array": "mock"}, 'test_start', 'test_end',
                                             'test_base_value', 'test_assigned_value', ['test_others'])




