from v0.ui.account.models import ContactDetails
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
import datetime
from v0.ui.gupshup.models import ContactVerification,MessageTemplate
from v0.ui.common.models import mongo_client
from django.db.models import Q
from bson.objectid import ObjectId


def mobile_verification(mobile):
    
    if mobile.isnumeric():
        name = ""
        designation = ""
        city = ""
        area = ""
        subarea = ""
        supplier_name = ""
        data = {}

        contact_verification = mongo_client.ContactVerification.find_one(
            {"mobile":mobile})
        contact_details = ContactDetails.objects.filter(mobile=mobile).first()
        if contact_details:
            print(2)
            supplier = SupplierTypeSociety.objects.filter(supplier_id=
            contact_details.object_id).first()
            if supplier:

                city = supplier.society_city
                area = supplier.society_locality
                subarea = supplier.society_subarea
                supplier_name = supplier.society_name
            else:
                supplier_master = SupplierMaster.objects.filter(supplier_id=
                    contact_details.object_id).first()

                if supplier_master:

                    city = supplier_master.city
                    area = supplier_master.area
                    subarea = supplier_master.subarea
                    supplier_name = supplier_master.supplier_name

        if contact_verification and contact_details:
            print(3)
            name = contact_details.name
            designation = contact_details.contact_type
            
            if contact_details.mobile and name and designation and city and \
                area and subarea and supplier_name:

                contact_verification = dict(contact_verification)
                update_dict = {"$set":
                    {"verification_status":2,
                    "name":name,
                    "contact_type":designation,
                    "entity_name":supplier_name}
                    }
                
                update_verification = mongo_client.ContactVerification.update(
                    {"_id":ObjectId(contact_verification['_id'])},update_dict)

        elif not contact_verification and contact_details:
            print(4)

            name = contact_details.name
            designation = contact_details.contact_type

            if contact_details.mobile and name and designation and city and \
                area and subarea and supplier_name:

                data = {
                    "mobile":mobile,
                    "verification_status":2,
                    "user_status":1,
                    "name":name,
                    "designation":designation,
                    "entity_name":supplier_name
                }
            else:
                data = {
                    "mobile":mobile,
                    "verification_status":1,
                    "user_status":1,
                    "name":name,
                    "designation":designation,
                    "entity_name":supplier_name
                }
        else:
            print(5)
            data = {
                "mobile":mobile,
                "verification_status":0,
                "user_status": 1,
                "name":name,
                "designation":designation,
                "entity_name":supplier_name
            }
    if data:
        mongo_client.ContactVerification.insert_one(data)

    return True


def get_template(obj):
    
    template = MessageTemplate.objects.filter(verification_status=
        obj['verification_status']).first()
    
    if template:
        name = obj['name']
        designation = obj['designation']
        entity_name = obj['entity_name']
        string = template.message

        string = string.replace("$NAME",name)
        string = string.replace("$DESIGNATION",designation)
        string = string.replace("$SUPPLIER_NAME",entity_name)
    else:
        string = "Hello, Welcome to Machadalo"
    return string
