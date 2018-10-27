from rest_framework.views import APIView
from models import Checklist, ChecklistColumns, ChecklistData
from serializers import ChecklistSerializer, ChecklistColumnsSerializer, ChecklistDataSerializer
import v0.ui.utils as ui_utils
from celery import shared_task
from v0.ui.common.models import mongo_client, mongo_test
import datetime

# class CreateChecklistTemplate(APIView):
#     def post(self, request, campaign_id):
#         """
#         :param request:
#         :return:
#         """
#         class_name = self.__class__.__name__
#         checklist_name = request.data['checklist_name']
#         checklist_columns = request.data['checklist_columns']
#         checklist_type = request.data['checklist_type']
#         static_column_values = request.data['static_column_values']
#         supplier_id = request.data['supplier_id'] if checklist_type == 'supplier'else None
#         is_template = True if "is_template" in request.data and request.data['is_template'] == 1 else False
#         rows = len(static_column_values)
#         new_form = Checklist(**{
#             'campaign_id': campaign_id,
#             'checklist_name': checklist_name,
#             'status': 'active',
#             'supplier_id': supplier_id,
#             'checklist_type': checklist_type,
#             'rows': rows,
#             'is_template': is_template
#         })
#         new_form.save()
#         form_columns_list = []
#         item_id = 1
#         checklist_id = new_form.__dict__['id']
#         created_at = new_form.__dict__['created_at']
#         updated_at = new_form.__dict__['updated_at']
#         for column in checklist_columns:
#             form_columns_list.append(ChecklistColumns(**{
#                 "checklist_id": checklist_id,
#                 "created_at": created_at,
#                 "updated_at": updated_at,
#                 "column_name": column["column_name"],
#                 "column_type": column["column_type"],
#                 "column_options": column["column_options"] if "column_options" in column else None,
#                 "order_id": column["order_id"],
#                 "column_id": item_id,
#                 "status": 'active'
#             }))
#             item_id = item_id + 1
#         ChecklistColumns.objects.bulk_create(form_columns_list)
#         static_rows_list = []
#         for row in static_column_values:
#             static_rows_list.append(ChecklistData(**{
#                 "checklist_id": checklist_id,
#                 "created_at": created_at,
#                 "updated_at": updated_at,
#                 "supplier_id": supplier_id,
#                 "cell_value": row["cell_value"],
#                 "row_id": row["row_id"],
#                 "column_id": 1, # first column is static by default
#                 "status": 'active'
#             }))
#         ChecklistData.objects.bulk_create(static_rows_list)
#         return ui_utils.handle_response({}, data='success', success=True)


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
        static_column_values = request.data['static_column_values']
        last_id_data = mongo_client.checklists.find_one(sort=[('checklist_id', -1)])
        last_id = last_id_data['checklist_id']
        supplier_id = request.data['supplier_id'] if checklist_type == 'supplier'else None
        is_template = True if "is_template" in request.data and request.data['is_template'] == 1 else False
        rows = len(static_column_values)
        mongo_form = {
            'checklist_id': last_id + 1,
            'campaign_id': campaign_id,
            'checklist_name': checklist_name,
            'status': 'active',
            'supplier_id': supplier_id,
            'checklist_type': checklist_type,
            'rows': rows,
            'is_template': is_template,
            'data': {}
        }
        #mongo_client.checklist.insert_one(mongo_form)
        column_id = 0
        for column in checklist_columns:
            column_id = column_id + 1
            column_options = column['column_options'] if 'column_options' in column else None
            if column_options and not isinstance(column_options, list):
                column_options = column_options.split(',')
                column['column_options'] = column_options
            column['column_id'] = column_id
            mongo_form['data'][str(column_id)] = column
        mongo_client.checklists.insert_one(mongo_form)
        return ui_utils.handle_response({}, data='success', success=True)


