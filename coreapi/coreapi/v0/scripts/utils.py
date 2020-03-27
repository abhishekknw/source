import random
import string


def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_supplier_id(supplier, city, area, subarea, supplier_type_code):
    # Create supplier Id
    supplier_code = supplier.strip()[:3]
    supplier_id = city[:3].strip() + area[:3].strip() + subarea[:3].strip() \
                  + supplier_type_code.strip() + supplier_code
    supplier_id = supplier_id.upper()
    return supplier_id


def create_random_supplier_id(supplier, city, area, subarea, supplier_type_code):
    supplier_id = create_supplier_id(supplier, city, area, subarea, supplier_type_code)
    new_supplier_id = randomString() + supplier_id
    return new_supplier_id