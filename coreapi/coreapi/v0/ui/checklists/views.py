from rest_framework.views import APIView
from models import Checklist, ChecklistColumns, ChecklistData
from serializers import ChecklistSerializer, ChecklistColumnsSerializer, ChecklistDataSerializer
import v0.ui.utils as ui_utils
from celery import shared_task
from v0.ui.common.models import mongo_client, mongo_test
import datetime

def insert_static_cols(row_dict_original,static_column_values, static_column_names, static_column_types, lower_level_checklists):
    row_dict_array = []
    #lower_level_rows = list(set([x["parent_row_id"] for x in lower_level_checklists]))
    if isinstance(static_column_values, dict):
        static_column_ids = [int(x) for x in static_column_values.keys()]
    else:
        static_column_ids = [1]
        static_column_values = {"1": static_column_values}

    static_data = {}
    first_column_rows = static_column_values["1"]

    counter = 0

    for curr_row in first_column_rows:
        rowid = curr_row["row_id"]
        row_dict = row_dict_original.copy()
        row_dict["rowid"] = rowid
        cell_value = curr_row['cell_value']

        #if curr_row in lower_level_rows:
        lower_level_array = [x['static_column_values'] for x in lower_level_checklists
                                            if x['parent_row_id']==rowid]
        lower_level_static_column_values = lower_level_array[0] if len(lower_level_array)>0 else {}

        for static_column in static_column_ids:
            static_column_str = str(static_column)
            if static_column > 1:
                curr_static_column_values = static_column_values[static_column_str]
                cell_value = [x["cell_value"] for x in curr_static_column_values if x["row_id"] == rowid][0]
            static_data[static_column_str] = {
                "cell_value": cell_value,
                "column_id": static_column,
                "column_type": static_column_types[static_column_str],
                "column_name": static_column_names[static_column_str]
            }
            if static_column_str in lower_level_static_column_values.keys():
                lower_level_row_values = lower_level_static_column_values[static_column_str]
                static_data[static_column_str]["lower_level_row_values"] = lower_level_row_values

        row_dict["data"] = static_data
        mongo_client.checklist_data.insert_one(row_dict)
    return

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
        static_column_indices = static_column_values.keys()
        lower_level_checklists = []
        if 'lower_level_checklists' in request.data:
            lower_level_checklists = request.data['lower_level_checklists']

        if isinstance(static_column_values, dict):
            static_column_ids = [int(x) for x in static_column_values.keys()]
            static_column_number = len(static_column_ids)
        else:
            static_column_ids = [1]
            static_column_values = {"1":static_column_values}

        last_id_data = mongo_client.checklists.find_one(sort=[('checklist_id', -1)])
        last_id = last_id_data['checklist_id'] if last_id_data is not None else 0
        supplier_id = request.data['supplier_id'] if checklist_type == 'supplier'else None
        is_template = True if "is_template" in request.data and request.data['is_template'] == 1 else False
        rows = len(static_column_values)
        checklist_id = last_id + 1
        mongo_form = {
            'checklist_id': checklist_id,
            'campaign_id': campaign_id,
            'checklist_name': checklist_name,
            'status': 'active',
            'supplier_id': supplier_id,
            'checklist_type': checklist_type,
            'rows': rows,
            'is_template': is_template,
            'data': {},
            'univalue_items': univalue_items,
            'static_columns': static_column_indices
        }
        column_id = 0
        static_column_names = {}
        static_column_types = {}
        for column in checklist_columns:
            column_id = column_id + 1
            column_options = column['column_options'] if 'column_options' in column else None
            if column_options and not isinstance(column_options, list):
                column_options = column_options.split(',')
                column['column_options'] = column_options
            column['column_id'] = column_id
            mongo_form['data'][str(column_id)] = column
            # if column_id == 1:
            #     first_column_name = column['column_name']
            #     first_column_type = column['column_type']
            if column_id in static_column_ids:
                static_column_names[str(column_id)] = column['column_name']
                static_column_types[str(column_id)] = column['column_type']
        mongo_client.checklists.insert_one(mongo_form)
        timestamp = datetime.datetime.utcnow()

        row_dict = {"created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                        "checklist_id": checklist_id, "status": "active"}

        insert_static_cols(row_dict,static_column_values, static_column_names, static_column_types, lower_level_checklists)

        # for static_column in static_column_ids:
        #     static_column_str = str(static_column)
        #     curr_static_column_values = static_column_values[static_column_str]
        #     for curr_row in curr_static_column_values:
        #         rowid = curr_row["row_id"]
        #         #rows_data[str(rowid)]
        #         cell_value = curr_row["cell_value"]
        #
        #         static_data[static_column_str] = {
        #             "cell_value": cell_value,
        #             "column_id": static_column,
        #             "column_type": static_column_types[static_column_str],
        #             "column_name": static_column_names[static_column_str]
        #         }
        #         row_dict["data"] = static_data

        return ui_utils.handle_response({}, data='success', success=True)


def enter_row_to_mongo(checklist_data, supplier_id, campaign_id, checklist):
    all_checklist_columns_dict = checklist['data']
    checklist_id = checklist['checklist_id']
    static_columns = checklist['static_columns'] if 'static_columns' in checklist else ["1"]
    timestamp = datetime.datetime.utcnow()
    rows = checklist_data.keys()
    exist_rows_query = mongo_client.checklist_data.find({"checklist_id": checklist_id})
    exist_rows_list = list(exist_rows_query)
    exist_rows = exist_rows_query.distinct("rowid")

    for curr_row in rows:
        rowid = int(curr_row)
        exist_row_data = []
        if rowid in exist_rows:
            exist_row_data = [x['data'] for x in exist_rows_list if x['rowid'] == rowid][0]
            mongo_client.checklist_data.delete_one({'checklist_id': int(checklist_id), 'rowid': rowid})
        new_row_data = checklist_data[curr_row]

        row_dict = {"data": {}, "created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                    "checklist_id": checklist_id, "rowid": rowid, "status": "active"}

        for static_column in static_columns:
            row_dict['data'][static_column] = exist_row_data[static_column]
        columns = new_row_data.keys()
        for column in columns:
            column_data = new_row_data[column]
            if "cell_value" not in column_data:
                continue
            column_id = column_data["column_id"]
            if str(column_id) in static_columns:
                print 'cannot edit static column', column_id
                continue
            column_name = all_checklist_columns_dict[str(column_id)]["column_name"]
            column_type = all_checklist_columns_dict[str(column_id)]["column_type"]
            value = column_data["cell_value"]

            row_dict['data'][str(column_id)] = {
                'column_name': column_name,
                'cell_value': value,
                'column_id': column_id,
                'column_type': column_type
            }
        mongo_client.checklist_data.insert_one(row_dict).inserted_id
    return


class ChecklistEntry(APIView):
    # used to create and update checklist elements
    def post(self, request, checklist_id):
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
        columns = request.data['columns']
        static_column = request.data['static_column']
        # n_rows = len(static_column)
        # n_cols = len(columns)
        # column_ids = [x["column_id"] for x in columns]
        checklist_column_data_all = list(mongo_client.checklists.find({"checklist_id": checklist_id}))[0]['data']
        checklist_data_all = list(mongo_client.checklist_data.find({"checklist_id": checklist_id}))
        for column in columns:
            column_id = column['column_id']
            new_column_data = column
            new_column_data['order_id'] = checklist_column_data_all[str(column_id)]['order_id']
            checklist_column_data_all[str(column_id)] = new_column_data
            mongo_client.checklists.update_one({'checklist_id': checklist_id}, {
                "$set": {'data': checklist_column_data_all}})
        for row in static_column:
            row_id = row['row_id']
            row_data = [x['data']['1'] for x in checklist_data_all if x['rowid']==row_id][0]
            row_data['cell_value'] = row['cell_value']
            mongo_client.checklist_data.update_one({'rowid':int(row_id), 'checklist_id': checklist_id}, {
                "$set": {'data.1': row_data}})
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
            if curr_checklist['is_template'] == is_template:
                del curr_checklist['_id']
                checklists.append(curr_checklist)
        # checklist_dict = []
        # for item in checklists:
        #     list_item = ChecklistSerializer(item).data
        #     checklist_dict.append(list_item)
        return ui_utils.handle_response(class_name, data=checklists, success=True)


# class GetSupplierChecklists(APIView):
#     # used for getting a list of all checklists of a particular supplier within a campaign
#     def get(self, request, campaign_id, supplier_id):
#         checklists = Checklist.objects.filter(campaign_id=campaign_id, supplier_id = supplier_id).exclude(status='inactive')
#         checklist_type = request.query_params.get('query_type')
#         if checklist_type == 'list':
#             checklists = checklists.exclude(is_template=1)
#         if checklist_type == 'template':
#             checklists = checklists.filter(is_template=1)
#
#         checklist_dict = []
#         for item in checklists:
#             list_item = ChecklistSerializer(item).data
#             checklist_dict.append(list_item)
#         return ui_utils.handle_response({}, data=checklist_dict, success=True)

# class GetChecklistData(APIView):
#     # viewing a particular checklist
#     @staticmethod
#     def get(request,checklist_id):
#         checklist_info = Checklist.objects.get(id=checklist_id)
#         last_entry_id = checklist_info.rows
#         checklist_columns = ChecklistColumns.objects.filter(checklist_id=checklist_id).exclude(status='inactive')
#         checklist_data = ChecklistData.objects.filter(checklist_id=checklist_id).exclude(status='inactive')
#         checklist_rows = []
#
#         values = []
#         checklist_items_dict = {}
#         checklist_items_dict_part = []
#         for item in checklist_columns:
#             curr_item = ChecklistColumnsSerializer(item).data
#             checklist_items_dict[item.column_id] = curr_item
#             curr_item_part = {key:curr_item[key] for key in ['column_id', 'column_name', 'column_type']}
#             checklist_items_dict_part.append(curr_item_part)
#
#         rows = []
#         row_labels = checklist_data.filter(column_id = 1).values('row_id','cell_value')
#         for row in row_labels:
#             rows.append(row)
#
#         previous_entry_id = -1
#         current_list = []
#         for i in range(1, last_entry_id+1):
#             entry_data = checklist_data.filter(row_id = i).exclude(column_id=1)
#            # if entry_data is not None:
#             for keys in checklist_columns:
#                 key_name = keys.column_name
#                 item_id = keys.column_id
#                 key_query = entry_data.filter(column_id=item_id).first()
#                 if (not key_query):
#                     continue
#                 key_value = key_query.cell_value
#                 #current_row[key_name] = key_value
#                 current_row = ({
#                     "row_id": i,
#                     "column_id": item_id,
#                     "value": key_value
#                 })
#                 if i != previous_entry_id and current_list != []:
#                     values.append(current_list)
#                     current_list = []
#                 # current_list.append(current_row)
#                 previous_entry_id = i
#                 values.append(current_row)
#
#         all_data = {
#             'column_headers': checklist_items_dict_part,
#             'row_headers': rows,
#             'values': values,
#         }
#
#         return ui_utils.handle_response({}, data=all_data, success=True)
class GetChecklistData(APIView):
    @staticmethod
    def get(request, checklist_id):
        checklist_id = int(checklist_id)
        checklist_info = mongo_client.checklists.find_one({"checklist_id": checklist_id})
        if checklist_info is None:
            return ui_utils.handle_response({}, data="incorrect checklist id", success=False)
        elif checklist_info['status']=='inactive':
            return ui_utils.handle_response({}, data="checklist already deleted", success=False)
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
                        "column_id": column_id
                    })
        final_data = {'values': values, 'column_headers': column_headers, 'row_headers': row_headers}
        return ui_utils.handle_response({}, data=final_data, success=True)

