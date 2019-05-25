from __future__ import absolute_import
from validate_email import validate_email
from datetime import datetime
from .models import BaseBookingTemplate, BookingTemplate
from bson.objectid import ObjectId


def validate_booking(booking_template):
    possible_attribute_types = ['FLOAT', 'INT', 'STRING', 'BOOLEAN', 'EMAIL', 'PASSWORD', 'PHONE', 'DROPDOWN', 'RADIO',
                                'CHECKBOX', 'TEXTAREA', 'DATE', 'DATETIME', 'INVENTORY_TYPE','INVENTORY', "SUPPLIER_TYPE", "BASE_SUPPLIER_TYPE",
                                "HASHTAG", "MULTISELECT"]
    validation_msg_dict = {'repeating_name_field': [], "type_mismatch": [], "other_errors": [],
                           "base_booking_fields_mismatch": []}
    is_valid = True
    booking_attributes = booking_template["booking_attributes"]
    base_booking_template_id = booking_template["base_booking_template_id"]
    all_attribute_names = []
    base_booking_template = list(BaseBookingTemplate.objects.raw({'_id': ObjectId(base_booking_template_id)}))
    if len(base_booking_template) == 0:
        is_valid = False
        validation_msg_dict['other_errors'].append("base_booking_template_not_found")
        return is_valid, validation_msg_dict
    base_booking_template = base_booking_template[0]
    booking_attributes_dict = {}
    for single_attribute in booking_attributes:
        if single_attribute['name'] in all_attribute_names:
            is_valid = False
            validation_msg_dict['repeating_name_field'].append(single_attribute['name'])
        if single_attribute['type'] not in possible_attribute_types:
            is_valid = False
            validation_msg_dict['type_mismatch'].append(single_attribute['type'])
        all_attribute_names.append(single_attribute['name'])
        booking_attributes_dict[single_attribute['name']] = single_attribute
    for base_booking_attribute in base_booking_template.booking_attributes:
        if "is_required" in base_booking_attribute:
            if base_booking_attribute["is_required"]:
                if base_booking_attribute["name"] not in booking_attributes_dict:
                    is_valid = False
                    validation_msg_dict["base_booking_fields_mismatch"].append(base_booking_attribute["name"])
                else:
                    if booking_attributes_dict[base_booking_attribute["name"]]["type"] != base_booking_attribute["type"]:
                        is_valid = False
                        validation_msg_dict["base_booking_fields_mismatch"].append(base_booking_attribute["name"])

    return is_valid, validation_msg_dict


