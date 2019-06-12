from __future__ import absolute_import
import os
import time
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import (BaseBookingTemplate, BookingTemplate, BookingData, BookingDetails, BookingInventoryActivity,
                     BookingInventory)
from datetime import datetime
from bson.objectid import ObjectId
from .utils import validate_booking, get_dynamic_booking_data_by_campaign, get_supplier_attributes

from v0.ui.dynamic_suppliers.models import SupplySupplier
import boto3
import v0.ui.utils as ui_utils
from django.conf import settings

from v0.ui.proposal.views import upload_hashtag_images
from v0.ui.proposal.models import ProposalInfo
from v0.ui.website.utils import (get_address_from_lat_long, add_string_to_image)



class BaseBookingTemplateView(APIView):
    @staticmethod
    def post(request):

        name = request.data['name'] if 'name' in request.data else None
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        supplier_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        base_supplier_type_id = request.data['base_supplier_type_id'] if 'base_supplier_type_id' in request.data else None
        dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes,
                                  "booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "base_supplier_type_id": base_supplier_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:

            return handle_response('', data=validation_msg_dict, success=None)

        base_booking_template = dict_of_req_attributes
        base_booking_template["created_at"] = datetime.now()
        BaseBookingTemplate(**base_booking_template).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        data_all = BaseBookingTemplate.objects.raw({})
        final_data_list = []
        for data in data_all:
            final_data = {}
            final_data['booking_attributes'] = data.booking_attributes
            final_data['supplier_attributes'] = data.supplier_attributes
            final_data['name'] = data.name if 'name' in data else None
            final_data['base_supplier_type_id'] = data.base_supplier_type_id
            final_data['organisation_id'] = data.organisation_id
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)


class BaseBookingTemplateById(APIView):
    @staticmethod
    def get(request, base_booking_template_id):
        base_booking_supplier_type = BaseBookingTemplate.objects.raw({'_id': ObjectId(base_booking_template_id)})[0]
        base_booking_supplier_type = {
            "id": str(base_booking_supplier_type._id),
            "base_supplier_type_id": str(base_booking_supplier_type.base_supplier_type_id),
            "name": base_booking_supplier_type.name,
            "supplier_attributes": base_booking_supplier_type.supplier_attributes,
            "booking_attributes": base_booking_supplier_type.booking_attributes,
            "organisation_id": base_booking_supplier_type.organisation_id
        }
        return handle_response('', data=base_booking_supplier_type, success=True)

    @staticmethod
    def put(request, base_booking_template_id):
        data = request.data.copy()
        data['updated_at'] = datetime.now()
        BaseBookingTemplate.objects.raw({'_id': ObjectId(base_booking_template_id)}).update({"$set": data})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request, base_booking_template_id):
        exist_query = BaseBookingTemplate.objects.raw({'_id': ObjectId(base_booking_template_id)})
        exist_query.delete()
        return handle_response('', data="success", success=True)


class BookingTemplateView(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else None
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        supplier_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        base_booking_template_id = request.data['base_booking_template_id'] if 'base_booking_template_id' in request.data else None
        supplier_type_id = request.data['supplier_type_id'] if 'supplier_type_id' in request.data else None
        dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes,
                                  "booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "base_booking_template_id": base_booking_template_id,
                                  "supplier_type_id": supplier_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:

            return handle_response('', data=validation_msg_dict, success=False)
        booking_template = dict_of_req_attributes
        booking_template["created_at"] = datetime.now()
        is_valid_adv, validation_msg_dict_adv = validate_booking(booking_template)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        BookingTemplate(**booking_template).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        organisation_id = get_user_organisation_id(request.user)
        data_all = BookingTemplate.objects.raw({'organisation_id':organisation_id})
        final_data_list = []
        for data in data_all:
            final_data = {}
            final_data['booking_attributes'] = data.booking_attributes
            final_data['supplier_attributes'] = data.supplier_attributes
            final_data['name'] = data.name if 'name' in data else None
            final_data['supplier_type_id'] = data.supplier_type_id
            final_data['organisation_id'] = data.organisation_id
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)