class DeleteChecklist(APIView):
    # deactivating a full checklist
    @staticmethod
    def put(request,checklist_id):
        mongo_client.checklists.update_one({"checklist_id": int(checklist_id)},  {"$set": {'status': 'inactive'}})
        return ui_utils.handle_response({}, data='success', success=True)


class DeleteChecklistColumns(APIView):
    # this function is being currently skipped because it is too complex
    def put (self, request, checklist_id, column_id):
        checklist_item = ChecklistColumns.objects.get(checklist_id=checklist_id, column_id=column_id)
        checklist_item.status = 'inactive'
        checklist_item.save()
        return ui_utils.handle_response({}, data='success', success=True)

class DeleteChecklistRow(APIView):

    @staticmethod
    def put(request, checklist_id, row_id):
        mongo_client.checklist_data.update_one({"checklist_id": int(checklist_id), "rowid": int(row_id)},
                                               {"$set": {'status': 'inactive'}})
        return ui_utils.handle_response({}, data='success', success=True)


@shared_task()
def migrate_to_mongo():
    all_checklists_data_object = ChecklistData.objects.all()
    all_checklists_data = []
    for data in all_checklists_data_object:
        all_checklists_data.append(data.__dict__)
    all_checklists_forms = Checklist.objects.all().values('id', 'campaign_id', 'rows',
                                                     'status', 'created_at')
    all_checklists_columns = ChecklistColumns.objects.all().values('checklist_id', 'column_id', 'column_name',
                                                                   'column_options', 'order_id', 'status',
                                                                   'column_type')
    all_checklists_columns_dict = {}
    for column in all_checklists_columns:
        if column['checklist_id'] not in all_checklists_columns_dict:
            all_checklists_columns_dict[column['checklist_id']] = []
        all_checklists_columns_dict[column['checklist_id']].append(column)
    for checklist in all_checklists_forms:
        campaign_id = checklist['campaign_id']
        mongo_dict = {
            'checklist_id': checklist['id'],
            'campaign_id': campaign_id,
            'rows': checklist['rows'],
            'status': checklist['status'],
            'created_at': checklist['created_at'],
            'data': {}
        }
        if checklist['id'] in all_checklists_columns_dict:
            curr_checklist_columns = all_checklists_columns_dict[checklist['id']]
            for item in curr_checklist_columns:
                key_options = item['column_options'] if 'key_options' in item else None
                mongo_dict['data'][str(item['column_id'])] = {
                    'column_id': item['column_id'],
                    'column_type': item['column_type'],
                    'column_name': item['column_name'],
                    'column_options': key_options,
                    'order_id': item['order_id'],
                    'status': item['status'],
                    'checklist_id': item['checklist_id'],
                    'campaign_id': campaign_id,
                }
        mongo_client.checklists.insert_one(mongo_dict)
    checklist_ids = all_checklists_data_object.values_list('checklist_id', flat=True).distinct()
    for curr_checklist_id in checklist_ids:
        curr_checklist_data = [x for x in all_checklists_data if x['checklist_id'] == curr_checklist_id]
        #curr_checklist_columns = [x for x in all_checklists_columns_dict.values() if x['checklist_id'] == curr_checklist_id]
        curr_checklist_columns = all_checklists_columns_dict[curr_checklist_id]
        curr_checklists = [x for x in all_checklists_forms if x['id'] == curr_checklist_id]
        first_data_element = curr_checklist_data[0]
        campaign_id = curr_checklists[0]['campaign_id']
        row_ids = list(set([x['row_id'] for x in curr_checklist_data]))
        entry_count = 0
        for curr_row_id in row_ids:
            entry_count = entry_count + 1
            curr_row_data = [x for x in curr_checklist_data if x['row_id'] == curr_row_id]
            supplier_id = curr_row_data[0]['supplier_id']
            created_at = curr_row_data[0]['created_at']
            row_dict = {"data": [], "created_at": created_at, "supplier_id": supplier_id,
                        "campaign_id": campaign_id, "checklist_id": curr_checklist_id, "rowid": curr_row_id,
                        "status": "active"}
            for curr_data in curr_row_data:
                curr_column_id = curr_data['column_id']
                value = curr_data['cell_value']
                curr_item = [x for x in curr_checklist_columns if x['column_id'] == curr_column_id][0]
                column_name = curr_item['column_name']
                column_type = curr_item['column_type']
                item_dict = {
                    'column_id': curr_column_id,
                    'column_name': column_name,
                    'value': value,
                    'column_type': column_type
                }
                row_dict['data'].append(item_dict)
            mongo_client.checklist_data.insert_one(row_dict)
    return


class MigrateChecklistToMongo(APIView):
    def put(self, request):
        class_name = self.__class__.__name__
        migrate_to_mongo()
        return ui_utils.handle_response(class_name, data='success', success=True)
