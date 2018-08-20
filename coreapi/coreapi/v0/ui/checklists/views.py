from rest_framework.views import APIView
from models import Checklist, ChecklistColumns, ChecklistRows, ChecklistData
from serializers import ChecklistSerializer
import v0.ui.utils as ui_utils

class Test(APIView):

    def get(self, request):
        """
        :param request:
        :return:
        """
        return ui_utils.handle_response({}, data="success", success=True)

# class CreateChecklist(APIView):
#     # import checklist template using excel
#     def post(self, request):
#         levels = 2   # will change later
#         source_file = request.data['file']
#         wb = load_workbook(source_file)
#         ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
#         for index, row in enumerate(ws.iter_rows()):
#             if index == 0:


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
        supplier_id = request.data['supplier_id'] if checklist_type == 'supplier'else None
        new_form = Checklist(**{
            'campaign_id': campaign_id,
            'checklist_name': checklist_name,
            'status': 'active',
            'supplier_id': supplier_id,
            'checklist_type': checklist_type
        })
        new_form.save()
        form_items_list = []
        item_id = 1
        checklist_id = new_form.__dict__['id']
        created_at = new_form.__dict__['created_at']
        updated_at = new_form.__dict__['updated_at']
        for item in checklist_columns:
            form_items_list.append(ChecklistColumns(**{
                "checklist_id": checklist_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "key_name": item["key_name"],
                "key_type": item["key_type"],
                "key_options": item["key_options"] if "key_options" in item else None,
                "order_id": item["order_id"],
                "item_id": item_id,
                "status": 'active'
            }))
            item_id = item_id + 1
        ChecklistColumns.objects.bulk_create(form_items_list)
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
        entry_id = checklist_info.last_entry_id + 1 if checklist_info.last_entry_id else 1
        checklist_type = checklist_info.checklist_type
        supplier_id = checklist_info.supplier_id if checklist_info.checklist_type == 'supplier' else None
        checklist_data = request.data
        checklist_entry_list = []
        for item in checklist_data:
            row = (ChecklistData(**{
                "checklist_id": checklist_info.id,
                "item_id": item["item_id"],
                "item_value": item["item_value"],
                "status": "active",
                "supplier_id": supplier_id
            }))
            checklist_entry_list.append(row)
            row.save()

        checklist_info.last_entry_id = entry_id
        checklist_info.save()
        return ui_utils.handle_response({}, data='success', success=True)

class GetCampaignChecklists(APIView):
    # used for getting a list of all checklists of a campaign
    def get(self, request, campaign_id):
        checklists = Checklist.objects.filter(campaign_id = campaign_id)
        checklist_dict = []
        for item in checklists:
            list_item = ChecklistSerializer(item).data
            checklist_dict.append(list_item)
        return ui_utils.handle_response({}, data=checklist_dict, success=True)

class GetSupplierChecklists(APIView):
    # used for getting a list of all checklists of a particular supplier within a campaign
    def get(self, request, campaign_id, supplier_id):
        checklists = Checklist.objects.filter(campaign_id=campaign_id, supplier_id = supplier_id)
        checklist_dict = []
        for item in checklists:
            list_item = ChecklistSerializer(item).data
            checklist_dict.append(list_item)
        return ui_utils.handle_response({}, data=checklist_dict, success=True)


