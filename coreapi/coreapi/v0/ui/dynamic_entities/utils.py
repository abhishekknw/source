from validate_email import validate_email
from datetime import datetime
from models import SupplyEntityType
from bson.objectid import ObjectId


def validate_entity_type_data(entity_type_dict):
    possible_attribute_types = ['FLOAT', 'INT', 'STRING', 'BOOLEAN', 'EMAIL', 'PASSWORD', 'PHONE', 'DROPDOWN', 'RADIO',
                                'CHECKBOX', 'TEXTAREA', 'DATE', 'DATETIME', 'INVENTORYLIST']
    validation_msg_dict = {'repeating_name_field': [], "type_mismatch": []}
    is_valid = True
    entity_type_attributes = entity_type_dict["entity_attributes"]
    all_attribute_names = []
    for single_attribute in entity_type_attributes:
        if single_attribute['name'] in all_attribute_names:
            is_valid = False
            validation_msg_dict['repeating_name_field'].append(single_attribute['name'])
        if single_attribute['type'] not in possible_attribute_types:
            is_valid = False
            validation_msg_dict['type_mismatch'].append(single_attribute['type'])
        all_attribute_names.append(single_attribute['name'])
    return is_valid, validation_msg_dict


def validate_attribute_with_type(entity_type_attribute_dict, attribute_value):
    attribute_is_valid = True
    attribute_type = entity_type_attribute_dict['type']
    if attribute_type in ['DROPDOWN', 'CHECKBOX', 'RADIO']:
        attribute_options = entity_type_attribute_dict['options'] if 'options' in entity_type_attribute_dict else None
        if not attribute_options:
            return False
        if attribute_value not in attribute_options:
            return False
    if attribute_type == 'FLOAT' and (isinstance(attribute_value,float) or isinstance(attribute_value,int)) is False:
        return False
    if attribute_type == 'INT' and isinstance(attribute_value,int) is False:
        return False
    if attribute_type == 'STRING' and isinstance(attribute_value,basestring) is False:
        return False
    if attribute_type == 'BOOLEAN' and isinstance(attribute_value,bool) is False:
        return False
    if attribute_type == 'EMAIL':
        return validate_email(attribute_value)
    if attribute_type == 'PASSWORD' and isinstance(attribute_value,basestring) is False:
        return False
    if attribute_type == 'TEXTAREA' and isinstance(attribute_value,basestring) is False:
        return False
    if attribute_type == 'DATE' and isinstance(attribute_value,datetime.date) is False:
        return False
    if attribute_type == 'DATETIME' and isinstance(attribute_value,datetime) is False:
        return False
    return attribute_is_valid


def validate_with_entity_type(entity_dict,entity_type_id):
    entity_type = list(SupplyEntityType.objects.raw({'_id': ObjectId(entity_type_id)}))
    validation_msg_dict = {'missing_data': [], "data_mismatch": []}
    is_valid = True
    if len(entity_type) == 0:
        validation_msg_dict['data_mismatch'].append("entity_type_id")
        return (False, validation_msg_dict)
    entity_type = entity_type[0]
    entity_type_attribute_dict = {single_attribute["name"]: single_attribute for single_attribute in entity_type.entity_attributes}
    new_entity_attribute_dict = {single_attribute["name"]: single_attribute for single_attribute in entity_dict["entity_attributes"]}
    for key, value in entity_type_attribute_dict.items():
        if 'is_required' in value and value['is_required']:
            if key not in new_entity_attribute_dict:
                is_valid = False
                validation_msg_dict['missing_data'].append(key)
        if key in new_entity_attribute_dict:
            attribute_dict = entity_type_attribute_dict[key]
            attribute_value = new_entity_attribute_dict[key]['value']
            attribute_is_valid = validate_attribute_with_type(attribute_dict, attribute_value)
            if not attribute_is_valid:
                is_valid = False
                validation_msg_dict['data_mismatch'].append(key)
    return is_valid, validation_msg_dict