class BookingTemplateById(APIView):
    @staticmethod
    def get(request, booking_template_id):
        booking_supplier_type = BookingTemplate.objects.raw({'_id': ObjectId(booking_template_id)})[0]
        booking_supplier_type = {
            "id": str(booking_supplier_type._id),
            "supplier_type_id": str(booking_supplier_type.supplier_type_id),
            "name": booking_supplier_type.name,
            "supplier_attributes": booking_supplier_type.supplier_attributes,
            "booking_attributes": booking_supplier_type.booking_attributes,
            "organisation_id": booking_supplier_type.organisation_id

        }
        return handle_response('', data=booking_supplier_type, success=True)

    @staticmethod
    def put(request, booking_template_id):
        data = request.data.copy()
        data['updated_at'] = datetime.now()
        BookingTemplate.objects.raw({'_id': ObjectId(booking_template_id)}).update({"$set": data})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request, booking_template_id):
        exist_query = BookingTemplate.objects.raw({'_id': ObjectId(booking_template_id)})
        exist_query.delete()
        return handle_response('', data="success", success=True)


def create_inventories(inventory_counts, supplier_id, campaign_id):
    for inventory in inventory_counts:
        for _ in range(inventory["count"]):
            BookingInventory(**{
                "supplier_id": supplier_id,
                "inventory_name": inventory["name"],
                "campaign_id": campaign_id,
                "created_at": datetime.now()
            }).save()


class BookingDataView(APIView):
    @staticmethod
    def post(request):
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None

        data_old_all = BookingData.objects.raw({'campaign_id': campaign_id})
        data_old = None
        if data_old_all and len(list(data_old_all)) > 0:
            data_old = data_old_all[0]
        if data_old:
            old_supplier_id = data_old.supplier_id if 'supplier_id' in data_old else None
            old_booking_template_id= data_old.booking_template_id if 'booking_template_id' in data_old else None

        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        comments = request.data['comments'] if 'comments' in request.data else None
        phase_id = int(request.data['phase_id']) if 'phase_id' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        supplier_id = request.data['supplier_id'] if 'supplier_id' in request.data else None
        inventory_counts = request.data['inventory_counts'] if 'inventory_counts' in request.data else None
        if inventory_counts:
            create_inventories(inventory_counts, supplier_id, campaign_id)
        if data_old:
            if old_supplier_id == supplier_id:
                return handle_response('', data="supplier_id already exist", success=None)

        booking_template_id = request.data['booking_template_id'] if 'booking_template_id' in request.data else None
        if data_old:
            if old_booking_template_id != booking_template_id:
                return handle_response('', data="booking_template_id must be same for same campaign_id", success=None)

        dict_of_req_attributes = {"booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "supplier_id": supplier_id, "campaign_id": campaign_id, "booking_template_id": booking_template_id}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=None)
        booking_data = dict_of_req_attributes
        booking_data["created_at"] = datetime.now()
        if comments:
            booking_data["comments"] = comments
        if inventory_counts:
            booking_data["inventory_counts"] = inventory_counts
        if phase_id:
            booking_data["phase_id"] = phase_id
        BookingData(**booking_data).save()
        return handle_response('', data={"success": True}, success=True)


class BookingDataById(APIView):
    @staticmethod
    def get(request, booking_data_id):
        data = BookingData.objects.raw({'_id': ObjectId(booking_data_id)})[0]
        booking_template_id = data.booking_template_id
        booking_template = BookingTemplate.objects.raw({"_id": ObjectId(booking_template_id)})[0]
        final_data = dict()
        final_data['booking_attributes'] = data.booking_attributes
        final_data['comments'] = data.comments
        final_data['inventory_counts'] = data.inventory_counts
        final_data['phase_id'] = data.phase_id
        final_data['supplier_attributes'] = get_supplier_attributes(data.supplier_id, booking_template.supplier_attributes)
        final_data['name'] = data.name if 'name' in data else None
        final_data['supplier_id'] = data.supplier_id
        final_data['organisation_id'] = data.organisation_id
        final_data['campaign_id'] = data.campaign_id
        final_data['booking_template_id'] = data.booking_template_id
        final_data['id'] = str(data._id)
        return handle_response('', data=final_data, success=True)

    @staticmethod
    def put(request, booking_data_id):
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        comments = request.data['comments'] if 'comments' in request.data else None
        inventory_counts = request.data['inventory_counts'] if 'inventory_counts' in request.data else None
        phase_id = request.data['phase_id'] if 'phase_id' in request.data else None
        update_dict = {}
        if booking_attributes:
            update_dict["booking_attributes"] = booking_attributes
        if comments:
            update_dict["comments"] = comments
        if phase_id:
            update_dict["phase_id"] = phase_id
        update_dict["updated_at"] = datetime.now()
        BookingData.objects.raw({'_id': ObjectId(booking_data_id)}).update({"$set": update_dict})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request, booking_data_id):
        exist_query = BookingData.objects.raw({'_id': ObjectId(booking_data_id)})
        inventories = BookingInventory.objects.raw({"campaign_id": exist_query[0].campaign_id,
                                        "supplier_id": exist_query[0].supplier_id})
        inventories.delete()
        exist_query.delete()
        return handle_response('', data="success", success=True)


