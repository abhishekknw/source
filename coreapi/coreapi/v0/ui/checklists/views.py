from rest_framework.views import APIView
from models import Checklist, ChecklistColumns, ChecklistData
from serializers import ChecklistSerializer, ChecklistColumnsSerializer, ChecklistDataSerializer
import v0.ui.utils as ui_utils

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
        supplier_id = request.data['supplier_id'] if checklist_type == 'supplier'else None
        is_template = True if "is_template" in request.data and request.data['is_template'] == 1 else False
        rows = len(static_column_values)
        new_form = Checklist(**{
            'campaign_id': campaign_id,
            'checklist_name': checklist_name,
            'status': 'active',
            'supplier_id': supplier_id,
            'checklist_type': checklist_type,
            'rows': rows,
            'is_template': is_template
        })
        new_form.save()
        form_columns_list = []
        item_id = 1
        checklist_id = new_form.__dict__['id']
        created_at = new_form.__dict__['created_at']
        updated_at = new_form.__dict__['updated_at']
        for column in checklist_columns:
            form_columns_list.append(ChecklistColumns(**{
                "checklist_id": checklist_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "column_name": column["column_name"],
                "column_type": column["column_type"],
                "column_options": column["column_options"] if "column_options" in column else None,
                "order_id": column["order_id"],
                "column_id": item_id,
                "status": 'active'
            }))
            item_id = item_id + 1
        ChecklistColumns.objects.bulk_create(form_columns_list)
        static_rows_list = []
        for row in static_column_values:
            static_rows_list.append(ChecklistData(**{
                "checklist_id": checklist_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "supplier_id": supplier_id,
                "cell_value": row["cell_value"],
                "row_id": row["row_id"],
                "column_id": 1, # first column is static by default
                "status": 'active'
            }))
        ChecklistData.objects.bulk_create(static_rows_list)
        return ui_utils.handle_response({}, data='success', success=True)



class ChecklistEntry(APIView):
    # used to create and update checklist elements
    def put(self, request, checklist_id):
        """
        :param request:
        :return:
        """
        checklist_rows = []
        checklist_info = Checklist.objects.get(id=checklist_id)
        #row_id = checklist_info.last_entry_id + 1 if checklist_info.last_row_id else 1
        #checklist_type = checklist_info.checklist_type
        if checklist_info.status=='inactive':
            data = 'deleted checklist'
            success = False
        elif checklist_info.is_template == 1:
            data = 'checklist is a template'
            success = False
        else:
            supplier_id = checklist_info.supplier_id if checklist_info.checklist_type == 'supplier' else None
            rows_data = request.data
            #checklist_data = request.data["row_data"]
            rows = dict.keys(rows_data)
            checklist_entry_list = []
            for row_id_str in rows:
                row_data = rows_data[row_id_str]
                row_id = int(row_id_str)
                columns = dict.keys(row_data)
                for column_id_str in columns:
                    item = row_data[column_id_str]
                    column_id = int(column_id_str)
                    if item['column_id'] == 1:
                        print "Cannot edit static column"
                        continue
                    row = (ChecklistData(**{
                        "checklist_id": checklist_info.id,
                        "column_id": column_id,
                        "cell_value": item["cell_value"],
                        "status": "active",
                        "supplier_id": supplier_id,
                        "row_id": row_id
                    }))
                    checklist_entry_list.append(row)
                    row.save()

            #checklist_info.last_row_id = row_id
            checklist_info.save()
            data = 'success'
            success = True
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
            curr_item_part = {key:curr_item[key] for key in ['column_id', 'column_name']}
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
                current_list.append(current_row)
                previous_entry_id = i
        values.append(current_list)

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