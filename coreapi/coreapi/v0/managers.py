from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

import ui.constants as ui_constants


class GetInventoryObjectManager(models.Manager):
    """
    custom manager that will return right inventory object for a given supplier_type_code
    """

    def get_object(self, data, id):
        """
        Args:
            data: a dict that contains supplier_type_code
            id: supplier_id

        Returns: returns an object of the model which is linked to right supplier.

        """
        try:
            supplier_code = data['supplier_type_code']
            # supplier_code = 'CP'  # todo: change this when get clearity
            content_type = self.get_content_type(supplier_code)
            inventory_object = self.get(object_id=id,
                                                content_type=content_type)

            return inventory_object

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            return None

    def filter_objects(self, data, supplier_ids):
        """
        Args:
            data: dict containig supplier_type_code
            supplier_ids: a list of supplier id's.

        Returns: All objects of the this  model that are linked to suppliers in supplier_ids.

        """
        try:
            # supplier_code = data['supplier_type_code']

            supplier_code = 'RS'  # todo: change this when get clearity
            content_type = self.get_content_type(supplier_code)
            inventory_objects = self.filter(object_id__in=supplier_ids, content_type=content_type)
            return inventory_objects

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            return None

    def get_price_mapping_object(self, data, id, supplier_type_code):
        """
        This manager should only be used on PriceMappingDefault class.
        Args:
            data: Price Mapping Default Data
            id: supplier_id
            supplier_type_code: RS, CP

        Returns: Object of PriceMappingDefault class which has the given data in data.

        """
        try:
            adinventory_type = data['adinventory_type']
            duration_type = data['duration_type']

            content_type = self.get_content_type(supplier_type_code)
            price_object = self.get(object_id=id,
                                                content_type=content_type, adinventory_type=adinventory_type, duration_type=duration_type)
            return price_object

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            return None

    def get_or_create_objects(self, data, id, supplier_type_code):
        """
        Args:
            data: a dict containing any data with which you want to create objects of this class
            id: supplier_id
            supplier_type_code: RS, CP etc

        Returns: an object which is either created or fetched for data in 'data'.

        """
        try:
            content_type = self.get_content_type(supplier_type_code)
            data['object_id'] = id
            data['content_type'] = content_type

            (general_object, is_created) = self.get_or_create(**data)

            return general_object

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            return None

    def get_content_type(self, supplier_type_code):
        try:
            ContentType = apps.get_model('contenttypes', 'ContentType')
            suppliers = ui_constants.string_suppliers
            load_model = apps.get_model('v0', suppliers[supplier_type_code])
            content_type = ContentType.objects.get_for_model(load_model)
            return content_type
        except Exception as e:
            pass









