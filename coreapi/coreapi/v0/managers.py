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
            # supplier_code = data['supplier_type_code']

            supplier_code = 'CP'  # todo: change this when get clearity
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
