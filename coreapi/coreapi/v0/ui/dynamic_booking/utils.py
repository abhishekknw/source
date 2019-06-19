from __future__ import absolute_import
from validate_email import validate_email
from datetime import datetime
from .models import BaseBookingTemplate, BookingTemplate, BookingData
from bson.objectid import ObjectId
from v0.ui.dynamic_suppliers.models import SupplySupplier


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


def get_dynamic_booking_data_by_campaign(campaign_id):
    data_all = list(BookingData.objects.raw({'campaign_id': campaign_id}))
    if not data_all or not len(data_all):
        return []
    booking_template_id = data_all[0].booking_template_id
    booking_template = BookingTemplate.objects.raw({"_id": ObjectId(booking_template_id)})[0]
    final_data_list = []
    for data in data_all:
        final_data = {}
        final_data['booking_attributes'] = data.booking_attributes
        final_data['comments'] = data.comments
        final_data['inventory_counts'] = data.inventory_counts
        final_data['phase_id'] = data.phase_id
        (final_data['supplier_attributes'], final_data['additional_attributes']) = get_supplier_attributes(
            data.supplier_id, booking_template.supplier_attributes)
        final_data['supplier_id'] = data.supplier_id
        final_data['organisation_id'] = data.organisation_id
        final_data['campaign_id'] = data.campaign_id
        final_data['booking_template_id'] = data.booking_template_id
        final_data['id'] = str(data._id)
        final_data_list.append(final_data)
    return final_data_list


def get_supplier_attributes(supplier_id, supplier_attributes):
    all_supplier_attribute_names = [supplier['name'] for supplier in supplier_attributes]
    supplier_object_list = list(SupplySupplier.objects.raw({"_id": ObjectId(supplier_id)}))
    if not len(supplier_object_list):
        return []
    supplier_object = supplier_object_list[0]
    final_attributes = []
    additional_attributes = supplier_object.additional_attributes if hasattr(supplier_object,
                                                                             "additional_attributes") else None
    for supplier in supplier_object.supplier_attributes:
        if supplier['name'] in all_supplier_attribute_names:
            final_attributes.append(supplier)
    return (final_attributes, additional_attributes)