def enter_row_to_mongo(checklist_data, supplier_id, campaign_id, checklist):
    all_checklist_columns_dict = checklist['data']
    checklist_id = checklist['checklist_id']
    timestamp = datetime.datetime.utcnow()
    rows = checklist_data.keys()
    #exist_row_data = mongo_client.checklist_data.find({"checklist_id":13},{'_id':0, 'rowid':1})
    exist_rows = mongo_client.checklist_data.find({"checklist_id": 13}).distinct("rowid")
    for curr_row in rows:
        rowid = int(curr_row)
        if rowid in exist_rows:
            print checklist_id, rowid
            mongo_client.checklist_data.delete_one({'checklist_id': int(checklist_id), 'rowid': rowid})
        row_data = checklist_data[curr_row]
        row_dict = {"data": {}, "created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                    "checklist_id": checklist_id, "rowid": rowid, "status": "active"}
        columns = row_data.keys()
        for column in columns:
            column_data = row_data[column]
            if "cell_value" not in column_data:
                continue
            column_id = column_data["column_id"]
            column_name = all_checklist_columns_dict[str(column_id)]["column_name"]
            column_type = all_checklist_columns_dict[str(column_id)]["column_type"]
            value = column_data["cell_value"]
            # row_dict["data"].append({
            #     'column_name': column_name,
            #     'cell_value': value,
            #     'column_id': column_id,
            #     'column_type': column_type
            # })

            row_dict['data']['column_id'] = {
                'column_name': column_name,
                'cell_value': value,
                'column_id': column_id,
                'column_type': column_type
            }
        mongo_client.checklist_data.insert_one(row_dict).inserted_id
    #mongo_client.checklists.update_one({'checklist_id': int(checklist_id)}, {'$inc': {'rows': 1}})
    return


# class ChecklistEntry(APIView):
#     # used to create and update checklist elements
#     def put(self, request, checklist_id):
#         """
#         :param request:
#         :return:
#         """
#         checklist_rows = []
#         checklist_info = Checklist.objects.get(id=checklist_id)
#         #row_id = checklist_info.last_entry_id + 1 if checklist_info.last_row_id else 1
#         #checklist_type = checklist_info.checklist_type
#         if checklist_info.status=='inactive':
#             data = 'deleted checklist'
#             success = False
#         elif checklist_info.is_template == 1:
#             data = 'checklist is a template'
#             success = False
#         else:
#             supplier_id = checklist_info.supplier_id if checklist_info.checklist_type == 'supplier' else None
#             rows_data = request.data
#             #checklist_data = request.data["row_data"]
#             rows = dict.keys(rows_data)
#             checklist_entry_list = []
#             for row_id_str in rows:
#                 row_data = rows_data[row_id_str]
#                 row_id = int(row_id_str)
#                 columns = dict.keys(row_data)
#                 for column_id_str in columns:
#                     item = row_data[column_id_str]
#                     column_id = int(column_id_str)
#                     if item['column_id'] == 1:
#                         print "Cannot edit static column"
#                         continue
#                     row = (ChecklistData(**{
#                         "checklist_id": checklist_info.id,
#                         "column_id": column_id,
#                         "cell_value": item["cell_value"],
#                         "status": "active",
#                         "supplier_id": supplier_id,
#                         "row_id": row_id
#                     }))
#                     checklist_entry_list.append(row)
#                     row.save()
#
#             #checklist_info.last_row_id = row_id
#             checklist_info.save()
#             data = 'success'
#             success = True
#         return ui_utils.handle_response({}, data=data, success=success)



class ChecklistEntry(APIView):
    # used to create and update checklist elements
    def post(self, request, checklist_id):
        checklist = mongo_client.checklists.find_one({"checklist_id": int(checklist_id)})

        if checklist['status']=='inactive':
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
            #row_id = checklist['rows'] + 1 if checklist['rows'] is not None else 1
            enter_row_to_mongo(rows_data, supplier_id, campaign_id, checklist)
            data = 'success'
            success = True

        # lead_form = mongo_client.leads_forms.find_one({"leads_form_id": int(leads_form_id)})
        # entry_id = lead_form['last_entry_id'] + 1 if 'last_entry_id' in lead_form else 1
        # campaign_id = lead_form['campaign_id']
        # lead_data = request.data["leads_form_entries"]
        # enter_lead_to_mongo(lead_data, supplier_id, campaign_id, lead_form, entry_id)
        return ui_utils.handle_response({}, data=data, success=success)


class ChecklistEdit(APIView):
    def post(self, request, checklist_id):
        class_name = self.__class__.__name__
        columns = request.data['columns']
        static_column = request.data['static_column']
        n_rows = len(static_column)
        n_cols = len(columns)
        column_ids = [x["column_id"] for x in columns]
        for column in columns:
            column_id = column['column_id']
            column_data = ChecklistColumns.objects.get(column_id=column_id, checklist_id = checklist_id)
            column_data.column_name = column['column_name']
            column_data.column_type = column['column_type']
            column_data.save()
        for row in static_column:
            row_id = row['row_id']
            row_data = ChecklistData.objects.get(row_id=row_id, column_id = 1, checklist_id = checklist_id)
            row_data.cell_value = row['cell_value']
            row_data.save()
        return ui_utils.handle_response({}, data='success', success=True)


class GetCampaignChecklists(APIView):
    # used for getting a list of all checklists of a campaign
    def get(self, request, campaign_id):
        checklist_type = request.query_params.get('query_type')
        checklists = Checklist.objects.filter(campaign_id = campaign_id).exclude(status='inactive')
        if checklist_type == 'list':
            checklists = checklists.exclude(is_template=1)
        if checklist_type == 'template':
            checklists = checklists.filter(is_template=1)

        checklist_dict = []
        for item in checklists:
            list_item = ChecklistSerializer(item).data
            checklist_dict.append(list_item)
        return ui_utils.handle_response({}, data=checklist_dict, success=True)


class GetSupplierChecklists(APIView):
    # used for getting a list of all checklists of a particular supplier within a campaign
    def get(self, request, campaign_id, supplier_id):
        checklists = Checklist.objects.filter(campaign_id=campaign_id, supplier_id = supplier_id).exclude(status='inactive')
        checklist_type = request.query_params.get('query_type')
        if checklist_type == 'list':
            checklists = checklists.exclude(is_template=1)
        if checklist_type == 'template':
            checklists = checklists.filter(is_template=1)

        checklist_dict = []
        for item in checklists:
            list_item = ChecklistSerializer(item).data
            checklist_dict.append(list_item)
        return ui_utils.handle_response({}, data=checklist_dict, success=True)

class GetChecklistData(APIView):
    # viewing a particular checklist
    @staticmethod
    def get(request,checklist_id):
        checklist_info = Checklist.objects.get(id=checklist_id)
        last_entry_id = checklist_info.rows
        checklist_columns = ChecklistColumns.objects.filter(checklist_id=checklist_id).exclude(status='inactive')
        checklist_data = ChecklistData.objects.filter(checklist_id=checklist_id).exclude(status='inactive')
        checklist_rows = []

        values = []
        checklist_items_dict = {}
        checklist_items_dict_part = []
        for item in checklist_columns:
            curr_item = ChecklistColumnsSerializer(item).data
            checklist_items_dict[item.column_id] = curr_item
            curr_item_part = {key:curr_item[key] for key in ['column_id', 'column_name', 'column_type']}
            checklist_items_dict_part.append(curr_item_part)

        rows = []
        row_labels = checklist_data.filter(column_id = 1).values('row_id','cell_value')
        for row in row_labels:
            rows.append(row)

        previous_entry_id = -1
        current_list = []
        for i in range(1, last_entry_id+1):
            entry_data = checklist_data.filter(row_id = i).exclude(column_id=1)
           # if entry_data is not None:
            for keys in checklist_columns:
                key_name = keys.column_name
                item_id = keys.column_id
                key_query = entry_data.filter(column_id=item_id).first()
                if (not key_query):
                    continue
                key_value = key_query.cell_value
                #current_row[key_name] = key_value
                current_row = ({
                    "row_id": i,
                    "column_id": item_id,
                    "value": key_value
                })
                if i != previous_entry_id and current_list != []:
                    values.append(current_list)
                    current_list = []
                # current_list.append(current_row)
                previous_entry_id = i
                values.append(current_row)

        all_data = {
            'column_headers': checklist_items_dict_part,
            'row_headers': rows,
            'values': values,
        }

        return ui_utils.handle_response({}, data=all_data, success=True)

class DeleteChecklist(APIView):
    # deactivating a full checklist
    @staticmethod
    def put(request,checklist_id):
        checklist_details = Checklist.objects.get(id=checklist_id)
        checklist_details.status = 'inactive'
        checklist_details.save()
        return ui_utils.handle_response({}, data='success', success=True)

class DeleteChecklistColumns(APIView):
    def put (self, request, checklist_id, column_id):
        checklist_item = ChecklistColumns.objects.get(checklist_id=checklist_id, column_id=column_id)
        checklist_item.status = 'inactive'
        checklist_item.save()
        return ui_utils.handle_response({}, data='success', success=True)

class DeleteChecklistRow(APIView):
    @staticmethod
    def put(request, checklist_id, row_id):
        entry_list = ChecklistData.objects.filter(checklist_id=checklist_id, row_id=row_id)
        for item in entry_list:
            item.status = 'inactive'
            item.save()
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
