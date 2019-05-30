from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import *
from bson.objectid import ObjectId
from datetime import datetime


class State(APIView):
    @staticmethod
    def post(request):
        state_name = request.data['state_name'] if 'state_name' in request.data else None
        state_code = request.data['state_code'] if 'state_code' in request.data else None
        dict_of_req_attributes = {"state_name": state_name, "state_code": state_code}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)

        state_dict = dict_of_req_attributes

        StateDetails(**state_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_states= StateDetails.objects.all()
        all_state_dict = {}
        for state in all_states:
            all_state_dict[str(state._id)] = {
                "id": str(state._id),
                "state_name": state.state_name,
                "state_code": state.state_code,
            }
        return handle_response('', data=all_state_dict, success=True)


class StateById(APIView):
    @staticmethod
    def get(request, state_id):
        stateId = StateDetails.objects.raw({'_id':ObjectId(state_id)})[0]
        stateId = {
            "id": str(stateId._id),
            "state_name": str(stateId.state_name),
            "state_code": stateId.state_code,
        }
        return handle_response('', data=stateId, success=True)


    @staticmethod
    def put(request, state_id):
        state_name = request.data['state_name'] if 'state_name' in request.data else None
        state_code = request.data['state_code'] if 'state_code' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"state_name": state_name, "state_code": state_code, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        state_dict = dict_of_req_attributes
        state_dict['updated_at'] = datetime.now()

        StateDetails.objects.raw({'_id': ObjectId(state_id)}).update({"$set": state_dict})
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def delete(request, state_id):
        exist_state_query = StateDetails.objects.raw({'_id': ObjectId(state_id)})[0]
        exist_state_query.delete()
        return handle_response('', data="success", success=True)


class City(APIView):
    @staticmethod
    def post(request):
        city_name = request.data['city_name'] if 'city_name' in request.data else None
        city_code = request.data['city_code'] if 'city_code' in request.data else None
        state_code = request.data['state_code'] if 'state_code' in request.data else None
        dict_of_req_attributes = {"city_name": city_name, "city_code": city_code, "state_code":state_code}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)

        city_dict = dict_of_req_attributes

        CityDetails(**city_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_cities= CityDetails.objects.all()
        all_cities_dict = {}
        for city in all_cities:
            all_cities_dict[str(city._id)] = {
                "id": str(city._id),
                "city_name": city.city_name,
                "city_code": city.city_code,
                "state_code": city.state_code,
            }
        return handle_response('', data=all_cities_dict, success=True)


class CityById(APIView):
    @staticmethod
    def get(request, city_id):
        cityId = CityDetails.objects.raw({'_id':ObjectId(city_id)})[0]
        cityId = {
            "id": str(cityId._id),
            "city_name": str(cityId.city_name),
            "city_code": cityId.city_code,
            "state_code": cityId.state_code,
        }
        return handle_response('', data=cityId, success=True)


    @staticmethod
    def put(request, city_id):
        city_name = request.data['city_name'] if 'city_name' in request.data else None
        city_code = request.data['city_code'] if 'city_code' in request.data else None
        state_code = request.data['state_code'] if 'state_code' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"city_name": city_name,"city_code":city_code, "state_code": state_code, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        city_dict = dict_of_req_attributes
        city_dict['updated_at'] = datetime.now()

        CityDetails.objects.raw({'_id': ObjectId(city_id)}).update({"$set": city_dict})
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def delete(request, city_id):
        exist_city_query = CityDetails.objects.raw({'_id': ObjectId(city_id)})[0]
        exist_city_query.delete()
        return handle_response('', data="success", success=True)


class Area(APIView):
    @staticmethod
    def post(request):
        label = request.data['label'] if 'label' in request.data else None
        area_code = request.data['area_code'] if 'area_code' in request.data else None
        city_code = request.data['city_code'] if 'city_code' in request.data else None
        dict_of_req_attributes = {"label": label, "area_code": area_code, "city_code":city_code}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)

        area_dict = dict_of_req_attributes

        CityAreaDetails(**area_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_areas= CityAreaDetails.objects.all()
        all_areas_dict = {}
        for area in all_areas:
            all_areas_dict[str(area._id)] = {
                "id": str(area._id),
                "label": area.label,
                "area_code": area.area_code,
                "city_code": area.city_code,
            }
        return handle_response('', data=all_areas_dict, success=True)


class AreaById(APIView):
    @staticmethod
    def get(request, area_id):
        areaId = CityAreaDetails.objects.raw({'_id':ObjectId(area_id)})[0]
        areaId = {
            "id": str(areaId._id),
            "label": str(areaId.label),
            "area_code": areaId.area_code,
            "city_code": areaId.city_code,
        }
        return handle_response('', data=areaId, success=True)


    @staticmethod
    def put(request, area_id):
        label = request.data['label'] if 'label' in request.data else None
        area_code = request.data['area_code'] if 'area_code' in request.data else None
        city_code = request.data['city_code'] if 'city_code' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"label": label, "area_code": area_code, "city_code":city_code, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        area_dict = dict_of_req_attributes
        area_dict['updated_at'] = datetime.now()

        CityAreaDetails.objects.raw({'_id': ObjectId(area_id)}).update({"$set": area_dict})
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def delete(request, area_id):
        exist_area_query = CityAreaDetails.objects.raw({'_id': ObjectId(area_id)})[0]
        exist_area_query.delete()
        return handle_response('', data="success", success=True)


class SubArea(APIView):
    @staticmethod
    def post(request):
        subarea_name = request.data['subarea_name'] if 'subarea_name' in request.data else None
        subarea_code = request.data['subarea_code'] if 'subarea_code' in request.data else None
        locality_rating = request.data['locality_rating'] if 'locality_rating' in request.data else None
        area_code = request.data['area_code'] if 'area_code' in request.data else None
        dict_of_req_attributes = {"subarea_name": subarea_name, "subarea_code": subarea_code, "locality_rating":locality_rating, "area_code":area_code}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)

        sub_area_dict = dict_of_req_attributes

        CitySubAreaDetails(**sub_area_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_sub_areas= CitySubAreaDetails.objects.all()
        all_sub_areas_dict = {}
        for sub_area in all_sub_areas:
            all_sub_areas_dict[str(sub_area._id)] = {
                "id": str(sub_area._id),
                "subarea_name": sub_area.subarea_name,
                "subarea_code": sub_area.subarea_code,
                "locality_rating": sub_area.locality_rating,
                "area_code": sub_area.area_code,
            }
        return handle_response('', data=all_sub_areas_dict, success=True)


class SubAreaById(APIView):
    @staticmethod
    def get(request, sub_area_id):
        subAreaId = CitySubAreaDetails.objects.raw({'_id':ObjectId(sub_area_id)})[0]
        subAreaId = {
            "id": str(subAreaId._id),
            "subarea_name": str(subAreaId.subarea_name),
            "subarea_code": subAreaId.subarea_code,
            "locality_rating": subAreaId.locality_rating,
            "area_code": subAreaId.area_code,
        }
        return handle_response('', data=subAreaId, success=True)


    @staticmethod
    def put(request, sub_area_id):
        subarea_name = request.data['subarea_name'] if 'subarea_name' in request.data else None
        subarea_code = request.data['subarea_code'] if 'subarea_code' in request.data else None
        locality_rating = request.data['locality_rating'] if 'locality_rating' in request.data else None
        area_code = request.data['area_code'] if 'area_code' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"subarea_name": subarea_name, "subarea_code": subarea_code, "locality_rating":locality_rating, "area_code":area_code, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        sub_area_dict = dict_of_req_attributes
        sub_area_dict['updated_at'] = datetime.now()

        CitySubAreaDetails.objects.raw({'_id': ObjectId(sub_area_id)}).update({"$set": sub_area_dict})
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def delete(request, sub_area_id):
        exist_sub_area_query = CitySubAreaDetails.objects.raw({'_id': ObjectId(sub_area_id)})[0]
        exist_sub_area_query.delete()
        return handle_response('', data="success", success=True)
