from __future__ import absolute_import
from validate_email import validate_email
from datetime import datetime
from .models import SupplySupplierType, BaseSupplySupplierType
from bson.objectid import ObjectId


def validate_supplier_type_data(supplier_type_dict):
    possible_attribute_types = ['FLOAT', 'INT', 'STRING', 'BOOLEAN', 'EMAIL', 'PASSWORD', 'PHONE', 'DROPDOWN', 'RADIO',
                                'CHECKBOX', 'TEXTAREA', 'DATE', 'DATETIME', 'INVENTORY_TYPE','INVENTORY', "SUPPLIER_TYPE", "BASE_SUPPLIER_TYPE"]
    validation_msg_dict = {'repeating_name_field': [], "type_mismatch": [], "other_errors": [],
                           "base_supplier_fields_mismatch": []}
    is_valid = True
    supplier_type_attributes = supplier_type_dict["supplier_attributes"]
    base_supplier_type_id = supplier_type_dict["base_supplier_type_id"]
    all_attribute_names = []
    base_supplier_type = list(BaseSupplySupplierType.objects.raw({'_id': ObjectId(base_supplier_type_id)}))
    if len(base_supplier_type) == 0:
        is_valid = False
        validation_msg_dict['other_errors'].append("base_supplier_type_not_found")
        return is_valid, validation_msg_dict
    base_supplier_type = base_supplier_type[0]
    supplier_type_attributes_dict = {}
    for single_attribute in supplier_type_attributes:
        if single_attribute['name'] in all_attribute_names:
            is_valid = False
            validation_msg_dict['repeating_name_field'].append(single_attribute['name'])
        if single_attribute['type'] not in possible_attribute_types:
            is_valid = False
            validation_msg_dict['type_mismatch'].append(single_attribute['type'])
        all_attribute_names.append(single_attribute['name'])
        supplier_type_attributes_dict[single_attribute['name']] = single_attribute
    for base_supplier_attribute in base_supplier_type.supplier_attributes:
        if "is_required" in base_supplier_attribute:
            if base_supplier_attribute["is_required"]:
                if base_supplier_attribute["name"] not in supplier_type_attributes_dict:
                    is_valid = False
                    validation_msg_dict["base_supplier_fields_mismatch"].append(base_supplier_attribute["name"])
                else:
                    if supplier_type_attributes_dict[base_supplier_attribute["name"]]["type"] != base_supplier_attribute["type"]:
                        is_valid = False
                        validation_msg_dict["base_supplier_fields_mismatch"].append(base_supplier_attribute["name"])

    return is_valid, validation_msg_dict


def validate_attribute_with_type(supplier_type_attribute_dict, attribute_value):
    attribute_is_valid = True
    attribute_type = supplier_type_attribute_dict['type']
    if attribute_type in ['DROPDOWN', 'CHECKBOX', 'RADIO']:
        attribute_options = supplier_type_attribute_dict['options'] if 'options' in supplier_type_attribute_dict else None
        if not attribute_options:
            return False
        if attribute_value not in attribute_options:
            return False
    if attribute_type == 'FLOAT' and (isinstance(attribute_value,float) or isinstance(attribute_value,int)) is False:
        return False
    if attribute_type == 'INT' and isinstance(attribute_value,int) is False:
        return False
    if attribute_type == 'STRING' and isinstance(attribute_value,str) is False:
        return False
    if attribute_type == 'BOOLEAN' and isinstance(attribute_value,bool) is False:
        return False
    if attribute_type == 'EMAIL':
        return validate_email(attribute_value)
    if attribute_type == 'PASSWORD' and isinstance(attribute_value,str) is False:
        return False
    if attribute_type == 'TEXTAREA' and isinstance(attribute_value,str) is False:
        return False
    if attribute_type == 'DATE' and isinstance(attribute_value,datetime.date) is False:
        return False
    if attribute_type == 'DATETIME' and isinstance(attribute_value,datetime) is False:
        return False
    return attribute_is_valid


def validate_with_supplier_type(supplier_dict,supplier_type_id):
    supplier_type = list(SupplySupplierType.objects.raw({'_id': ObjectId(supplier_type_id)}))
    validation_msg_dict = {'missing_data': [], "data_mismatch": []}
    is_valid = True
    if len(supplier_type) == 0:
        validation_msg_dict['data_mismatch'].append("supplier_type_id")
        return (False, validation_msg_dict)
    supplier_type = supplier_type[0]
    supplier_type_attribute_dict = {single_attribute["name"]: single_attribute for single_attribute in supplier_type.supplier_attributes}
    new_supplier_attribute_dict = {single_attribute["name"]: single_attribute for single_attribute in supplier_dict["supplier_attributes"]}
    for key, value in supplier_type_attribute_dict.items():
        if 'is_required' in value and value['is_required']:
            if key not in new_supplier_attribute_dict:
                is_valid = False
                validation_msg_dict['missing_data'].append(key)
        if key in new_supplier_attribute_dict:
            attribute_dict = supplier_type_attribute_dict[key]
            attribute_value = new_supplier_attribute_dict[key]['value'] if 'value' in new_supplier_attribute_dict[key] else None
            # attribute_is_valid = validate_attribute_with_type(attribute_dict, attribute_value)
            # if not attribute_is_valid:
            #     is_valid = False
            #     validation_msg_dict['data_mismatch'].append(key)
    return is_valid, validation_msg_dict