class BookingDataByCampaignId(APIView):
    @staticmethod
    def get(request, campaign_id):
        final_data_list = get_dynamic_booking_data_by_campaign(campaign_id)
        return handle_response('', data=final_data_list, success=True)

    @staticmethod
    def delete(request, campaign_id):
        exist_query = BookingData.objects.raw({'campaign_id': campaign_id})
        exist_query.delete()
        return handle_response('', data="success", success=True)


class BookingDetailsView(APIView):
    @staticmethod
    def post(request):
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        booking_template_id = request.data['booking_template_id'] if 'booking_template_id' in request.data else None

        dict_of_req_attributes = {"organisation_id": organisation_id, "campaign_id": campaign_id,
                                  "booking_template_id": booking_template_id}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=None)
        booking_data = dict_of_req_attributes
        booking_data["created_at"] = datetime.now()
        BookingDetails(**booking_data).save()
        return handle_response('', data={"success": True}, success=True)


class BookingDetailsById(APIView):
    @staticmethod
    def get(request, booking_details_id):
        data = BookingDetails.objects.raw({'_id': ObjectId(booking_details_id)})[0]
        final_data = dict()
        final_data['organisation_id'] = data.organisation_id
        final_data['campaign_id'] = data.campaign_id
        final_data['booking_template_id'] = data.booking_template_id
        final_data['id'] = str(data._id)
        return handle_response('', data=final_data, success=True)

    @staticmethod
    def delete(request, booking_details_id):
        exist_query = BookingDetails.objects.raw({'_id': ObjectId(booking_details_id)})
        exist_query.delete()
        return handle_response('', data="success", success=True)


class BookingDetailsByCampaignId(APIView):
    @staticmethod
    def get(request, campaign_id):
        data = BookingDetails.objects.raw({'campaign_id': campaign_id})[0]
        final_data = dict()
        final_data['organisation_id'] = data.organisation_id
        final_data['campaign_id'] = data.campaign_id
        final_data['booking_template_id'] = data.booking_template_id
        final_data['id'] = str(data._id)
        return handle_response('', data=final_data, success=True)


class BookingInventoryView(APIView):
    @staticmethod
    def get(request, campaign_id):
        all_inventories = BookingInventory.objects.raw({'campaign_id': campaign_id})
        list_of_inventory_dicts = list()
        for inventory in all_inventories:
            final_data = dict()
            final_data['supplier_id'] = inventory.supplier_id
            final_data['campaign_id'] = inventory.campaign_id
            final_data['inventory_name'] = inventory.inventory_name
            final_data['comments'] = inventory.comments
            final_data['inventory_images'] = inventory.inventory_images
            final_data['created_at'] = inventory.created_at
            final_data['id'] = str(inventory._id)
            list_of_inventory_dicts.append(final_data)
        return handle_response('', data=list_of_inventory_dicts, success=True)


