from v0.ui.account.models import ContactDetails
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
import datetime
from v0.ui.gupshup.models import ContactVerification,MessageTemplate
from v0.ui.common.models import mongo_client
from django.db.models import Q
from bson.objectid import ObjectId
import time
import requests
import threading 

ENTITY_CODE = {
    'a':'RS',
    'b':'CO',
    'c':'EI',
    'd':'HL',
}

def mobile_verification(mobile):
    
    if mobile.isnumeric():
        name = ""
        designation = ""
        city = ""
        area = ""
        subarea = ""
        supplier_name = ""
        supplier_type = ""
        data = {}

        contact_verification = mongo_client.ContactVerification.find_one(
            {"mobile":mobile})

        contact_details = ContactDetails.objects.filter(mobile=mobile).first()
        if contact_details:

            designation = contact_details.contact_type
            name = contact_details.name

            supplier_obj = get_supplier_object(contact_details.object_id)
            city = supplier_obj['city']
            area = supplier_obj['area']
            subarea = supplier_obj['subarea']
            supplier_name = supplier_obj['supplier_name']
            supplier_type = supplier_obj['supplier_type']

        if contact_verification:

            contact_verification = dict(contact_verification)
            if contact_details:
                if contact_details.mobile and name and designation and city and \
                    area and subarea and supplier_name:

                    update_data = {"$set":{"verification_status":2,"name":name,
                        "contact_type":designation,"entity_name":supplier_name,"city":city,
                        "entity_type":supplier_type,"updated_at":datetime.datetime.now()}}
                else:

                    update_data = {"$set":{"verification_status":1,"name":name,
                        "contact_type":designation,"entity_name":supplier_name,"city":city,
                        "entity_type":supplier_type,"updated_at":datetime.datetime.now()}}

                update_verification = mongo_client.ContactVerification.update(
                    {"_id":ObjectId(contact_verification['_id'])},update_data)

        else:
            if not contact_details:

                data = {"city":city,"mobile":mobile,"verification_status":0,"user_status": 1,
                    "name":name,"designation":designation,"entity_name":supplier_name,
                    "entity_type":supplier_type,"level":0,"updated_at":datetime.datetime.now()
                    ,"created_at":datetime.datetime.now()}
            else:
                if contact_details.mobile and name and designation and city and \
                    area and subarea and supplier_name:

                    data = {"city":city,"mobile":mobile,"verification_status":2,"user_status":1,
                        "name":name,"designation":designation,"entity_name":supplier_name,
                        "entity_type":supplier_type,"level":0,"updated_at":datetime.datetime.now()
                        ,"created_at":datetime.datetime.now()}
                else:
                    data = {"city":city,"mobile":mobile,"verification_status":1,"user_status":1,
                    "name":name,"designation":designation,"entity_name":supplier_name,
                    "entity_type":supplier_type,"level":0,"updated_at":datetime.datetime.now()
                    ,"created_at":datetime.datetime.now()}

            mongo_client.ContactVerification.insert_one(data)

    return True


def get_template(obj):
    
    template = MessageTemplate.objects.filter(verification_status=
        obj['verification_status']).first()
    
    if template:
        name = obj.get('name')
        designation = obj.get('designation')
        entity_name = obj.get('entity_name')
        string = template.message
        if name:
            string = string.replace("$NAME",name)
        else:
            string = string.replace("$NAME","")

        if designation:
            string = string.replace("$DESIGNATION",designation)
        else:
            string = string.replace("$DESIGNATION","")

        if entity_name:
            string = string.replace("$SUPPLIER_NAME",entity_name)
        else:
            string = string.replace("$SUPPLIER_NAME","")
        
    else:
        string = "Hello, Welcome to Machadalo"
    return string


def get_supplier_object(supplier_id):
    
    supplier = SupplierTypeSociety.objects.filter(supplier_id=
    supplier_id).first()
    context = {}
    city = ""
    area = ""
    subarea = ""
    supplier_name = ""

    if supplier:
        city = supplier.society_city
        area = supplier.society_locality
        subarea = supplier.society_subarea
        supplier_name = supplier.society_name
        supplier_type = "RS"
    else:
        supplier_master = SupplierMaster.objects.filter(supplier_id=
            supplier_id).first()

        if supplier_master:

            city = supplier_master.city
            area = supplier_master.area
            subarea = supplier_master.subarea
            supplier_name = supplier_master.supplier_name
            supplier_type = supplier_type

    context = {
        "supplier_name":supplier_name,
        "city":city,
        "area":area,
        "subarea":subarea,
        "supplier_type":supplier_type
    }

    return context

def get_response_template(obj):

    msg = (obj['message']).lower()
    template = None
    update_dict = {}
    
    if msg == "v" or msg == "verify":

        verification_dict = mongo_client.ContactVerification.find_one(
            {"mobile":obj['mobile']})

        if verification_dict['verification_status'] == 1 or verification_dict['verification_status'] == 0:
            
            if not verification_dict.get('city'):
                template = "Provide your city"
                update_dict = {"$set": {"level": 8,"updated_at":datetime.datetime.now()}}

            if not verification_dict.get('entity_type'):
                template = get_template({"verification_status":"ET"})
                update_dict = {"$set": {"level": 4,"updated_at":datetime.datetime.now()}}

            if not verification_dict.get('designation'):
                template = "Please provide your designation in "+verification_dict['entity_name']
                update_dict = {"$set": {"level": 7,"updated_at":datetime.datetime.now()}}

            if not verification_dict.get('entity_name'):
                template = "Provide your Entity name"
                update_dict = {"$set": {"level": 6,"updated_at":datetime.datetime.now()}}

            if not verification_dict.get('name'):
                template = "Provide your name"
                update_dict = {"$set": {"level": 5,"updated_at":datetime.datetime.now()}}

    if msg == "m" or msg == "main" or \
        msg == "main menu" or msg == "menu":
        verification_status = 8
        template = "Please select your service"

    if update_dict:
        mongo_client.ContactVerification.update({"_id": 
            verification_dict['_id']},update_dict)

    return template

