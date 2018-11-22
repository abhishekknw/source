from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from celery import shared_task
from v0.ui.common.models import mongo_client, mongo_test
import datetime
import collections

def insert_static_cols(row_dict_original,static_column_values, static_column_names, static_column_types, lower_level_checklists):
    #lower_level_rows = list(set([x["parent_row_id"] for x in lower_level_checklists]))
    if isinstance(static_column_values, dict):
        static_column_ids = [int(x) for x in static_column_values.keys()]
    else:
        static_column_ids = [1]
        static_column_values = {"1": static_column_values}

    static_data = {}
    first_column_rows = static_column_values["1"]

    counter = 0
    row_dict_array = []

    for curr_row in first_column_rows:
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
                cell_value = [x["cell_value"] for x in curr_static_column_values if x["order_id"] == rowid][0]
            static_data[static_column_str] = {
                "cell_value": cell_value,
                "column_id": static_column,
                "column_type": static_column_types[static_column_str],
                "column_name": static_column_names[static_column_str]
            }
            if static_column_str in lower_level_static_column_values.keys():
                lower_level_row_values = lower_level_static_column_values[static_column_str]
                lower_level_row_values_2 = []
                for lower_level_row in lower_level_row_values:
                    lower_level_row["row_id"] = lower_level_row.pop("order_id")
                    lower_level_row_values_2.append(lower_level_row)
                static_data[static_column_str]["lower_level_row_values"] = lower_level_row_values_2

        row_dict["data"] = static_data
        mongo_client.checklist_data.insert_one(row_dict)
    return

def sort_dict(random_dict):
    sorted_dict = collections.OrderedDict()
    for key in sorted(random_dict.keys()):
        sorted_dict[key] = random_dict[key]
    return sorted_dict