class BookingAssignmentView(APIView):
    @staticmethod
    def post(request):
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None
        inventory_name = request.data['inventory_name'] if 'inventory_name' in request.data else None
        supplier_id = request.data['supplier_id'] if 'supplier_id' in request.data else None
        activity_list = request.data['activity_list'] if 'activity_list' in request.data else None
        all_booking_inventories = BookingInventory.objects.raw({"campaign_id": campaign_id,
                                                                "inventory_name": inventory_name,
                                                                "supplier_id": supplier_id})
        all_booking_inventory_ids = [booking_inventory._id for booking_inventory in all_booking_inventories]
        for booking_inventory_id in all_booking_inventory_ids:
            for activity in activity_list:
                assigned_to_id = activity['assigned_to_id'] if 'assigned_to_id' in activity else None
                activity_type = activity['activity_type'] if 'activity_type' in activity else None
                activity_date = activity['activity_date'] if 'activity_date' in activity else None
                comments = request.data['comments'] if 'comments' in request.data else None
                inventory_images = request.data['inventory_images'] if 'inventory_images' in request.data else None
                dict_of_req_attributes = {"booking_inventory_id": booking_inventory_id, "assigned_to_id": assigned_to_id,
                                          "activity_type": activity_type, "activity_date": activity_date,
                                          "campaign_id": campaign_id, "inventory_name": inventory_name,
                                          "supplier_id": supplier_id}

                (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
                if not is_valid:
                    return handle_response('', data=validation_msg_dict, success=None)
                booking_assignment = dict_of_req_attributes
                booking_assignment["comments"] = comments
                booking_assignment["inventory_images"] = inventory_images
                BookingInventoryActivity(**booking_assignment).save()
        return handle_response('', data={"success": True}, success=True)


class BookingAssignmentByCampaignId(APIView):
    @staticmethod
    def get(request, campaign_id):
        data_all = list(BookingInventoryActivity.objects.raw({'campaign_id': campaign_id}))
        final_data_list = []
        for data in data_all:
            final_data = {}
            final_data['booking_inventory_id'] = data.booking_inventory_id
            final_data['inventory_name'] = data.inventory_name
            final_data['supplier_id'] = data.supplier_id
            final_data['assigned_to_id'] = data.assigned_to_id
            final_data['activity_type'] = data.activity_type
            final_data['activity_date'] = data.activity_date
            final_data['actual_activity_date'] = data.actual_activity_date
            final_data['status'] = data.status
            final_data['comments'] = data.comments
            final_data['inventory_images'] = data.inventory_images
            final_data['organisation_id'] = data.organisation_id
            final_data['created_at'] = data.created_at
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)


    @staticmethod
    def put(request, campaign_id):
        supplier_id = request.data['supplier_id'] if 'supplier_id' in request.data else None
        inventory_name = request.data['inventory_name'] if 'inventory_name' in request.data else None
        activity_list = request.data['activity_list'] if 'activity_list' in request.data else None
        for activity in activity_list:
            assigned_to_id = activity['assigned_to_id'] if 'assigned_to_id' in activity else None
            activity_type = activity['activity_type'] if 'activity_type' in activity else None
            activity_date = activity['activity_date'] if 'activity_date' in activity else None
            status = activity['status'] if 'status' in activity else None
            comments = activity['comments'] if 'comments' in activity else None
            update_dict = {}
            if assigned_to_id:
                update_dict["assigned_to_id"] = assigned_to_id
            if activity_type:
                update_dict["activity_type"] = activity_type
            if activity_date:
                update_dict["activity_date"] = activity_date
            if status:
                update_dict["status"] = status
            if comments:
                update_dict["comments"] = comments
            update_dict["updated_at"] = datetime.now()
            BookingInventoryActivity.objects.raw({"campaign_id": campaign_id,"inventory_name": inventory_name,
                                                  "supplier_id": supplier_id}).update({"$set": update_dict})
        return handle_response('', data={"success": True}, success=True)