def get_response_template_without_verify(obj):

    msg = (obj['message']).lower()
    template = None
    update_dict = {}

    verification_dict = mongo_client.ContactVerification.find_one(
        {"mobile":obj['mobile']})

    if verification_dict['verification_status'] == 1 or verification_dict['verification_status'] == 0:
        
        if not verification_dict.get('city'):
            template = "Provide your city"
            update_dict = {"$set": {"level": 8,"updated_at":datetime.datetime.now()}}

        if not verification_dict.get('entity_type'):
            template = get_template({"verification_status":"ET"})
            update_dict = {"$set": {"level": 4,"updated_at":datetime.datetime.now()}}

        if not verification_dict.get('designation'):
            template = "Please provide your designation in "+verification_dict['entity_name']
            update_dict = {"$set": {"level": 7,"updated_at":datetime.datetime.now()}}

        if not verification_dict.get('entity_name'):
            template = "Provide your Entity name"
            update_dict = {"$set": {"level": 6,"updated_at":datetime.datetime.now()}}

        if not verification_dict.get('name'):
            template = "Provide your name"
            update_dict = {"$set": {"level": 5,"updated_at":datetime.datetime.now()}}

    if update_dict:
        mongo_client.ContactVerification.update({"_id": 
            verification_dict['_id']},update_dict)

    return template

def save_response(obj):
    
    if obj['level'] == 4:

        if obj['text']:
            entity_type = ENTITY_CODE.get(obj['text'].lower())

        mongo_client.ContactVerification.update(
            {"_id": obj['_id']},{"$set":{"entity_type":obj['text'],"entity_type":entity_type,
            "updated_at":datetime.datetime.now()}})

    if obj['level'] == 5:

        mongo_client.ContactVerification.update(
            {"_id": obj['_id']},{"$set":{"name":obj['text'],
            "updated_at":datetime.datetime.now()}})

    if obj['level'] == 6:

        mongo_client.ContactVerification.update(
            {"_id": obj['_id']},{"$set":{"entity_name":obj['text'],
            "updated_at":datetime.datetime.now()}})

    if obj['level'] == 7:

        mongo_client.ContactVerification.update(
            {"_id": obj['_id']},{"$set":{"designation":obj['text'],
            "updated_at":datetime.datetime.now()}})

    if obj['level'] == 8:

        mongo_client.ContactVerification.update(
            {"_id": obj['_id']},{"$set":{"city":obj['text'],
            "updated_at":datetime.datetime.now()}})

    verify = mongo_client.ContactVerification.find_one({"_id": obj['_id']})
    if verify:
        if verify.get('entity_type') and verify.get('city') and \
            verify.get('designation') and verify.get('name') and verify.get('entity_name'):

            mongo_client.ContactVerification.update(
                {"_id": obj['_id']},{"$set":{"verification_status":2,
                "updated_at":datetime.datetime.now()}})

    return True

def update_supplier_details(obj):
    
    mobile = obj.get("mobile")
    name = obj.get("name")
    city = obj.get("city")
    designation = obj.get("designation")
    supplier_name = obj.get("entity_name")
    supplier_type = obj.get("entity_type")

    if mobile:
        contact_details = ContactDetails.objects.filter(mobile=mobile)
        if contact_details:
            supplier_id = []
            for contact in contact_details:
                supplier_id.append(contact.object_id)
            if supplier_type == "RS":
                supplier = SupplierTypeSociety.objects.filter(
                    supplier_id__in=supplier_id).first()

                if supplier:
                    supplier.society_name = supplier_name
                    supplier.society_city = city
                    supplier.save()

                    contact_data = contact_details.get(object_id = supplier.supplier_id)
                    contact_data.name = name
                    contact_data.contact_type = designation
                    contact_data.save()

            else:
                supplier_master = SupplierMaster.objects.filter(
                    supplier_id__in=supplier_id, supplier_type=entity_type).first()
                if supplier_master:
                    supplier_master = SupplierTypeSociety(
                    supplier_name=supplier_name,
                    city=city,
                    )
                    supplier_master.save()

    return True

def send_message_to_gupshup():
  
    time.sleep(120)
    URL = "https://api.gupshup.io/sm/api/v1/msg"
    # obj = threading.current_thread().obj
    template = MessageTemplate.objects.filter(verification_status="WR").first()
    if template:

        mobile = "919713198098"
        message = template.message
        print("##########")
        params = {
                "channel" : "whatsapp",
                "source" : "917834811114",
                "destination" : mobile,
                "src.name":"TestMachadalo",
                "message" : message
            }

        headers = {'Content-Type': 'application/x-www-form-urlencoded','apikey':"gb4safxmjwlppbs4h9ssnjramaluzjke"}
        response = requests.post(URL, data=params, headers=headers)
        print(response.text)
        return response.text

def waiting_response(obj):
    # time.sleep(5)
    # Event.wait(5)
    print("$$$$$$$$$$$")
    t = threading.Thread(target=send_message_to_gupshup)
    print(t)

    t.start()
    return t
    # response = send_message_to_gupshup(obj)

    