class CreateChecklistTemplate(APIView):
    def post(self, request, campaign_id):
        """
        :param request:
        :return:
        """
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
            static_column_indices = static_column_values.keys()
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
        for key in sorted(form_data.keys()):
            form_data_sorted[key] = form_data[key]
        mongo_form['data'] = form_data_sorted

        mongo_client.checklists.insert_one(mongo_form)
        timestamp = datetime.datetime.utcnow()

        row_dict = {"created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                        "checklist_id": checklist_id, "status": "active"}

        insert_static_cols(row_dict,static_column_values, static_column_names, static_column_types, lower_level_checklists)

        return ui_utils.handle_response({}, data='success', success=True)


def enter_row_to_mongo(checklist_data, supplier_id, campaign_id, checklist):
    all_checklist_columns_dict = checklist['data']
    n_cols = len(all_checklist_columns_dict)
    checklist_id = checklist['checklist_id']
    static_columns = checklist['static_columns'] if 'static_columns' in checklist else ["1"]
    timestamp = datetime.datetime.utcnow()
    total_rows = checklist_data.keys()
    exist_rows_query = mongo_client.checklist_data.find({"checklist_id": checklist_id})
    exist_rows_list = list(exist_rows_query)
    exist_rows = exist_rows_query.distinct("rowid")

    #for row in total_rows:
    top_level_rows = [x for x in total_rows if x.count('.')==0]

    for curr_row in top_level_rows:
        curr_level = 0
        rowid = int(curr_row)
        sub_rows = [x for x in total_rows if x.count('.') == 1 and x[0] == curr_row[0]]

        if rowid in exist_rows:
            exist_row_data = [x['data'] for x in exist_rows_list if x['rowid'] == rowid][0]
        new_row_data = checklist_data[curr_row]

        row_dict = {"data": {}, "created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                    "checklist_id": checklist_id, "rowid": rowid, "status": "active"}

        for static_column in static_columns:
            row_dict['data'][static_column] = exist_row_data[static_column]
        columns = new_row_data.keys()
        for column in range(1, n_cols+1):
            lower_level_row_values = []
            if str(column) in new_row_data:
                column_data = new_row_data[str(column)]
            else:
                continue
            if "cell_value" not in column_data:
                continue
            column_id = column_data["column_id"]
            if str(column_id) in static_columns:
                print 'cannot edit static column', column_id
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
        mongo_client.checklist_data.insert_one(row_dict).inserted_id
    return


class ChecklistEntry(APIView):
    # used to create and update checklist elements
    def put(self, request, checklist_id):
        checklist = mongo_client.checklists.find_one({"checklist_id": int(checklist_id)})

        if checklist == None:
            data = 'Checklist id does not exist'
            success = False
        elif checklist['status']=='inactive':
            data = 'deleted checklist'
            success = False
        elif checklist['is_template'] == True:
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
            enter_row_to_mongo(rows_data, supplier_id, campaign_id, checklist)
            data = 'success'
            success = True

        return ui_utils.handle_response({}, data=data, success=success)


class ChecklistEdit(APIView):

    def post(self, request, checklist_id):
        checklist_id = int(checklist_id)
        class_name = self.__class__.__name__
        columns = request.data['checklist_columns'] if 'checklist_columns' in request.data else []
        static_column = request.data['static_column_values'] if 'static_column_values' in request.data else {}
        new_checklist_columns = request.data['new_checklist_columns'] \
            if 'new_checklist_columns' in request.data else []
        new_static_column_values = request.data['new_static_column_values'] \
            if 'new_static_column_values' in request.data else {}


        if not isinstance(new_static_column_values, dict):
            new_static_column_values = {"1": new_static_column_values}

        checklist_column_all_query = list(mongo_client.checklists.find({"checklist_id": checklist_id}))

        if len(checklist_column_all_query) == 0:
            result = "checklist does not exist"
            return ui_utils.handle_response(class_name, data=result, success=False)
        else:
            checklist_column_all = checklist_column_all_query[0]

        checklist_status = checklist_column_all['status']

        if checklist_status == 'inactive':
            result = "checklist is already deleted"
            return ui_utils.handle_response(class_name, data=result, success=False)
        elif checklist_status == 'frozen':
            result = "checklist is frozen, cannot be modified"
            return ui_utils.handle_response(class_name, data=result, success=False)

        delete_rows = request.data['delete_rows'] if 'delete_rows' in request.data else []
        for row in delete_rows:
            mongo_client.checklist_data.update_one({"checklist_id": int(checklist_id), "rowid": int(row)},
                                                   {"$set": {'status': 'inactive'}})


        checklist_column_data_all = checklist_column_all['data']
        exist_static_column_indices = checklist_column_all['static_columns']
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

        checklist_data_all = list(mongo_client.checklist_data.find({"checklist_id": checklist_id}))
        for column in columns:
            column_id = column['column_id']
            new_column_data = column
            new_column_data['order_id'] = checklist_column_data_all[str(column_id)]['order_id']
            checklist_column_data_all[str(column_id)] = new_column_data
        print checklist_column_data_all
        checklist_column_data_all = sort_dict(checklist_column_data_all)
        mongo_client.checklists.update_one({'checklist_id': checklist_id}, {
            "$set": {'data': checklist_column_data_all}})

        if not isinstance(static_column, dict):
            static_column = {"1": static_column}

        timestamp = datetime.datetime.utcnow()
        campaign_id = checklist_column_all["campaign_id"]
        supplier_id = checklist_column_all["supplier_id"]

        for column in exist_static_column_indices:
            column_id = int(column)
            if static_column:
                curr_column_data = static_column[column]
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
                        print "cannot add lower level checklists to deleted row", row_id
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
                        print "cannot edit labels of deleted row", row_id
                    else:
                        exist_row_data = [x['data'][column] for x in checklist_data_all if x['rowid'] == row_id][0]
                        exist_row_data['cell_value'] = row_data[0]['cell_value']
                        mongo_client.checklist_data.update_one({'rowid': int(row_id), 'checklist_id': checklist_id}, {
                            "$set": {'data.'+column: exist_row_data}})

        row_dict = {"created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                    "checklist_id": checklist_id, "status": "active", "data": {}}
        row_array = {}
        row_data = {}

        for row_id in range(n_rows+1, n_rows+new_rows+1):
            row_index = row_id - (n_rows+1)
            row_dict['rowid'] = row_id
            all_rows_dict = {}
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
            row_dict["data"] = row_data
            all_rows_dict[order_id] = row_dict
            all_rows_dict = sort_dict(all_rows_dict)
        for curr_row_key in all_rows_dict.keys():
            curr_row_dict = all_rows_dict[curr_row_key]
            mongo_client.checklist_data.insert_one(curr_row_dict)

        mongo_client.checklists.update_one({'checklist_id': checklist_id}, {
            "$set": {'data': checklist_column_data_all, 'columns':total_cols, 'rows': n_rows+new_rows}})

        return ui_utils.handle_response(class_name, data='success', success=True)



class GetCampaignChecklists(APIView):
    # used for getting a list of all checklists of a campaign
    def get(self, request, campaign_id):
        class_name = self.__class__.__name__
        checklist_object = mongo_client.checklists.find({"campaign_id": campaign_id, "status": "active"})
        checklist_data = list(checklist_object)
        checklist_type = str(request.query_params.get('query_type')) if request.query_params.get('query_type') \
            else 'list'
        checklists = []
        is_template = True if checklist_type == 'template' else False
        for curr_checklist in checklist_data:
            if curr_checklist['is_template'] == is_template:
                del curr_checklist['_id']
                checklists.append(curr_checklist)
        # checklist_dict = []
        # for item in checklists:
        #     list_item = ChecklistSerializer(item).data
        #     checklist_dict.append(list_item)
        return ui_utils.handle_response(class_name, data=checklists, success=True)


class GetSupplierChecklists(APIView):
    # used for getting a list of all checklists of a campaign
    def get(self, request, campaign_id, supplier_id):
        class_name = self.__class__.__name__
        checklist_object = mongo_client.checklists.find({'campaign_id': campaign_id, 'supplier_id': supplier_id,
                                                         'status': 'active'})
        checklist_data = list(checklist_object)
        checklist_type = str(request.query_params.get('query_type')) if request.query_params.get('query_type') \
            else 'list'
        checklists = []
        is_template = True if checklist_type == 'template' else False
        for curr_checklist in checklist_data:
            curr_checklist['id'] = curr_checklist['checklist_id']
            if curr_checklist['is_template'] == is_template:
                del curr_checklist['_id']
                checklists.append(curr_checklist)
        # checklist_dict = []
        # for item in checklists:
        #     list_item = ChecklistSerializer(item).data
        #     checklist_dict.append(list_item)
        return ui_utils.handle_response(class_name, data=checklists, success=True)


class FreezeChecklist(APIView):
    @staticmethod
    def put(request,checklist_id, state):
        current_data = mongo_client.checklists.find_one({"checklist_id": int(checklist_id)})
        current_status = current_data['status']
        if current_status == 'inactive':
            response = 'checklist is already deleted'
            return ui_utils.handle_response({}, data=response, success=False)
        if current_status == 'active':
            if state == '0':
                response = 'checklist is already active'
                return ui_utils.handle_response({}, data=response, success=False)
            if state == '1':
                mongo_client.checklists.update_one({"checklist_id": int(checklist_id)},  {"$set": {'status': 'frozen'}})
        if current_status == 'frozen':
            if state == '0':
                mongo_client.checklists.update_one({"checklist_id": int(checklist_id)}, {"$set": {'status': 'active'}})
            if state == '1':
                response = 'checklist is already frozen'
                return ui_utils.handle_response({}, data=response, success=False)
        return ui_utils.handle_response({}, data='success', success=True)

class GetChecklistData(APIView):
    @staticmethod
    def get(request, checklist_id):
        checklist_id = int(checklist_id)
        checklist_info = mongo_client.checklists.find_one({"checklist_id": checklist_id})
        if checklist_info is None:
            return ui_utils.handle_response({}, data="incorrect checklist id", success=False)
        elif checklist_info['status']=='inactive':
            return ui_utils.handle_response({}, data="checklist already deleted", success=False)
        checklist_dict = {
            "checklist_type": checklist_info['checklist_type'],
            "campaign_id": checklist_info['campaign_id'],
            "rows": checklist_info['rows'],
            "supplier_id": checklist_info['supplier_id'],
            "checklist_name": checklist_info['checklist_name'],
            "is_template": checklist_info['is_template'],
            "checklist_id": checklist_info['checklist_id'],
        }
        checklist_data = list(mongo_client.checklist_data.find({"checklist_id": checklist_id}))
        values = []
        column_headers = []
        row_headers = []
        checklist_info_columns = checklist_info['data']
        columns_list = checklist_info_columns.keys()
        for column in columns_list:
            column_headers.append(checklist_info_columns[column])
        for checklist in checklist_data:
            row_id = checklist['rowid']
            if checklist['status']=='inactive':
                print("# row already deleted: ", row_id)
                continue
            curr_row_data = checklist['data']
            curr_row_columns = curr_row_data.keys()
            for column in curr_row_columns:
                value = curr_row_data[column]["cell_value"]
                column_id = column
                if column == '1':
                    row_headers.append({
                        "cell_value": value,
                        "row_id": row_id
                    })
                else:
                    values.append({
                        "row_id": row_id,
                        "value": value,
                        "column_id": int(column_id)
                    })
        final_data = {'values': values, 'column_headers': column_headers, 'row_headers': row_headers, 'checklist_info': checklist_dict}
        return ui_utils.handle_response({}, data=final_data, success=True)


class DeleteChecklist(APIView):
    # deactivating a full checklist
    @staticmethod
    def put(request,checklist_id):
        checklist_info = mongo_client.checklists.find_one({"checklist_id": int(checklist_id)})
        success = False
        if checklist_info is None:
            return ui_utils.handle_response({}, data='checklist does not exist', success=success)
        checklist_status = checklist_info['status'] if 'status' in checklist_info else 'active'
        if checklist_status == 'inactive':
            data = 'checklist is already deleted'
        elif checklist_status == 'frozen':
            data = "checklist is frozen, cannot be modified"
        else:
            mongo_client.checklists.update_one({"checklist_id": int(checklist_id)},  {"$set": {'status': 'inactive'}})
            data = 'success'
            success = True
        return ui_utils.handle_response({}, data=data, success=success)

class DeleteChecklistRow(APIView):

    @staticmethod
    def put(request, checklist_id, row_id):
        mongo_client.checklist_data.update_one({"checklist_id": int(checklist_id), "rowid": int(row_id)},
                                               {"$set": {'status': 'inactive'}})
        return ui_utils.handle_response({}, data='success', success=True)


