from __future__ import print_function
from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg, is_user_permitted
from celery import shared_task
from v0.ui.common.models import mongo_client, mongo_test
from bson.objectid import ObjectId
import datetime
import collections
from operator import itemgetter
from .models import ChecklistPermissions, ChecklistData, ChecklistOperators
from v0.ui.campaign.models import CampaignAssignment
from v0.ui.proposal.models import ProposalInfo
from v0.ui.common.models import BaseUser
from v0.ui.user.serializers import BaseUserSerializer
import numpy as np
from bson import Binary, Code
from bson.json_util import dumps
from v0.ui.notifications.views import create_new_notification_bulk
from v0.ui.account.models import Profile


def is_user_permitted(permission_type, user, **kwargs):
    is_permitted = True
    validation_msg_dict = {'msg': None}
    return is_permitted, validation_msg_dict
    checklist_id = kwargs['checklist_id'] if 'checklist_id' in kwargs else None
    campaign_id = kwargs['campaign_id'] if 'campaign_id' in kwargs else None
    permission_list = list(ChecklistPermissions.objects.raw({'profile_id': user.profile_id}))
    if len(permission_list) == 0:
        is_permitted = False
        validation_msg_dict['msg'] = 'no_permission_document'
        return is_permitted, validation_msg_dict
    else:
        permission_obj = permission_list[0]
        checklist_permissions = permission_obj.checklist_permissions
        if checklist_id:
            campaign_id = list(mongo_client.checklists.find({"checklist_id": int(checklist_id)}))[0]['campaign_id']
            checklist_level_permissions = permission_obj.checklist_permissions['checklists']
            if str(checklist_id) not in checklist_level_permissions:
                champaign_level_permissions = permission_obj.checklist_permissions['campaigns']
                if campaign_id not in champaign_level_permissions:
                    is_permitted = False
                    validation_msg_dict['msg'] = 'not_permitted'
                    return is_permitted, validation_msg_dict
                else:
                    if permission_type not in champaign_level_permissions[campaign_id]:
                        is_permitted = False
                        validation_msg_dict['msg'] = 'not_permitted'
                        return is_permitted, validation_msg_dict
            else:
                if permission_type not in checklist_level_permissions[str(checklist_id)]:
                    is_permitted = False
                    validation_msg_dict['msg'] = 'not_permitted'
                    return is_permitted, validation_msg_dict
        elif campaign_id:
            if 'campaigns' not in permission_obj.checklist_permissions:
                validation_msg_dict['msg'] = 'not_permitted'
                return False, validation_msg_dict
            champaign_level_permissions = permission_obj.checklist_permissions['campaigns']
            if campaign_id not in champaign_level_permissions:
                is_permitted = False
                validation_msg_dict['msg'] = 'not_permitted'
                return is_permitted, validation_msg_dict
            else:
                if permission_type not in champaign_level_permissions[campaign_id]:
                    is_permitted = False
                    validation_msg_dict['msg'] = 'not_permitted'
                    return is_permitted, validation_msg_dict
    return is_permitted, validation_msg_dict


def insert_static_cols(row_dict_original,static_column_values, static_column_names, static_column_types, lower_level_checklists):
    #lower_level_rows = list(set([x["parent_row_id"] for x in lower_level_checklists]))
    if isinstance(static_column_values, dict):
        static_column_ids = [int(x) for x in list(static_column_values.keys())]
    else:
        static_column_ids = [1]
        static_column_values = {"1": static_column_values}

    static_data = {}
    first_column_rows = static_column_values["1"]

    counter = 0
    row_dict_all = {}

    order_id_str = "order_id"
    for curr_row in first_column_rows:
        if "row_id" in curr_row and order_id_str == "order_id":
            order_id_str = "row_id"
        order_id = curr_row["order_id"] if 'order_id' in curr_row else curr_row["row_id"]
        #rowid = curr_row["row_id"]
        rowid = order_id
        row_dict = row_dict_original.copy()
        row_dict["rowid"] = rowid
        row_dict["order_id"] = order_id
        cell_value = curr_row['cell_value']

        #if curr_row in lower_level_rows:
        lower_level_array = [x['static_column_values'] for x in lower_level_checklists
                                            if x['parent_row_id']==rowid]
        lower_level_static_column_values = lower_level_array[0] if len(lower_level_array)>0 else {}

        for static_column in static_column_ids:
            static_column_str = str(static_column)
            if static_column > 1:
                curr_static_column_values = static_column_values[static_column_str]
                cell_value = [x["cell_value"] for x in curr_static_column_values if x[order_id_str] == rowid][0]
            static_data[static_column_str] = {
                "cell_value": cell_value,
                "column_id": static_column,
                "column_type": static_column_types[static_column_str],
                "column_name": static_column_names[static_column_str]
            }
            if static_column_str in list(lower_level_static_column_values.keys()):
                lower_level_row_values = lower_level_static_column_values[static_column_str]
                lower_level_row_values_2 = []
                for lower_level_row in lower_level_row_values:
                    lower_level_row["row_id"] = lower_level_row.pop("order_id")
                    lower_level_row_values_2.append(lower_level_row)
                static_data[static_column_str]["lower_level_row_values"] = lower_level_row_values_2

        row_dict["data"] = static_data
        row_dict_all[order_id] = row_dict
        mongo_client.checklist_data.insert_one(row_dict)
    return


def sort_dict(random_dict):
    sorted_dict = collections.OrderedDict()
    random_keys = list(random_dict.keys())
    keys = sorted([int(x) for x in list(random_dict.keys())])
    for key in keys:
        if isinstance(random_keys[0], bytes) or isinstance(random_keys[0], str):
            key = str(key)
        sorted_dict[key] = random_dict[key]
    return sorted_dict


def sort_list_by_key_value(list_to_be_sorted, sorting_key):
    newlist = sorted(list_to_be_sorted, key=itemgetter(sorting_key))
    return newlist


