from __future__ import absolute_import
import unittest
from django.test import TestCase
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch
from nose.tools import assert_true
from unittest.mock import create_autospec
from v0.ui.analytics.views import (GetLeadsDataGeneric, get_data_analytics, get_details_by_higher_level,
                                   get_details_by_higher_level_geographical)
from v0.ui.analytics.utils import ranged_data_to_other_groups, z_calculator_array_multiple, \
    calculate_freqdist_mode_from_list
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


def returns(*accepted_return_type_tuple):
    '''
    Validates the return type. Since there's only ever one
    return type, this makes life simpler. Along with the
    accepts() decorator, this also only does a check for
    the top argument. For example you couldn't check
    (<type 'tuple'>, <type 'int'>, <type 'str'>).
    In that case you could only check if it was a tuple.
    '''

    def return_decorator(validate_function):
        # No return type has been specified.
        if len(accepted_return_type_tuple) == 0:
            raise TypeError('You must specify a return type.')

        @functools.wraps(validate_function)
        def decorator_wrapper(*function_args):
            # More than one return type has been specified.
            if len(accepted_return_type_tuple) > 1:
                raise TypeError('You must specify one return type.')

            # Since the decorator receives a tuple of arguments
            # and the is only ever one object returned, we'll just
            # grab the first parameter.
            accepted_return_type = accepted_return_type_tuple[0]

            # We'll execute the function, and
            # take a look at the return type.
            return_value = validate_function(*function_args)
            return_value_type = type(return_value)

            if return_value_type is not accepted_return_type:
                raise InvalidReturnType(return_value_type,
                                        validate_function.__name__)

            return return_value

        return decorator_wrapper

    return return_decorator


@accepts(int, int)
@returns(int)
def add_ints_test(a, b):
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
        add_ints_test(0, 0)
        self.assertEqual(add_ints_test(2, 3), 5)

    # generally, a function has the following tests:
    # 1. Returns expected output if all inputs are blank
    # 2. Number of arguments should match the original signature
    # 3. Type of arguments should also match (for functions without default values only)
    # arguments may be replaced by actual values in validate_* functions for testing

    def test_get_data_analytics(self):
        self.assertEqual(get_data_analytics({}, {}, [], [], {}, {}), [])
        sample_args = ({"data_scope": "mock"}, {"data_point": "mock"}, ['test_raw_data'], ['test_metrics'],
                                    {"stat_info": "mock"}, {"high_level_stat_info": "mock"})
        mock_get_data_analytics = create_autospec(get_data_analytics, return_value='# args matched')
        mock_get_data_analytics(*sample_args)
        validate_get_data_analytics(*sample_args)

    def test_get_details_by_higher_level(self):
        self.assertEqual(get_details_by_higher_level(None, None, []), [])
        sample_args = ('highest_level', 'lowest_level', ['element 1', 'element 2'])
        mock_get_details_by_higher_level = create_autospec(get_details_by_higher_level, return_value='# args matched')
        mock_get_details_by_higher_level(*sample_args)

    def test_ranged_data_to_other_groups(self):
        self.assertEqual(ranged_data_to_other_groups([], [], '', '', '', '', []),[])
        sample_args = (["base_array"], ["range_array"], 'test_start', 'test_end',
                       'test_base_value', 'test_assigned_value', ['test_others'])
        validate_ranged_data_to_other_groups(*sample_args)

    def test_get_details_by_higher_level_geographical(self):
        self.assertEqual(get_details_by_higher_level_geographical('', []),{'final_dict':{}, 'single_list':[]})
        sample_args = ('city',["Bengaluru", "Chandigarh"])
        mock_get_details_by_higher_level_geographical = create_autospec(get_details_by_higher_level_geographical,
                                                                        return_value='# args matched')
        mock_get_details_by_higher_level_geographical(*sample_args)


class TestUtils(TestCase):

    def test_z_calculator_array_multiple(self):
        self.assertEqual(z_calculator_array_multiple([],{}),[])
        sample_args = (['sample_array'],{'sample_array_dict':['sample_element']})
        mock_z_calculator_array_multiple = create_autospec(z_calculator_array_multiple, return_value = 'success')
        mock_z_calculator_array_multiple(*sample_args)

    def test_calculate_freqdist_mode_from_list(self):
        self.assertEqual(calculate_freqdist_mode_from_list([]),{})
        sample_args = (['sample_list'])
        mock_calculate_freqdist_mode_from_list = create_autospec(calculate_freqdist_mode_from_list,
                                                                 return_value = 'success')
        mock_calculate_freqdist_mode_from_list(*sample_args)

