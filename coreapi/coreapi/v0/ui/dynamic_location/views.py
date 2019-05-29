from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import State

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

        State(**state_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_state= State.objects.all()
        all_state_dict = {}
        for state in all_state:
            all_state_dict[str(state._id)] = {
                "id": str(state._id),
                "state_name": state.state_name,
                "state_code": state.state_code,
            }
        return handle_response('', data=all_state_dict, success=True)