class CreateChecklistTemplate(APIView):
    def post(self, request, campaign_id):
        """
        :param request:
        :return:
        """

        is_permitted, validation_msg_dict = is_user_permitted("EDIT", request.user, campaign_id=campaign_id)
        if not is_permitted:
            return handle_response('', data=validation_msg_dict, success=False)
        class_name = self.__class__.__name__
        checklist_name = request.data['checklist_name']
        checklist_columns = request.data['checklist_columns']
        checklist_type = request.data['checklist_type']
        univalue_items = request.data['univalue_items'] if 'univalue_items' in request.data else None
        static_column_values = request.data['static_column_values']
        lower_level_checklists = []
        n_cols = len(checklist_columns)
        if 'lower_level_checklists' in request.data:
            lower_level_checklists = request.data['lower_level_checklists']

        if isinstance(static_column_values, dict):
            static_column_indices = list(static_column_values.keys())
            static_column_ids = [int(x) for x in static_column_values.keys()]
            static_column_number = len(static_column_ids)
        else:
            static_column_indices = ["1"]
            static_column_ids = [1]
            static_column_values = {"1":static_column_values}

        last_id_data = mongo_client.checklists.find_one(sort=[('checklist_id', -1)])
        last_id = last_id_data['checklist_id'] if last_id_data is not None else 0
        supplier_id = request.data['supplier_id'] if checklist_type == 'supplier'else None
        is_template = True if "is_template" in request.data and request.data['is_template'] == 1 else False
        rows = len(static_column_values["1"])
        checklist_id = last_id + 1
        mongo_form = {
            'checklist_id': checklist_id,
            'campaign_id': campaign_id,
            'checklist_name': checklist_name,
            'status': 'active',
            'supplier_id': supplier_id,
            'checklist_type': checklist_type,
            'rows': rows,
            'columns': n_cols,
            'is_template': is_template,
            'data': {},
            'univalue_items': univalue_items,
            'static_columns': static_column_indices
        }
        column_id = 0
        order_ids = []
        static_column_names = {}
        static_column_types = {}
        for column in checklist_columns:
            column_id = column_id + 1
            order_id = column['order_id']
            order_ids.append(order_id)
            column_options = column['column_options'] if 'column_options' in column else None
            if column_options and not isinstance(column_options, list):
                column_options = column_options.split(',')
                column['column_options'] = column_options
            column['column_id'] = column_id
            mongo_form['data'][str(order_id)] = column
            # if column_id == 1:
            #     first_column_name = column['column_name']
            #     first_column_type = column['column_type']
            if column_id in static_column_ids:
                static_column_names[str(column_id)] = column['column_name']
                static_column_types[str(column_id)] = column['column_type']

        # sorting data
        form_data = mongo_form['data']
        form_data_sorted = collections.OrderedDict()
        for key in sorted(list(form_data.keys())):
            form_data_sorted[key] = form_data[key]
        mongo_form['data'] = form_data_sorted

        mongo_client.checklists.insert_one(mongo_form)
        timestamp = datetime.datetime.utcnow()

        row_dict = {"created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                        "checklist_id": checklist_id, "status": "active"}

        insert_static_cols(row_dict,static_column_values, static_column_names, static_column_types, lower_level_checklists)
        add_single_checklist_permission(request.user.profile_id, checklist_id, ["EDIT", "VIEW", "DELETE", "FILL", "FREEZE", "UNFREEZE"])
        return handle_response(class_name, data='success', success=True)


def enter_row_to_mongo(checklist_data, supplier_id, campaign_id, checklist):
    all_checklist_columns_dict = checklist['data']
    n_cols = len(all_checklist_columns_dict)
    checklist_id = checklist['checklist_id']
    deleted_columns = checklist['deleted_columns'] if 'deleted_columns' in checklist else []
    static_columns = checklist['static_columns'] if 'static_columns' in checklist else ["1"]
    timestamp = datetime.datetime.utcnow()
    total_rows = list(checklist_data.keys())
    exist_rows_query = mongo_client.checklist_data.find({"checklist_id": checklist_id})
    exist_rows_list = list(exist_rows_query)
    exist_rows = exist_rows_query.distinct("rowid")

    #for row in total_rows:
    top_level_rows = [x for x in total_rows if x.count('.')==0]
    top_level_rows_int = [int(x) for x in total_rows if x.count('.')==0]
    row_dict_all = {}

    if not (set(top_level_rows_int)<=set(exist_rows)):
        return [False, 'some rows do not exist']

    for curr_row in top_level_rows:
        curr_level = 0
        rowid = int(curr_row)
        sub_rows = [x for x in total_rows if x.count('.') == 1 and x[0] == curr_row[0]]

        if rowid in exist_rows:
            exist_row_info = [x for x in exist_rows_list if x['rowid'] == rowid][0]
            exist_row_status = exist_row_info['status']
            if exist_row_status == 'inactive':
                print('already deleted row id: ', rowid)
                break
            exist_row_data = exist_row_info['data']
        else:
            return [False,'row '+str(rowid)+' does not exist']
        new_row_data = checklist_data[curr_row]

        row_dict = {"data": {}, "created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                    "checklist_id": checklist_id, "rowid": rowid, "status": "active"}
        order_id = exist_row_info['order_id']
        row_dict['order_id'] = order_id

        for static_column in static_columns:
            if static_column in deleted_columns:
                break
            row_dict['data'][static_column] = exist_row_data[static_column]
        columns = list(new_row_data.keys())
        for column in range(1, n_cols+1):
            if str(column) in deleted_columns:
                print('already deleted column id: ', column)
                continue
            lower_level_row_values = []
            if str(column) in new_row_data:
                column_data = new_row_data[str(column)]
            else:
                continue
            if "cell_value" not in column_data:
                continue
            column_id = column_data["column_id"]
            if str(column_id) in static_columns:
                print('cannot edit static column', column_id)
                continue
            column_name = all_checklist_columns_dict[str(column_id)]["column_name"]
            column_type = all_checklist_columns_dict[str(column_id)]["column_type"]
            value = column_data["cell_value"]

            for sub_row in sub_rows:
                sub_row_id = sub_row.split('.',1)[0]
                if str(column) in checklist_data[sub_row]:
                    sub_row_data = checklist_data[sub_row][str(column)]
                else:
                    continue
                sub_row_data.pop("column_id")
                sub_row_data["row_id"] = rowid
                lower_level_row_values.append(sub_row_data)

            row_dict['data'][str(column_id)] = {
                'column_name': column_name,
                'cell_value': "",
                'column_id': column_id,
                'column_type': column_type,
            }
            if len(lower_level_row_values)>0:
                row_dict['data'][str(column_id)]['lower_level_row_values']= lower_level_row_values
            else:
                # if sub-rows are not empty, higher row cannot be filled
                row_dict['data'][str(column_id)]['cell_value'] = value
        if rowid in exist_rows:
            x = mongo_client.checklist_data.delete_many({'checklist_id': int(checklist_id), 'rowid': rowid}).deleted_count
        row_dict_all[order_id] = row_dict.copy()
    row_dict_all_sorted = sort_dict(row_dict_all)
    for curr_row_order_id in list(row_dict_all_sorted.keys()):
        curr_row_dict = row_dict_all_sorted[curr_row_order_id]
        mongo_client.checklist_data.insert_one(curr_row_dict)
    return [True,'']


class ChecklistEntry(APIView):
    # used to create and update checklist elements
    def put(self, request, checklist_id):

        is_permitted, validation_msg_dict = is_user_permitted("FILL", request.user, checklist_id=checklist_id)
        if not is_permitted:
            return handle_response('', data=validation_msg_dict, success=False)

        checklist = mongo_client.checklists.find_one({"checklist_id": int(checklist_id)})

        if checklist is None:
            data = 'Checklist id does not exist'
            success = False
        elif checklist['status'] == 'inactive':
            data = 'deleted checklist'
            success = False
        elif checklist['is_template'] is True:
            data = 'checklist is a template'
            success = False
        elif checklist['status'] == 'frozen':
            data = 'checklist is already frozen'
            success = False
        else:
            checklist_type = checklist['checklist_type'] if checklist['checklist_type'] else None
            supplier_id = checklist['supplier_id'] if checklist_type == 'supplier'else None
            rows_data = request.data
            campaign_id = checklist['campaign_id']
            new_notifications = request.data['notifications'] if 'notifications' in request.data else None
            if 'notifications' in request.data:
                del request.data['notifications']
            rows_entered = enter_row_to_mongo(rows_data, supplier_id, campaign_id, checklist)
            if rows_entered[0]==False:
                return handle_response({}, data=rows_entered[1], success=False)
            if new_notifications:
                create_new_notification_bulk(request.user, new_notifications, "checklist")
            data = 'success'
            success = True

        return handle_response({}, data=data, success=success)


class ChecklistEdit(APIView):

    def post(self, request, checklist_id):
        is_permitted, validation_msg_dict = is_user_permitted("EDIT", request.user, checklist_id=checklist_id)
        if not is_permitted:
            return handle_response('', data=validation_msg_dict, success=False)
        checklist_id = int(checklist_id)
        class_name = self.__class__.__name__
        columns = request.data['checklist_columns'] if 'checklist_columns' in request.data else []
        static_column = request.data['static_column_values'] if 'static_column_values' in request.data else {}
        new_checklist_columns = request.data['new_checklist_columns'] \
            if 'new_checklist_columns' in request.data else []
        new_static_column_values = request.data['new_static_column_values'] \
            if 'new_static_column_values' in request.data else {}


        is_template = request.data['is_template'] if "is_template" in request.data else None
        if not isinstance(new_static_column_values, dict):
            new_static_column_values = {"1": new_static_column_values}

        checklist_column_all_query = list(mongo_client.checklists.find({"checklist_id": checklist_id}))

        if len(checklist_column_all_query) == 0:
            result = "checklist does not exist"
            return handle_response(class_name, data=result, success=False)
        else:
            checklist_column_all = checklist_column_all_query[0]

        exist_static_column_indices = checklist_column_all['static_columns'] \
            if 'static_columns' in checklist_column_all else []

        if not list(new_static_column_values.keys()) == exist_static_column_indices:
            return handle_response(class_name, data='improper static column info in new rows', success=False)

        checklist_status = checklist_column_all['status']

        if checklist_status == 'inactive':
            result = "checklist is already deleted"
            return handle_response(class_name, data=result, success=False)
        elif checklist_status == 'frozen':
            result = "checklist is frozen, cannot be modified"
            return handle_response(class_name, data=result, success=False)

        delete_rows = request.data['delete_rows'] if 'delete_rows' in request.data else []
        for row in delete_rows:
            mongo_client.checklist_data.update_one({"checklist_id": int(checklist_id), "rowid": int(row)},
                                                   {"$set": {'status': 'inactive'}})

        delete_columns = map(str,request.data['delete_columns']) if 'delete_columns' in request.data else []
        exist_inactive_columns = checklist_column_all['deleted_columns'] if 'deleted_columns' in checklist_column_all\
            else []
        if not delete_columns == []:
            new_delete_columns = list(set(delete_columns+exist_inactive_columns))
            mongo_client.checklists.update_one({"checklist_id": int(checklist_id)},
                                                   {"$set": {'deleted_columns': new_delete_columns}})
        else:
            new_delete_columns = exist_inactive_columns

        checklist_column_data_all = checklist_column_all['data']
        lower_level_checklists = request.data['lower_level_checklists'] \
            if 'lower_level_checklists' in request.data else []
        n_rows = checklist_column_all['rows']
        n_cols = checklist_column_all['columns']
        if new_static_column_values:
            first_element = list(new_static_column_values.values())[0]
            new_rows = len(first_element)
        else:
            new_rows = 0

        # adding column data to checklists table
        # currently, new static column cannot be added to table
        column_id = n_cols
        new_checklist_col_data = {}
        for column in new_checklist_columns:
            column_id = column_id + 1
            column_options = column['column_options'] if 'column_options' in column else None
            if column_options and not isinstance(column_options, list):
                column_options = column_options.split(',')
                column['column_options'] = column_options
            column['column_id'] = column_id
            new_checklist_col_data[str(int(column_id))] = column
        checklist_column_data_all.update(new_checklist_col_data)

        total_cols = column_id

        # editing existing columns
        checklist_data_all = list(mongo_client.checklist_data.find({"checklist_id": checklist_id}))
        for column in columns:
            column_id = column['column_id']
            if str(column_id) in new_delete_columns:
                print("cannot edit already deleted column ", column_id)
                continue
            new_column_data = column
            new_column_data['order_id'] = checklist_column_data_all[str(column_id)]['order_id']
            checklist_column_data_all[str(column_id)] = new_column_data
        checklist_column_data_all = sort_dict(checklist_column_data_all)
        mongo_client.checklists.update_one({'checklist_id': checklist_id}, {
            "$set": {'data': checklist_column_data_all}})

        if not isinstance(static_column, dict):
            static_column = {"1": static_column}

        timestamp = datetime.datetime.utcnow()
        campaign_id = checklist_column_all["campaign_id"]
        supplier_id = checklist_column_all["supplier_id"]

        # editing existing rows
        for column in exist_static_column_indices:
            column_id = int(column)
            if static_column:
                if column in static_column:
                    curr_column_data = static_column[column]
                else:
                    continue
                column_options = curr_column_data['column_options'] if 'column_options' in curr_column_data else None
                if column_options and not isinstance(column_options, list):
                    column_options = column_options.split(',')
                    curr_column_data['column_options'] = column_options
            else:
                curr_column_data = []
            column_name = checklist_column_data_all[column]['column_name']
            column_type = checklist_column_data_all[column]['column_type']

            for row_id in range(1, n_rows+1):
                row_data = [x for x in curr_column_data if x["row_id"] == row_id]
                exist_row = [x for x in checklist_data_all if x['rowid'] == row_id][0]
                exist_row_status = exist_row['status']

                if len(lower_level_checklists) > 0:
                    if exist_row_status == 'inactive':
                        print("cannot add lower level checklists to deleted row", row_id)
                    else:
                        lower_level_array = [x['static_column_values'] for x in lower_level_checklists
                                             if x['parent_row_id'] == row_id]
                        lower_level_static_column_values = lower_level_array[0] if len(lower_level_array) > 0 else {}
                        lower_level_rows = lower_level_static_column_values[column]\
                            if column in lower_level_static_column_values else None
                        mongo_client.checklist_data.update_one({'rowid': int(row_id), 'checklist_id': checklist_id}, {
                            "$set": {'data.'+column+'.lower_level_row_values': lower_level_rows}})
                if len(row_data)>0:
                    if exist_row_status == 'inactive':
                        print("cannot edit labels of deleted row", row_id)
                    else:
                        exist_row_data = [x['data'][column] for x in checklist_data_all if x['rowid'] == row_id][0]
                        exist_row_data['cell_value'] = row_data[0]['cell_value']
                        mongo_client.checklist_data.update_one({'rowid': int(row_id), 'checklist_id': checklist_id}, {
                            "$set": {'data.'+column: exist_row_data}})

        # creating new rows
        row_dict = {"created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                    "checklist_id": checklist_id, "status": "active", "data": {}}
        row_array = {}
        row_data = {}

        all_rows_dict = {}
        for row_id in range(n_rows+1, n_rows+new_rows+1):
            row_index = row_id - (n_rows+1)
            row_dict['rowid'] = row_id
            for column in exist_static_column_indices:
                column_id = int(column)
                column_name = checklist_column_data_all[column]['column_name']
                column_type = checklist_column_data_all[column]['column_type']
                curr_row_data = new_static_column_values[column][row_index]
                order_id = curr_row_data['order_id']
                row_dict['order_id'] = order_id
                cell_value = curr_row_data['cell_value']
                row_data[column] = {
                    "column_id": column_id,
                    "column_name": column_name,
                    "column_type": column_type,
                    "cell_value": cell_value,
                    "order_id": order_id
                }
            row_dict["data"] = row_data.copy()
            all_rows_dict[order_id] = row_dict.copy()
        all_rows_dict = sort_dict(all_rows_dict)
        for curr_row_key in list(all_rows_dict.keys()):
            curr_row_dict = all_rows_dict[curr_row_key]
            mongo_client.checklist_data.insert_one(curr_row_dict)

        set_checklist_dict = {'data': checklist_column_data_all, 'columns': total_cols, 'rows': n_rows+new_rows}

        if is_template:
            set_checklist_dict['is_template'] = is_template
        mongo_client.checklists.update_one({'checklist_id': checklist_id}, {
            "$set": set_checklist_dict})

        return handle_response(class_name, data='success', success=True)


class GetAllChecklists(APIView):
    # used for getting a list of all checklists of a campaign
    def get(self, request):
        class_name = self.__class__.__name__
        campaign_list = CampaignAssignment.objects.filter(assigned_to_id=request.user.id).values_list('campaign_id', flat=True) \
            .distinct()
        campaign_list = [campaign_id for campaign_id in campaign_list]
        all_campaign_name = ProposalInfo.objects.filter(proposal_id__in=campaign_list).values('proposal_id',
                                                                                                     'name')
        all_campaign_name_dict = {campaign['proposal_id']: campaign['name'] for campaign in all_campaign_name}
        all_campaign_checklists = list(mongo_client.checklists.find({"$and": [{"campaign_id": {"$in": campaign_list}},
                                                                         {"status": {"$ne": "inactive"}}]}))
        all_checklist_names = {checklist["checklist_id"]: checklist["checklist_name"] for checklist in all_campaign_checklists}
        all_campaign_checklists_dict = {}
        for single_object in all_campaign_checklists:
            if single_object['campaign_id'] not in all_campaign_checklists_dict:
                all_campaign_checklists_dict[single_object['campaign_id']] = []
            all_campaign_checklists_dict[single_object['campaign_id']].append(single_object['checklist_id'])
        for campaign_id in campaign_list:
            if campaign_id not in all_campaign_checklists_dict:
                all_campaign_checklists_dict[campaign_id] = []
        all_campaign_checklists_list = []
        for campaign_id in all_campaign_checklists_dict:
            campaign_checklist_dict = {
                "campaign_id": campaign_id,
                "campaign_name": all_campaign_name_dict[campaign_id],
                "checklists": []
            }

            for checklist_id in all_campaign_checklists_dict[campaign_id]:
                campaign_checklist_dict["checklists"].append({
                    "checklist_name": all_checklist_names[checklist_id],
                    "checklist_id": checklist_id
                })
            all_campaign_checklists_list.append(campaign_checklist_dict)
        return handle_response(class_name, data=all_campaign_checklists_list, success=True)


class GetCampaignChecklists(APIView):
    # used for getting a list of all checklists of a campaign
    def get(self, request, campaign_id):
        class_name = self.__class__.__name__
        status = request.query_params.get('status', 'both')
        if status == 'both':
            all_campaign_checklists = list(mongo_client.checklists.find({"$and": [{"campaign_id": campaign_id},
                                                                                  {"checklist_type": "campaign"},
                                                                         {"status": {"$ne": "inactive"}}]}))
        else:
            all_campaign_checklists = list(mongo_client.checklists.find({"campaign_id": campaign_id, "status": status}))
        checklist_id_list = []
        for checklist in all_campaign_checklists:
            is_permitted, validation_msg = is_user_permitted("VIEW", request.user,
                                                             checklist_id=checklist['checklist_id'])
            if is_permitted:
                checklist_id_list.append(checklist['checklist_id'])
        checklists = []
        for checklist_id in checklist_id_list:
            new_checklist = get_checklist_by_id(checklist_id)
            if new_checklist:
                checklists.append(new_checklist)
        return handle_response(class_name, data=checklists, success=True)


class GetAllChecklistsTemplates(APIView):
    # used for getting a list of all checklists of a campaign
    def get(self, request):
        class_name = self.__class__.__name__
        campaign_list = CampaignAssignment.objects.filter(assigned_to_id=request.user.id).values_list('campaign_id', flat=True) \
            .distinct()
        campaign_list = [campaign_id for campaign_id in campaign_list]
        all_campaign_checklists = list(mongo_client.checklists.find({"$and": [{"campaign_id": {"$in": campaign_list}},
                                                                              {"status": {"$ne": "inactive"}},
                                                                              {"is_template": True}]}))
        checklist_id_list = []
        for checklist in all_campaign_checklists:
            checklist_id_list.append(checklist['checklist_id'])
        checklists = []
        for checklist_id in checklist_id_list:
            new_checklist = get_checklist_by_id(checklist_id)
            if new_checklist:
                checklists.append(new_checklist)
        return handle_response(class_name, data=checklists, success=True)


class GetSupplierChecklists(APIView):
    # used for getting a list of all checklists of a campaign
    def get(self, request, campaign_id, supplier_id):
        class_name = self.__class__.__name__
        status = request.query_params.get('status', 'both')
        if status == 'both':
            all_campaign_checklists = list(mongo_client.checklists.find({"$and": [{"campaign_id": campaign_id,
                                           "supplier_id": supplier_id}, {"status": {"$ne": "inactive"}}]}))
        else:
            all_campaign_checklists = list(mongo_client.checklists.find({"campaign_id": campaign_id,
                                           "supplier_id": supplier_id, "status": status}))
        checklist_id_list = []
        for checklist in all_campaign_checklists:
            is_permitted, validation_msg = is_user_permitted("VIEW", request.user, checklist_id=checklist['checklist_id'])
            if is_permitted:
                checklist_id_list.append(checklist['checklist_id'])
        checklists = []
        for checklist_id in checklist_id_list:
            new_checklist = get_checklist_by_id(checklist_id)
            if new_checklist:
                checklists.append(new_checklist)
        return handle_response(class_name, data=checklists, success=True)


class FreezeChecklist(APIView):
    @staticmethod
    def put(request,checklist_id, state):
        current_data = mongo_client.checklists.find_one({"checklist_id": int(checklist_id)})
        current_status = current_data['status']
        if current_status == 'inactive':
            response = 'checklist is already deleted'
            return handle_response({}, data=response, success=False)
        if current_status == 'active':
            if state == '0':
                response = 'checklist is already active'
                return handle_response({}, data=response, success=False)
            if state == '1':
                is_permitted, validation_msg_dict = is_user_permitted("FREEZE", request.user, checklist_id=checklist_id)
                if not is_permitted:
                    return handle_response('', data=validation_msg_dict, success=False)
                mongo_client.checklists.update_one({"checklist_id": int(checklist_id)},  {"$set": {'status': 'frozen'}})
        if current_status == 'frozen':
            if state == '0':
                is_permitted, validation_msg_dict = is_user_permitted("UNFREEZE", request.user, checklist_id=checklist_id)
                if not is_permitted:
                    return handle_response('', data=validation_msg_dict, success=False)
                mongo_client.checklists.update_one({"checklist_id": int(checklist_id)}, {"$set": {'status': 'active'}})
            if state == '1':
                response = 'checklist is already frozen'
                return handle_response({}, data=response, success=False)
        return handle_response({}, data='success', success=True)


# class FreezeChecklistAll(APIView):
#     @staticmethod
#     def get(request, state):
#         campaign_id = request.query_params.get("campaign_id", None)
#         supplier_id = request.query_params.get("supplier_id", None)


def get_checklist_by_id(checklist_id):
    checklist_id = int(checklist_id)
    checklist_info = mongo_client.checklists.find_one({"checklist_id": checklist_id})
    if checklist_info is None:
        return None
    elif checklist_info['status'] == 'inactive':
        return None
    checklist_dict = {
        "checklist_type": checklist_info['checklist_type'] if 'checklist_type' in checklist_info else "campaign",
        "campaign_id": checklist_info['campaign_id'],
        "rows": checklist_info['rows'] if 'rows' in checklist_info else None,
        "supplier_id": checklist_info['supplier_id'] if 'supplier_id' in checklist_info else None,
        "checklist_name": checklist_info['checklist_name'] if 'checklist_name' in checklist_info else None,
        "is_template": checklist_info['is_template'] if 'is_template' in checklist_info else False,
        "checklist_id": checklist_info['checklist_id'],
        "status": checklist_info['status'] if 'status' in checklist_info else 'active',
    }
    checklist_data = list(mongo_client.checklist_data.find({"checklist_id": checklist_id}))
    try:
        checklist_data = sorted(checklist_data, key=itemgetter('order_id'))
    except:
        checklist_data = sorted(checklist_data, key=itemgetter('rowid'))
    values = []
    column_headers = []
    row_headers = {}
    checklist_info_columns_unsorted = checklist_info['data']
    checklist_info_deleted_columns = checklist_info['deleted_columns'] if 'deleted_columns' in checklist_info else []
    checklist_info_columns = sort_dict(checklist_info_columns_unsorted)
    columns_list = list(checklist_info_columns.keys())
    checklist_info_static_columns = checklist_info['static_columns'] if 'static_columns' in checklist_info else []
    for column in checklist_info_static_columns:
        row_headers[column] = []
    for column in columns_list:
        if str(column) not in checklist_info_deleted_columns:
            column_headers.append(checklist_info_columns[column])
    for checklist in checklist_data:
        row_id = checklist['rowid']
        if checklist['status'] == 'inactive':
            print(("# row already deleted: ", row_id))
            continue
        curr_row_data = checklist['data']
        curr_row_columns = list(curr_row_data.keys())
        curr_row_columns.sort()
        for column in curr_row_columns:
            value = curr_row_data[column]["cell_value"]
            column_id = column
            #row_headers[column_id] = []
            if column not in checklist_info_deleted_columns:
                if column in checklist_info_static_columns:
                    row_headers[column_id].append({
                        "cell_value": value,
                        "row_id": row_id
                    })
                else:
                    values.append({
                        "row_id": row_id,
                        "value": value,
                        "column_id": int(column_id)
                    })
    final_data = {'values': values, 'column_headers': column_headers, 'row_headers': row_headers,
                  'checklist_info': checklist_dict}
    return final_data


class GetChecklistData(APIView):
    @staticmethod
    def get(request, checklist_id):
        is_permitted, validation_msg_dict = is_user_permitted("VIEW", request.user, checklist_id=checklist_id)
        if not is_permitted:
            return handle_response('', data=validation_msg_dict, success=False)
        final_data = get_checklist_by_id(checklist_id)
        return handle_response({}, data=final_data, success=True)


class DeleteChecklist(APIView):
    # deactivating a full checklist
    @staticmethod
    def put(request,checklist_id):
        is_permitted, validation_msg_dict = is_user_permitted("DELETE", request.user, checklist_id=checklist_id)
        if not is_permitted:
            return handle_response('', data=validation_msg_dict, success=False)
        checklist_info = mongo_client.checklists.find_one({"checklist_id": int(checklist_id)})
        success = False
        if checklist_info is None:
            return handle_response({}, data='checklist does not exist', success=success)
        checklist_status = checklist_info['status'] if 'status' in checklist_info else 'active'
        if checklist_status == 'inactive':
            data = 'checklist is already deleted'
        elif checklist_status == 'frozen':
            data = "checklist is frozen, cannot be modified"
        else:
            mongo_client.checklists.update_one({"checklist_id": int(checklist_id)},  {"$set": {'status': 'inactive'}})
            data = 'success'
            success = True
        return handle_response({}, data=data, success=success)


class DeleteChecklistRow(APIView):
    @staticmethod
    def put(request, checklist_id, row_id):
        mongo_client.checklist_data.update_one({"checklist_id": int(checklist_id), "rowid": int(row_id)},
                                               {"$set": {'status': 'inactive'}})
        return handle_response({}, data='success', success=True)


def add_single_checklist_permission(profile_id, checklist_id, new_permissions):
    existing_checklist_permissions_dict = list(ChecklistPermissions.objects.raw({"profile_id": profile_id}))
    if len(existing_checklist_permissions_dict) == 0:
        return handle_response({}, data='something_is_wrong', success=False)
    existing_checklist_permissions_dict = existing_checklist_permissions_dict[0]
    permissions_id = str(existing_checklist_permissions_dict._id)
    old_checklist_permissions = existing_checklist_permissions_dict.checklist_permissions
    if "checklists" not in old_checklist_permissions:
        old_checklist_permissions["checklists"] = {}
    old_checklist_permissions["checklists"][str(checklist_id)] = new_permissions
    dict_of_req_attributes = {
        "profile_id": profile_id,
        "checklist_permissions": old_checklist_permissions,
        "updated_at": datetime.datetime.now()
    }
    ChecklistPermissions.objects.raw({'_id': ObjectId(permissions_id)}).update({"$set": dict_of_req_attributes})


class ChecklistPermissionsAPI(APIView):
    @staticmethod
    def post(request):
        for single_obj in request.data:
            checklist_permissions = single_obj['checklist_permissions']
            profile_id = single_obj['profile_id']
            organisation_id = get_user_organisation_id(request.user)
            dict_of_req_attributes = {"checklist_permissions": checklist_permissions,
                                      "organisation_id": organisation_id, "profile_id": profile_id}
            (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
            if not is_valid:
                return handle_response('', data=validation_msg_dict, success=False)
            checklist_permissions_dict = dict_of_req_attributes
            checklist_permissions_dict["created_by"] = request.user.id
            checklist_permissions_dict["created_at"] = datetime.datetime.now()
            ChecklistPermissions(**checklist_permissions_dict).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        organisation_id = get_user_organisation_id(request.user)
        checklist_permissions = ChecklistPermissions.objects.raw({"organisation_id": organisation_id})
        all_user_id_list = []
        all_profile_id_list = []
        for permission in checklist_permissions:
            if permission.profile_id not in all_profile_id_list:
                all_profile_id_list.append(permission.profile_id)
            if permission.created_by not in all_user_id_list:
                all_user_id_list.append(permission.created_by)
        all_user_objects = BaseUser.objects.filter(id__in=all_user_id_list).all()
        all_user_dict = {user.id: {"first_name": user.first_name,
                                    "last_name": user.last_name,
                                    "username": user.username,
                                    "email": user.email,
                                    "id": user.id
                                      } for user in all_user_objects}
        all_profile_objects = Profile.objects.filter(id__in=all_profile_id_list).all()
        all_profile_dict = {profile.id: {
                                        "id": profile.id,
                                        "name": profile.name,
                                        "is_standard": profile.is_standard,
                                        "organisation_id": profile.organisation_id,
                                    } for profile in all_profile_objects}
        data = []
        for permission in checklist_permissions:
            permission_data = {
                "id": str(permission._id),
                "profile_id": all_profile_dict[int(permission.profile_id)] if int(permission.profile_id) in all_profile_dict else None,
                "organisation_id": permission.organisation_id,
                "checklist_permissions": permission.checklist_permissions,
                "created_by": all_user_dict[int(permission.created_by)] if int(permission.created_by) in all_user_dict else None
            }
            data.append(permission_data)
        return handle_response('', data=data, success=True)

    @staticmethod
    def put(request):
        permissions = request.data
        for permission in permissions:
            dict_of_req_attributes = {
                "profile_id": permission['profile_id'],
                "checklist_permissions": permission['checklist_permissions'],
                "updated_at": datetime.datetime.now()
            }
            ChecklistPermissions.objects.raw({'_id': ObjectId(permission['id'])}).update({"$set": dict_of_req_attributes})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request):
        permission_id = request.query_params.get("permission_id",None)
        if not permission_id:
            return handle_response('', data="Permission Id Not Provided", success=False)
        exist_permission_query = ChecklistPermissions.objects.raw({'_id': ObjectId(permission_id)})[0]
        exist_permission_query.delete()
        return handle_response('', data="success", success=True)


class ChecklistPermissionsByProfileIdAPI(APIView):
    @staticmethod
    def get(request, profile_id):
        organisation_id = get_user_organisation_id(request.user)
        checklist_permissions = list(ChecklistPermissions.objects.raw(
            {"profile_id": int(profile_id), "organisation_id": organisation_id}))
        all_user_id_list = []
        all_profile_id_list = []
        for permission in checklist_permissions:
            if permission.profile_id not in all_profile_id_list:
                all_profile_id_list.append(permission.profile_id)
            if permission.created_by not in all_user_id_list:
                all_user_id_list.append(permission.created_by)

        all_user_objects = BaseUser.objects.filter(id__in=all_user_id_list).all()
        all_user_dict = {user.id: {"first_name": user.first_name,
                                    "last_name": user.last_name,
                                    "username": user.username,
                                    "email": user.email,
                                    "id": user.id
                                      } for user in all_user_objects}
        all_profile_objects = Profile.objects.filter(id__in=all_profile_id_list).all()
        all_profile_dict = {profile.id: {"name": profile.name,
                                         "id": profile.id,
                                         "is_standard": profile.is_standard,
                                         "organisation_id": profile.organisation_id,
                                         } for profile in all_profile_objects}
        if len(checklist_permissions) == 0:
            return handle_response('', data="no_permission_exists", success=True)

        checklist_permissions = checklist_permissions[0]
        permission_data = {
            "id": str(checklist_permissions._id),
            "profile_id": all_profile_dict[int(checklist_permissions.profile_id)] if int(checklist_permissions.profile_id) in all_profile_dict else None,
            "organisation_id": checklist_permissions.organisation_id,
            "checklist_permissions": checklist_permissions.checklist_permissions,
            "created_by": all_user_dict[int(checklist_permissions.created_by)] if int(checklist_permissions.created_by) in all_user_dict else None
        }
        return handle_response('', data=permission_data, success=True)


def get_numeric_in_array_dict(curr_dict):
    new_dict = {}
    for key in list(curr_dict.keys()):
        curr_array = curr_dict[key]
        new_array = []
        for x in curr_array:
            if isinstance(x, (int, float)):
                new_array.append(x)
        new_dict[key] = new_array
    return new_dict


def binary_operation(a, b, op):
    operator_map = {"/": round(float(a)/b,5), "*":a*b, "+":a+b, "-": a-b}
    return operator_map[op]


def process_metrics(operations_array, raw_map):
    valid_codes = list(raw_map.keys())
    final_array = []
    for metric_array in operations_array:
        if len(metric_array) == 1:
            result = raw_map[metric_array[0]]
            return [result]
        a_code = metric_array[0]
        b_code = metric_array[1]
        op = metric_array[2]
        if type(a_code) is str:
            if a_code[0] == 'm':
                a_code = a_code[1:]
                a = final_array[int(a_code) - 1]
            else:
                if a_code not in raw_map:
                    print("index points to invalid result operation")
                    return[]
                a = raw_map[a_code]
        else:
            a = a_code
        if type(b_code) is str:
            if b_code[0] == 'm':
                b_code = b_code[1:]
                b = final_array[int(b_code) - 1]
            else:
                if b_code not in raw_map:
                    print("index points to invalid result operation")
                    return[]
                b = raw_map[b_code]
        else:
            b = b_code
        curr_result = binary_operation(a, b, op)
        final_array.append(curr_result)
    return final_array


# def process_metrics_checklist(operations_array, raw_map):
#     final_array = []
#     for metric_array in operations_array:
#         a_code = metric_array[0]
#         b_code = metric_array[1]
#         op = metric_array[2]
#         if type(a_code) is str:
#             if a_code[0] == 'm':
#                 a_code = a_code[1:]
#                 a = final_array[int(a_code) - 1]
#             else:
#                 a_code = a_code[1:]
#                 a = raw_map[a_code]
#         else:
#             a = a_code
#         if type(b_code) is str:
#             if b_code[0] == 'm':
#                 b_code = b_code[1:]
#                 b = final_array[int(b_code) - 1]
#             else:
#                 b_code = b_code[1:]
#                 b = raw_map[b_code]
#         else:
#             b = b_code
#         curr_result = binary_operation(a, b, op)
#         final_array.append(curr_result)
#     return final_array


class ChecklistUnsavedOperators(APIView):
    @staticmethod
    def put(request):
        checklist_id = request.data['checklist_id']
        column_ids = request.data['column_ids']
        result_operations = request.data['result_operations']
        column_operations = request.data['column_operations']
        checklist_data_list_unsorted = list(mongo_client.checklist_data.find({"checklist_id":checklist_id}))
        checklist_data_list = checklist_data_list_unsorted
        column_value_dict = {}
        for curr_dict in checklist_data_list:
            for curr_column in column_ids:
                if curr_column not in curr_dict['data']:
                    continue
                curr_column_value = curr_dict['data'][curr_column]['cell_value']
                if curr_column not in column_value_dict:
                    column_value_dict[curr_column] = []
                column_value_dict[curr_column].append(curr_column_value)
        if column_value_dict == {}:
            return handle_response('', data=column_value_dict, success=True)
        numeric_dict = get_numeric_in_array_dict(column_value_dict)
        result_map = {}
        for op_id in column_operations:
            curr_operation_dict = column_operations[op_id]
            result_index = op_id
            column_id = str(curr_operation_dict['column_id'])
            if column_id not in numeric_dict:
                print("column id missing from checklist: ", column_id)
                continue
            curr_operation = curr_operation_dict['operator']
            corr_col_values = numeric_dict[column_id]
            curr_result_str = 'np.' + curr_operation + '(numeric_dict["' + column_id + '"])'
            curr_result = eval(curr_result_str)
            result_map[result_index] = curr_result
        final_result = process_metrics(result_operations,result_map)[-1]
        return handle_response('', data=[numeric_dict,result_map, final_result], success=True)


# used to store, retrieve and manage operator details
class ChecklistSavedOperators(APIView):

    @staticmethod
    def post(request):
        metrics_data = request.data
        last_operator_id =  mongo_client.checklist_operators.find_one(sort=[('operator_id', -1)])["operator_id"]
        print(last_operator_id)
        operator_id = last_operator_id+1
        metrics_data["operator_id"]=operator_id
        ChecklistOperators(**metrics_data).save()
        return handle_response('', data="success", success=True)

    @staticmethod
    def get(request):
        checklist_id = request.query_params.get("checklist_id",None)
        operator_response = list(ChecklistOperators.objects.raw({"$and": [{"checklist_id": int(checklist_id)}, {
            "status": {"$ne": "inactive"}}]}))
        fields = ["operator_id", "checklist_id", "column_ids","column_operations","result_operations"]
        final_response = {}
        counter = 1
        for curr_response in operator_response:
            #print(curr_response.to_son().to_dict)
            operator_name = curr_response.operator_name if curr_response.operator_name else None
            final_response[counter] = {
                "operator_id":curr_response.operator_id,
                "checklist_id": curr_response.checklist_id,
                "column_ids": curr_response.column_ids,
                "column_operations": curr_response.column_operations,
                "result_operations": curr_response.result_operations,
                "operator_name": operator_name
            }
            counter = counter + 1
        return handle_response('',data=final_response, success=True)

    @staticmethod
    def put(request):
        operator_data = request.data
        if 'operator_id' not in operator_data:
            return handle_response('', data='operator id missing', success=True)
        else:
            operator_id = operator_data['operator_id']
        operator_data.pop('operator_id')
        operator_response = mongo_client.checklist_operators.update_one({"operator_id": int(operator_id)}, {
            "$set":operator_data})
        return handle_response('', data="success", success=True)

    @staticmethod
    def delete(request):
        operator_id = request.query_params.get("operator_id", None)
        operator_response = mongo_client.checklist_operators.update_one(
            {"operator_id": int(operator_id)}, {"$set": {'status': 'inactive'}})
        return handle_response('', data="success", success=True)


# used to get results from execution of saved operators
class ChecklistSavedOperatorsResult(APIView):
    @staticmethod
    def get(request, checklist_id):
        operator_id = request.query_params.get('operator_id',None)
        match_dict = {"$and": [{"checklist_id": int(checklist_id)},  {"status": {"$ne": "inactive"}}]}
        if operator_id is not None:
            match_dict['operator_id'] = int(operator_id)
        operator_response = list(mongo_client.checklist_operators.find(match_dict,{"_id":0}))
        checklist_data_list = list(mongo_client.checklist_data.find({"checklist_id":int(checklist_id)}))
        # operator_response = list(ChecklistOperators.objects.raw({"$and": [{"checklist_id": int(checklist_id)}, {
        #     "status": {"$ne": "inactive"}}]}))
        result_dict = {}

        for curr_response in operator_response:
            column_ids = curr_response['column_ids']
            result_operations = curr_response['result_operations']
            column_operations = curr_response['column_operations']
            operator_id = curr_response['operator_id']
            column_value_dict = {}
            for curr_dict in checklist_data_list:
                for curr_column in column_ids:
                    if str(curr_column) not in curr_dict['data']:
                        continue
                    curr_column_value = curr_dict['data'][str(curr_column)]['cell_value']
                    if str(curr_column) not in column_value_dict:
                        column_value_dict[str(curr_column)] = []
                    column_value_dict[str(curr_column)].append(curr_column_value)
            if column_value_dict == {}:
                result_dict[str(operator_id)] = {'operator_definition': curr_response, 'final_value': 'operator error',
                                                 'column_values': {}, 'column_operations': {},
                                                 'result_operations': []}
                continue
                #return handle_response('', data=column_value_dict, success=True)
            numeric_dict = get_numeric_in_array_dict(column_value_dict)
            result_map = {}
            for op_id in column_operations:
                curr_operation_dict = column_operations[op_id]
                result_index = op_id
                column_id = str(curr_operation_dict['column_id'])
                if column_id not in numeric_dict:
                    print("column id missing from checklist: ", column_id)
                    continue
                curr_operation = curr_operation_dict['operator']
                corr_col_values = numeric_dict[column_id]
                curr_result_str = 'np.' + curr_operation + '(numeric_dict["' + column_id + '"])'
                curr_result = eval(curr_result_str)
                result_map[result_index] = curr_result

            all_results = process_metrics(result_operations, result_map)
            curr_result = all_results[-1] if not all_results == [] else "operator error"
            if '_cls' in curr_response: curr_response.pop("_cls")
            result_dict[str(operator_id)] = {'operator_definition': curr_response,'final_value': curr_result,
                                             'column_values': numeric_dict, 'column_operations': result_map,
                                             'result_operations': all_results}
        return handle_response('', data=result_dict, success=True)


class ChecklistPermissionsSelfAPI(APIView):
    @staticmethod
    def get(request):
        organisation_id = get_user_organisation_id(request.user)
        checklist_permissions = list(ChecklistPermissions.objects.raw(
            {"profile_id": int(request.user.profile_id), "organisation_id": organisation_id}))
        all_user_id_list = []
        all_profile_id_list = []
        for permission in checklist_permissions:
            if permission.created_by not in all_user_id_list:
                all_user_id_list.append(permission.created_by)
            if permission.profile_id not in all_profile_id_list:
                all_profile_id_list.append(permission.profile_id)

        all_user_objects = BaseUser.objects.filter(id__in=all_user_id_list).all()
        all_user_dict = {user.id: {"first_name": user.first_name,
                                    "last_name": user.last_name,
                                    "username": user.username,
                                    "email": user.email,
                                    "id": user.id
                                      } for user in all_user_objects}
        all_profile_objects = Profile.objects.filter(id__in=all_profile_id_list).all()
        all_profile_dict = {profile.id: {"name": profile.name,
                                       "is_standard": profile.is_standard,
                                       "organisation_id": profile.organisation_id,
                                   } for profile in all_profile_objects}
        if len(checklist_permissions) == 0:
            return handle_response('', data="no_permission_exists", success=True)

        checklist_permissions = checklist_permissions[0]
        permission_data = {
            "id": str(checklist_permissions._id),
            "profile_id": all_profile_dict[int(checklist_permissions.profile_id)] if int(checklist_permissions.profile_id) in all_profile_dict else None,
            "organisation_id": checklist_permissions.organisation_id,
            "checklist_permissions": checklist_permissions.checklist_permissions,
            "created_by": all_user_dict[int(checklist_permissions.created_by)] if int(checklist_permissions.created_by) in all_user_dict else None
        }
        return handle_response('', data=permission_data, success=True)
