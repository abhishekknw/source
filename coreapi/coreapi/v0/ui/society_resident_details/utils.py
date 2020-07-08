from v0.ui.supplier.models import SupplierTypeSociety


def get_supplier(supplier_id):
    society = SupplierTypeSociety.objects.filter(supplier_id=supplier_id).values('society_name')
    if society:
        return society[0]['society_name']
    else:
        return None


def format_contact_number(contact_number):
    if type(contact_number) == str:
        contact_number = contact_number.replace('-', '')
        contact_number = contact_number.replace(' ', '')
        contact_number = contact_number.split('\n')[0]
        contact_number = contact_number.split('&')[0]
        contact_number = contact_number.split(',')[0]
        contact_number = contact_number.split('/')[0]
        contact_number = contact_number.split('.')[0]
        contact_number = contact_number.split('*')[0]
        if not contact_number.isdigit():
            return None
    return int(contact_number) if contact_number else None
