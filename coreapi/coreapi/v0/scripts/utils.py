import random
import string
from v0.ui.supplier.models import (SupplierTypeSociety, SupplierTypeSalon, SupplierTypeGym, SupplierHording,
SupplierTypeCorporate, SupplierTypeBusShelter, SupplierTypeRetailShop, SupplierTypeBusDepot)
from v0.ui.account.models import ContactDetails


def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_supplier_id(supplier, city, area, subarea, supplier_type_code):
    # Create supplier Id
    supplier_code = supplier.strip()[:3]
    if subarea:
        supplier_id = city[:3].strip() + area[:3].strip() + subarea[:3].strip() \
                  + supplier_type_code.strip() + supplier_code
    else:
        supplier_id = city[:3].strip() + area[:3].strip() + supplier_type_code.strip() + supplier_code
    supplier_id = supplier_id.upper()
    return supplier_id


def create_random_supplier_id(supplier, city, area, subarea, supplier_type_code):
    supplier_id = create_supplier_id(supplier, city, area, subarea, supplier_type_code)
    new_supplier_id = randomString() + supplier_id
    new_supplier_id = new_supplier_id.replace(" ", "")
    return new_supplier_id.upper()


def create_new_society(model, supplier_name, city, area, subarea, supplier_type_code, tower_count, flat_count, latitude, longitude, address, zipcode, supplier_ids,contact_name, contact_number, designation, state):
    supplier_id = create_random_supplier_id(supplier_name, city, area, subarea, supplier_type_code)
    supplier = model.objects.filter(supplier_id=supplier_id).values('supplier_id', 'society_name')
    # Todo: Check supplier id in all suppliers
    # Change it to supplier master later
    salon = SupplierTypeSalon.objects.filter(supplier_id=supplier_id).values('supplier_id')
    gym = SupplierTypeGym.objects.filter(supplier_id=supplier_id).values('supplier_id')
    retail_shop = SupplierTypeRetailShop.objects.filter(supplier_id=supplier_id).values('supplier_id')
    busshelter = SupplierTypeBusShelter.objects.filter(supplier_id=supplier_id).values('supplier_id')
    coorporate = SupplierTypeCorporate.objects.filter(supplier_id=supplier_id).values('supplier_id')
    busdepot = SupplierTypeBusDepot.objects.filter(supplier_id=supplier_id).values('supplier_id')

    if len(supplier) > 0 or len(salon) > 0 or len(gym) > 0 or len(retail_shop) > 0 or len(coorporate) > 0 or len(
            busshelter) > 0 or len(busdepot) > 0:
        # create new supplier id
        supplier_id = create_random_supplier_id(supplier_name, city, area, subarea, supplier_type_code)

    # Create data in supplier & contact details
    if supplier_type_code == 'RS':
        supplier_details = model(
            supplier_id=supplier_id,
            society_name=supplier_name,
            society_state=state,
            society_city=city,
            society_locality=area,
            society_subarea=subarea,
            tower_count=tower_count if tower_count else 1,
            flat_count=flat_count if flat_count else 1,
            society_latitude=latitude if latitude else None,
            society_longitude=longitude if longitude else None,
            society_address1=address.strip().rstrip(',').lstrip(',').rstrip('.').rstrip('"').lstrip('.').lstrip('"') if address else None,
            supplier_code='RS',
            society_zip=zipcode if zipcode else None,
            representative_id='MAC1421'
        )
        supplier_details.save()
        # Append supplier id in supplier ids
        supplier_ids.append({
            'supplier_id': supplier_id,
            'name': supplier_name
        })
        print(supplier_ids)
        if supplier_details:
            # Update contact details
            contact_details = ContactDetails(object_id=supplier_id,
                                             name=contact_name.strip().rstrip(',').lstrip(','),
                                             mobile=contact_number,
                                             contact_type=designation.strip().rstrip(',').lstrip(','))
            contact_details.save()
        return [supplier_id, supplier_name]