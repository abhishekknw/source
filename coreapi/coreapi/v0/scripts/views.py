import csv
import os, sys

from django.db.models import Q
from rest_framework.views import APIView

from .utils import create_new_society
from v0.ui.utils import handle_response, get_model, fetch_content_type
from v0.ui.account.models import ContactDetails
from v0.ui.supplier.models import SupplierTypeSociety
from v0.ui.proposal.models import ShortlistedSpaces, BookingStatus, BookingSubstatus, ProposalInfo

from ..ui.common.models import BaseUser


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
                if len(designation) == 0:
                    designation = 'Office'
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
            data = request.data
            not_updated_file = open(os.path.join(sys.path[0], "supplier_not_created.txt"), "a")

            supplier_type_code = 'RS'
            model = get_model(supplier_type_code)
            content_type = fetch_content_type(supplier_type_code)
            supplier_ids = []
            # Get sheet
            with open('supplier_created.csv', mode='a') as supplier_file:
                writer = csv.writer(supplier_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # writer.writerow(['supplier_id', 'name'])
                for supplier in data:
                    supplier_name = supplier['supplier_name'].title()
                    state = supplier['state'].strip()
                    city = supplier['city'].strip()
                    area = supplier['area'].strip()
                    subarea = supplier['subarea'].strip()
                    contact_name = supplier.get('contact_name', None)
                    contact_number = supplier.get('contact_number', None)
                    designation = supplier.get('designation', '').title()
                    latitude = supplier['latitude']
                    longitude = supplier['longitude']
                    tower_count = supplier.get('tower_count', 1)
                    flat_count = supplier.get('flat_count', 1)
                    address = supplier.get('address','').title()
                    zipcode = supplier.get('zipcode', None)
                    contact_email = supplier.get('contact_email', None)

                    supplier_name = supplier_name.strip().lstrip('"').rstrip('"').lstrip(',').rstrip(',')
                    area = area.strip().rstrip(',').lstrip(',')
                    subarea = subarea.strip().rstrip(',').lstrip(',')

                    if len(subarea) == 0:
                        subarea = None
                    if latitude and type(latitude) == str:
                        latitude = latitude.replace(',', '')
                    latitude = float(latitude)
                    if longitude and type(longitude) == str:
                        longitude = longitude.replace(',', '')
                    longitude = float(longitude)

                    if zipcode and type(zipcode) == str:
                        zipcode = zipcode.replace(',', '')
                        zipcode = int(zipcode)

                    if contact_number and type(contact_number) == str:
                        print('inside')
                        if len(contact_number) == 0:
                            contact_number = None
                        contact_number = contact_number.replace('-','')
                        contact_number = contact_number.replace(' ', '')
                        contact_number = contact_number.split('\n')[0]
                        contact_number = contact_number.split('&')[0]
                        contact_number = contact_number.split(',')[0]
                        contact_number = contact_number.split('/')[0]

                    if not contact_number:
                        contact_number = None
                        print(contact_number)

                    if designation and len(designation) == 0:
                        designation = 'Office'

                    if not contact_email or len(contact_email) == 0:
                        contact_email = None
                    else:
                        contact_email = contact_email.strip().rstrip(',').lstrip(',')

                    if tower_count == '':
                        tower_count = 1
                    if flat_count == '':
                        flat_count = None

                    if contact_name is not None:
                        contact_name = contact_name.title()

                    if contact_number is not None:
                        contact_number = int(contact_number)
                    # First check supplier id in list of supplier ids
                    if not supplier_name or not city or not area:
                        # Write suppliers which are not created
                        return handle_response({}, data='Missing fields', success=False)

                    existing_supplier = model.objects.filter(society_name=supplier_name).values('society_locality', 'society_subarea','supplier_id').distinct()

                    # supplier_name = model.objects.filter(Q(society_name=supplier_name) & Q(society_locality=area) | Q(society_subarea=subarea) | Q(society_latitude=latitude) | Q(society_longitude=longitude)).values('society_name', 'supplier_id')
                    # If supplier name, update contact details
                    if len(existing_supplier) > 0:
                        print('society exists')
                        for society in existing_supplier:
                            print(society)
                            print(society['society_locality'])
                            if (society['society_locality'] == area) and (society['society_subarea'] == subarea):
                                # Update contact details
                                contacts = ContactDetails.objects.filter(
                                    object_id=society['supplier_id']).values('mobile')
                                print(contacts)
                                if len(contacts) == 0:
                                    print('no contacts found')
                                    contact_details = ContactDetails(object_id=society['supplier_id'],
                                                                     name=contact_name.strip().rstrip(',').lstrip(','),
                                                                     mobile=contact_number,
                                                                     contact_type=designation.strip().rstrip(',').lstrip(','),
                                                                     email=contact_email
                                                                     )
                                    contact_details.save()
                                else:
                                    if len(contacts) > 0:
                                        is_contact = False
                                        for contact in contacts:
                                            if contact['mobile'] == contact_number:
                                                is_contact = True
                                                print('contact already exists')
                                                continue
                                        if not is_contact:
                                            contact_details = ContactDetails(
                                                object_id=society['supplier_id'],
                                                name=contact_name.strip().rstrip(',').lstrip(','),
                                                mobile=contact_number,
                                                contact_type=designation.strip().rstrip(',').lstrip(',')
                                            )
                                            contact_details.save()
                            else:
                                supplier_details = create_new_society(model, supplier_name, city, area, subarea,
                                                                      supplier_type_code, tower_count, flat_count,
                                                                      latitude, longitude, address, zipcode,
                                                                      supplier_ids, contact_name, contact_number,
                                                                      designation, state)
                                writer.writerow(supplier_details)
                    else:
                        supplier_details = create_new_society(model, supplier_name, city, area, subarea,
                                                              supplier_type_code, tower_count, flat_count,
                                                              latitude, longitude, address, zipcode, supplier_ids,
                                                              contact_name, contact_number, designation, state)
                        writer.writerow(supplier_details)

            return handle_response({}, data=supplier_ids, success=True)
        except Exception as e:
            print('Catching error :', e)
            return handle_response({}, data="Error creating societies", success=False)


class DeleteDuplicateSocieties(APIView):
    def post(self, request):
        try:
            data = request.data
            response = []
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
                        for space in shortlisted_spaces:
                            proposal = ProposalInfo.objects.filter(proposal_id=space.proposal_id)
                            response.append({
                                'supplier_id': supplier_id,
                                'supplier_name': supplier_name,
                                'proposal': proposal[0].name,
                            })
                    else:
                        SupplierTypeSociety.objects.filter(supplier_id=supplier_id).delete()
        except Exception as e:
            print(e)
        return handle_response({}, data=response, success=True)


class DeleteUser(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data)
            for user in data:
                BaseUser.objects.filter(id=user['user_id']).delete()
            return handle_response({}, data={"message": "successfull"}, success=True)
        except Exception as e:
            print(e)
            return handle_response({}, exception_object=e, success=False)


class storeS3UrlToCSV(APIView):
    def post(self, request):
        try:
            data = request.data
            with open('milk-basket-products.csv', mode='a') as products_file:
                writer = csv.writer(products_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['product_id', 'url'])
                for product in data:
                    product_id = product['product_id']
                    url = 'https://milkbasket-product-images.s3.ap-south-1.amazonaws.com/{product_id}.jpg'.format(
                        product_id=product_id)
                    writer.writerow([product_id, url])
        except Exception as e:
            print(e)
        return handle_response({}, data='Societies deleted successfully', success=True)

class AddBookingStatus(APIView):
    def post(self, request):
        try:
            request_data = request.data
            data = request_data.get('data')
            for status in data:
                name = status.get('name')
                code = status.get('code')
                end_customer = status.get('end_customer')

                booking_status = BookingStatus.objects.create(name=name, code=code.upper(), type_of_end_customer_id=end_customer)
            return handle_response({}, data='status updated', success=True)
        except Exception as e:
            print(e)
            return handle_response({}, data='status not updated', success=True)

class AddBookingSubstatus(APIView):
    def post(self, request):
        try:
            request_data = request.data
            data = request_data.get('data')
            for status in data:
                name = status.get('name')
                code = status.get('code')
                booking_status_id = status.get('booking_status_id')

                booking_status = BookingSubstatus.objects.create(name=name, code=code.upper(), booking_status_id=booking_status_id)
            return handle_response({}, data='substatus updated', success=True)
        except Exception as e:
            print(e)
            return handle_response({}, data='substatuss not updated', success=True)
        return handle_response({}, data='File created', success=True)

class UpdateLandmark(APIView):

    def post(self, request):
    
        data = request.data
        for row in data:
            supplier_id = row['supplier_id']
            landmark = row['landmark']
            supplier_society = SupplierTypeSociety.objects.filter(supplier_id=supplier_id)
            if supplier_society:
                supplier_society.update(landmark=landmark)
        return handle_response({}, data='Landmark updated successfully', success=True)