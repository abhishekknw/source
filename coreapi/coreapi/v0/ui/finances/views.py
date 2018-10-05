from rest_framework.views import APIView
import v0.ui.utils as ui_utils
import v0.constants as v0_constants
import v0.ui.website.utils as website_utils
from django.db import transaction
import openpyxl


class ImportProposalCostData(APIView):
    """
    The class is responsible for importing proposal cost data from an excel sheet.
    All the import api's heavily depend upon the structure of the sheet which it's importing.
    so if you are trying to understand what this api does, understand the structure of the sheet first.

    two phases: data collection and data insertion.
    """
    def post(self, request, proposal_id):

        class_name = self.__class__.__name__

        if not request.FILES:
            return ui_utils.handle_response(class_name, data='No files found')

        file = request.FILES['file']
        # load the workbook
        wb = openpyxl.load_workbook(file)
        # read the sheet
        ws = wb.get_sheet_by_name(v0_constants.metric_sheet_name)

        # before inserting delete all previous data as we don't want to duplicate things.
        response = website_utils.delete_proposal_cost_data(proposal_id)
        if not response.data['status']:
            return response

        with transaction.atomic():
            try:
                count = 0
                master_data = {}
                # DATA COLLECTION  in order to  collect data in master_data, initialize with proper data structures
                master_data = website_utils.initialize_master_data(master_data)
                for index, row in enumerate(ws.iter_rows()):

                    # ignore empty rows
                    if website_utils.is_empty_row(row):
                        continue
                    # send one row for processing
                    response = website_utils.handle_offline_pricing_row(row, master_data)
                    if not response.data['status']:
                        return response
                    # update master_data with response
                    master_data = response.data['data']
                    count += 1

                # DATA INSERTION time to save the data
                master_data['proposal_master_cost']['proposal'] = proposal_id
                response = website_utils.save_master_data(master_data)
                if not response.data['status']:
                    return response
                return ui_utils.handle_response(class_name, data='successfully imported.Saved {0} rows'.format(count),
                                                success=
                                                True)
            except Exception as e:
                return ui_utils.handle_response(class_name, exception_object=e, request=request)