class UploadInventoryActivityImageGeneric(APIView):
    """
    This API first attempts to upload the given image to amazon and saves path in inventory activity image table.
    """

    def post(self, request):
        """
        API to upload inventory activity image amazon
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            file = request.data['file']
            extension = file.name.split('.')[-1]
            supplier_name = request.data['supplier_name'].replace(' ', '_')
            activity_type = request.data['activity_type']
            activity_date = request.data['activity_date']
            inventory_name = request.data['inventory_name']
            actual_activity_date = request.data['actual_activity_date']
            new_comment = request.data['comment']
            lat = None
            long = None
            address = None
            if 'lat' in request.data:
                lat = request.data['lat']
                long = request.data['long']
                address = get_address_from_lat_long(lat, long)
                image_string = lat + ", " +long + " " + address + " " + actual_activity_date
                file_address = add_string_to_image(file, image_string)
            file_name = supplier_name + '_' + inventory_name + '_' + activity_type + '_' + activity_date.replace('-',
                                                                                                                 '_') + '_' + str(
                time.time()).replace('.', '_') + '.' + extension
            booking_inventory_activity_id = request.data['booking_inventory_activity_id']
            existing_booking_activity = list(BookingInventoryActivity.objects.raw({'_id': ObjectId(booking_inventory_activity_id)}))
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            with open(file_address, 'rb') as f:
                contents = f.read()
                s3.put_object(Body=contents, Bucket=settings.ANDROID_BUCKET_NAME, Key=file_name)
                os.unlink(file_address)
                existing_images = existing_booking_activity[0].inventory_images
                existing_comments = existing_booking_activity[0].comments
                update_dict = {}
                if not existing_images:
                    existing_images = []
                existing_images.append({
                    "image_path": file_name,
                    "bucket_name": settings.ANDROID_BUCKET_NAME,
                    "lat": lat,
                    "long": long,
                    "address": address
                })
                update_dict["inventory_images"] = existing_images
                if new_comment:
                    if not existing_comments:
                        existing_comments = []
                    existing_comments.append({
                        "comment": new_comment,
                        "timestamp": datetime.now()
                    })
                    update_dict["comments"] = existing_comments
                update_dict["actual_activity_date"] = actual_activity_date
                BookingInventoryActivity.objects.raw({'_id': ObjectId(booking_inventory_activity_id)}).update({"$set": update_dict})
            return ui_utils.handle_response(class_name, data=file_name, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

class UploadHashTagImage(APIView):

    def post(self, request, booking_data_id):
        data = request.data
        supplier = SupplySupplier.objects.raw({'_id': ObjectId(data['supplier_id'])})
        campaign = ProposalInfo.objects.get(proposal_id=data['campaign_id'])
        if supplier.count() > 0 and data['file']:
            hashtag_data = {
                "file": data['file'],
                "hashtag": data['hashtag'],
                "comment": data['comment'] if data['comment'] else None,
                "supplier_name": supplier[0].name,
                "campaign_name": campaign.name,
                "supplier_id": data['supplier_id'],
                "campaign_id": data['campaign_id']
            }
            response = upload_hashtag_images(hashtag_data)
            image_data = {
                "image_path": response.data['data']['image_path'],
                "hashtag": response.data['data']['hashtag'],
                "comment": response.data['data']['comment']
            }
            booking_data = BookingData.objects.raw({'_id': ObjectId(booking_data_id)})
            if booking_data.count() > 0:
                new_booking_attributes = booking_data[0].booking_attributes
                for booking in new_booking_attributes:
                    if data['name'] == booking['name']:
                        if 'files' not in booking:
                            booking['files'] = []
                        booking['files'].append(image_data)
                        BookingData.objects.raw({'_id': ObjectId(booking_data_id)}). \
                            update({"$set": {"booking_attributes": new_booking_attributes}})
                        break
            return ui_utils.handle_response('', data={}, success=True)
        return ui_utils.handle_response('', data="Supplier or File Not found", success=False)