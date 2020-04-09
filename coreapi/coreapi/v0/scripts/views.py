import csv
import os, sys
from rest_framework.views import APIView

from .utils import create_supplier_id, create_random_supplier_id
from v0.ui.utils import handle_response, get_model, fetch_content_type
from v0.ui.account.models import ContactDetails
from v0.ui.supplier.models import SupplierTypeSociety
from v0.ui.proposal.models import ShortlistedSpaces


class UpdateSupplierContactDataImport(APIView):
    def post(self, request):
        try:
            data = request.data
            updated_contact_file = open(os.path.join(sys.path[0], "updated_contact.txt"), "a")
            new_contact_file = open(os.path.join(sys.path[0], "new_contact.txt"), "a")
            for supplier in data:
                supplier_id = supplier['supplier_id']
                contact_number = supplier['contact_number']
                contact_name = supplier['contact_name'].title()
                designation = supplier['designation'].title()
                print(supplier_id, contact_number, contact_name, designation)
                try:
                    if contact_number and supplier_id:
                        # Check contact number in contact details
                        contact_details = ContactDetails.objects.filter(mobile=contact_number, object_id=supplier_id)
                        if contact_details:
                            if contact_name and designation:
                                contact_details.update(name=contact_name, contact_type=designation)
                                updated_contact_file.write(
                                    "{mobile},{name},{id}\n".format(mobile=contact_number, name=contact_name, id=supplier_id))
                        else:
                            contact_details = ContactDetails(object_id=supplier_id, name=contact_name, contact_type=designation, mobile=contact_number)
                            contact_details.save()
                            new_contact_file.write(
                                "{mobile},{name},{id}\n".format(mobile=contact_number, name=contact_name, id=supplier_id))
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        return handle_response({}, data='Data updated successfully', success=True)


class CreateSupplierWithContactDetails(APIView):
    def post(self, request):
        try:
            supplier_ids = request.data['supplier_ids']
            not_updated_file = open(os.path.join(sys.path[0], "supplier_not_created.txt"), "a")

            supplier_type_code = request.data['supplier_type_code']
            model = get_model(supplier_type_code)
            content_type = fetch_content_type(supplier_type_code)
            # Get sheet
            this_folder = os.path.dirname(os.path.abspath(__file__))
            my_file = os.path.join(this_folder, 'contact_details.csv')
            with open(my_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    supplier_name = row[0] if row[0] else None
                    city = row[1] if row[1] else None
                    area = row[2] if row[2] else None
                    subarea = row[3] if row[3] else None
                    contact_name = row[4] if row[4] else None
                    contact_number = row[5] if row[5] else None
                    designation = row[6] if row[6] else None
                    supplier_type_code = row[7] if row[7] else None
                    # First check supplier id in list of supplier ids
                    if not supplier_name or not city or not area or not subarea:
                        # Write suppliers which are not created
                        not_updated_file.write(str(row) + '\n')
                    supplier_id = create_supplier_id(supplier_name, city, area, subarea, supplier_type_code)
                    if supplier_id not in supplier_ids:
                        already_existing_supplier_id = model.objects.filter(supplier_id=supplier_id).values('supplier_id')
                    if already_existing_supplier_id:
                        # create new supplier id
                        supplier_id = create_random_supplier_id(supplier_name, city, area, subarea, supplier_type_code)
                    print(supplier_id)
                    # Append supplier id in supplier ids
                    supplier_ids.append(supplier_id)
                    print(supplier_ids)
                    # Create data in supplier & contact details
                    if supplier_type_code == 'RS':
                        supplier_details = model(supplier_id=supplier_id,
                                                 society_name=supplier_name,
                                                 society_city=city,
                                                 society_locality=area,
                                                 society_subarea=subarea)
                        supplier_details.save()
                        if supplier_details:
                            # Update contact details
                            contact_details = ContactDetails(supplier_id=supplier_id,
                                                             name=contact_name,
                                                             mobile=contact_number,
                                                             contact_type=designation)
                            contact_details.save()
        except Exception as e:
            print(e)
        return handle_response({}, data='Supplier created successfully', success=True)


class DeleteDuplicateSocieties(APIView):
    def post(self, request):
        try:
            data = request.data
            deleted_societies_file = open(os.path.join(sys.path[0], "deleted_societies.txt"), "a")
            societies_not_deleted_file = open(os.path.join(sys.path[0], "societies_not_deleted.txt"), "a")
            for supplier in data:
                supplier_id = supplier['supplier_id']
                supplier_name = supplier.get('supplier_name', '')
                if supplier_id:
                    supplier_society = SupplierTypeSociety.objects.filter(supplier_id=supplier_id)
                    if not supplier_society:
                        print('Society not present')
                        continue
                    # Supplier in proposal
                    shortlisted_spaces = ShortlistedSpaces.objects.filter(object_id=supplier_id)
                    if shortlisted_spaces:
                        societies_not_deleted_file.write("{name},{id}\n".format(name=supplier_name, id=supplier_id))
                        print('Linked to proposal :', supplier_id)
                    else:
                        supplier_society = SupplierTypeSociety.objects.filter(supplier_id=supplier_id).delete()
                        if supplier_society:
                            deleted_societies_file.write("{name},{id}\n".format(name=supplier_name, id=supplier_id))
        except Exception as e:
            print(e)
        return handle_response({}, data='Societies deleted successfully', success=True)
