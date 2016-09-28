from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class GetInventoryObjectManager(models.Manager):
    """
    custom manager that will return right inventory object for a given supplier_type_code
    """

    def get_inventory_object(self, data, id):
        try:
            supplier_code = data['supplier_type_code']
            #supplier_code = 'CP'  # todo: change this when get clearity
            suppliers = {'RS': 'SupplierTypeSociety', 'CP': 'SupplierTypeCorporate',
                         'GY': 'SupplierTypeGym', 'SA': 'SupplierTypeSalon'}

            ContentType = apps.get_model('contenttypes', 'ContentType')

            load_model = apps.get_model('v0', suppliers[supplier_code])

            if not supplier_code:
                return None

            content_type = ContentType.objects.get_for_model(load_model)
            inventory_object = self.get(object_id=id,
                                                content_type=content_type)

            return inventory_object

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            return None

    def filter_inventory_objects(self, data, supplier_ids):
        try:
            # supplier_code = data['supplier_type_code']

            supplier_code = 'CP'  # todo: change this when get clearity
            suppliers = {'RS': 'SupplierTypeSociety', 'CP': 'SupplierTypeCorporate',
                         'GY': 'SupplierTypeGym', 'SA': 'SupplierTypeSalon'}

            ContentType = apps.get_model('contenttypes', 'ContentType')

            load_model = apps.get_model('v0', suppliers[supplier_code])

            if not supplier_code:
                return None

            content_type = ContentType.objects.get_for_model(load_model)

            inventory_objects = self.filter(object_id__in=supplier_ids, content_type=content_type)
            return inventory_objects

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            return None

    def get_price_mapping_object(self, data, id):
        try:
            # supplier_code = data['supplier_type_code']
            adinventory_type = data['adinventory_type']
            duration_type = data['duration_type']
            supplier_code = 'RS'  # todo: change this when get clearity
            suppliers = {'RS': 'SupplierTypeSociety', 'CP': 'SupplierTypeCorporate',
                         'GY': 'SupplierTypeGym', 'SA': 'SupplierTypeSalon'}

            ContentType = apps.get_model('contenttypes', 'ContentType')

            load_model = apps.get_model('v0', suppliers[supplier_code])

            if not supplier_code:
                return None

            content_type = ContentType.objects.get_for_model(load_model)
            price_object = self.get(object_id=id,
                                                content_type=content_type, adinventory_type=adinventory_type, duration_type=duration_type)

            return price_object

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            return None

    def get_or_create_objects(self, data, id, supplier_type_code):
        try:

            supplier_code = supplier_type_code
            #supplier_code = 'CP'  # todo: change this when get clearity
            suppliers = {'RS': 'SupplierTypeSociety', 'CP': 'SupplierTypeCorporate',
                         'GY': 'SupplierTypeGym', 'SA': 'SupplierTypeSalon'}

            ContentType = apps.get_model('contenttypes', 'ContentType')

            load_model = apps.get_model('v0', suppliers[supplier_code])

            if not supplier_code:
                return None

            content_type = ContentType.objects.get_for_model(load_model)

            data['object_id'] = id
            data['content_type'] = content_type

            (general_object, is_created) = self.get_or_create(**data)

            return general_object

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            print e.message






