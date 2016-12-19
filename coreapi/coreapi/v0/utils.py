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
        fields = myModel._meta.get_all_field_names() 
        field_name = None

        for field in fields:
            if field in ['supplier_id', 'society_id']:
                field_name = field
                break

        if not field_name:
            return ui_utils.handle_response(function, data='The model {0} does not have supplier_id field name'.format(myModel))        

        for row in myModel.objects.all():
            supplier_id = getattr(row, field_name)
            try:
                if supplier_id:
                    supplier_type = supplier_model.objects.get(supplier_id=row.supplier.supplier_id)   
                    row.content_type = content_type
                    row.object_id = row.supplier.supplier_id
                    row.content_object = supplier_type
                    row.save()
            except ObjectDoesNotExist as e:
                try:
                    q = {field_name: supplier_id}
                    myModel.objects.filter(**q).delete()
                    continue
                except Exception as e:
                    return ui_utils.handle_response(function, exception_object=e)
        return ui_utils.handle_response(function, data='success', success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def get_group_permission(user, group_code_name):
    """
    Args:
        user: a User instance
        group_code_name: can be'master_users', 'ops_heads', 'bd_heads', 'external_bds'

    Returns: True or False depending weather user belongs to group indicated by group_code_name.

    """
    if not hasattr(user, 'user_code'):
        return False
    if user.user_code not in v0_constants.group_codes[group_code_name]:
        return False
    return True

