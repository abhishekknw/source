from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

import v0.ui.utils as ui_utils
import v0.constants as v0_constants
import models as v0_models


def do_each_model(myModel, supplier_model, content_type):
    """
    :param myModel: Model whose fields need to be populated
    :param supplier_model: supplier type model
    :param content_type:  the content Type object
    :return: success in case of success, failure otherwise
    """
    function = do_each_model.__name__
    supplier_id = ''
    try:
        for row in myModel.objects.all():
            supplier_id = row.supplier_id
            if row.supplier:
                supplier_type = supplier_model.objects.get(supplier_id=row.supplier.supplier_id)
                row.content_type = content_type
                row.object_id = row.supplier.supplier_id
                row.content_object = supplier_type
                row.save()
        return ui_utils.handle_response(function, data='success', success=True)
    except ObjectDoesNotExist as e:
        return ui_utils.handle_response(function, data=supplier_id, exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def get_group_permission(user, group_code_name):
    """
    Args:
        user: a User instance
        group_code_name: can be'master_users', 'ops_heads', 'bd_heads', 'external_bds'

    Returns: True or False depending weather user belongs to group indicated by group_code_name.

    """
    if user.is_anonymous() or not hasattr(user, 'user_code'):
        return False
    if user.user_code not in v0_constants.group_codes[group_code_name]:
        return False
    return True


def get_user_related_query(model, permission_codes):
    """
    Args:
        model: model instance
        permission_codes: ['01', '02']

    Returns: a Q object which is a result of ORing indivual queries.

    """
    function = get_user_related_query.__name__
    try:
        # get all fields of the model
        fields = model._meta.get_fields()
        # to check of 'user' is present directly as a field
        is_user_field_present = False
        for field in fields:
            if 'user' == field.name:
                is_user_field_present = True
                break
        custom_query = Q()
        query_dict = {}
        # if user is present directly as a field
        if is_user_field_present:
            # set this to base_query
            base_query = 'user__user_code__startswith'
        else:
            # check if the model is in predefined list that contains the base_query format
            if model.__name__ in v0_constants.model_name_user_mapping.keys():
                base_query = v0_constants.model_name_user_mapping[model.__name__] + '__startswith'
            else:
                # if not return proper error
                return ui_utils.handle_response(function, data='model not in predefined list of models having base query')

        # in either case build a query by ORing individual queries.
        for permission_code in permission_codes:
            code = str(permission_code['extra_permission_code'])
            query_dict[base_query] = code
            if custom_query:
                custom_query |= Q(**query_dict)
            else:
                custom_query = Q(**query_dict)
        # return the custom query
        return ui_utils.handle_response(function, data=custom_query, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def get_user_related(model_instance, user, kwargs=None):
    """
    Args:
        model_instance: a model instance
        user: User instance
        kwargs: a dictionary of optional filters required

    purpose of the function is to give results when a user wants to access not only objects created by him, but  all
    objects which are created by any user under him. also it is useful, when a user with code '01' is granted
    permissions to access objects created by '02' or '03' etc.

    Returns: a queryset
    """
    function = get_user_related.__name__
    try:
        main_query = Q()

        # prepare the main query
        if kwargs:
            main_query = Q(**kwargs)

        # fetch the user's current permission code
        user_permission_code = user.user_code

        # get the extra permission codes which may be defined for this user
        extra_permission_codes = list(v0_models.CustomPermissions.objects.filter(user=user).values('extra_permission_code'))
        # even the user current permission code is going by name 'extra_permission_code'. don't be confused.
        extra_permission_codes.append({'extra_permission_code': user_permission_code})

        # the query that ORes individual permission codes.
        response = get_user_related_query(model_instance, extra_permission_codes)
        if not response.data['status']:
            return response
        # if found, fetch it
        custom_query = response.data['data']
        # join together the main and custom query and return
        if main_query and custom_query:
            final_query = main_query & custom_query
        elif main_query:
            final_query = main_query
        else:
            final_query = custom_query
        result = model_instance.objects.filter(final_query)
        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)
