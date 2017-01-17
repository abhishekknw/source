import ui.constants as ui_constants
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.db.models import Q
import v0.models


class GeneralManager(models.Manager):
    """
    custom manager that will do many things.
    """

    def get_supplier_type_specific_object(self, data, id):
        """
        Args:
            data: a dict that contains supplier_type_code
            id: supplier_id

        Returns: fetches model instance based on content_type and object_id

        """
        try:
            supplier_code = data['supplier_type_code']
            content_type = self.get_content_type(supplier_code)
            inventory_object = self.get(object_id=id, content_type=content_type)

            return inventory_object

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            return None

    def get_supplier_type_specific_objects(self, data, supplier_ids):
        """
        Args:
            data: dict containing supplier_type_code
            supplier_ids: a list of supplier id's.

        Returns: fetches all model instances whose content_type matches the supplier_type_code

        """
        try:
            supplier_code = data['supplier_type_code']
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
            # collect data that is used to get or create price mapping default object
            data = {
                'object_id': id,
                'content_type': content_type,
                'adinventory_type': adinventory_type,
                'duration_type': duration_type
            }

            # get or create price mapping object
            price_object = self.get(**data)
            return price_object

        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist("PMD object does not exist")
        except Exception as e:
            raise Exception("Some exception occurred {0}".format(e.message))

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
            suppliers = ui_constants.codes_to_model_names
            load_model = apps.get_model('v0', suppliers[supplier_type_code])
            content_type = ContentType.objects.get_for_model(load_model)
            return content_type
        except Exception as e:
            pass

    def get_user_related_object(self, user, **kwargs):
        function = self.get_user_related_object.__name__
        try:
            query = HelperManagerMethods.prepare_query(user, **kwargs)
            result = self.get(query)
            return result
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist(e, function)
        except MultipleObjectsReturned as e:
            raise MultipleObjectsReturned(e, function)
        except Exception as e:
            raise Exception(e, function)

    def filter_user_related_objects(self, user, **kwargs):
        function = self.filter_user_related_objects.__name__
        try:
            query = HelperManagerMethods.prepare_query(user, **kwargs)
            result = self.filter(query)
            return result
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist(e, function)
        except Exception as e:
            raise Exception(e, function)


class HelperManagerMethods(object):

    @staticmethod
    def prepare_query(user, **kwargs):
        """
        Args:
            user: User instance
            **kwargs: keyword arguments
        Returns: a query ( Q object )
        """
        function = HelperManagerMethods.prepare_query.__name__
        try:
            main_query = Q(**kwargs)
            # fetch the user's current permission code
            user_permission_code = user.user_code

            # get the extra permission codes which may be defined for this user
            extra_permission_codes = list(v0.models.CustomPermissions.objects.filter(user=user).values('extra_permission_code'))
            # even the user current permission code is going by name 'extra_permission_code'. don't be confused.
            extra_permission_codes.append({'extra_permission_code': user_permission_code})

            # the query that ORes individual permission codes.
            custom_query = HelperManagerMethods.get_user_related_query(extra_permission_codes)

            # join together the main and custom query and return
            if main_query and custom_query:
                final_query = main_query & custom_query
            elif main_query:
                final_query = main_query
            else:
                final_query = custom_query
            return final_query

        except Exception as e:
            raise Exception(e, function)

    @staticmethod
    def get_user_related_query(permission_codes):
        """
        Args:
            permission_codes: ['01', '02']
        Returns: a Q object which is a result of ORing individual queries.
        """
        function = HelperManagerMethods.get_user_related_query.__name__
        try:
            custom_query = Q()
            query_dict = {}
            base_query_string = 'user__user_code__startswith'
            # in either case build a query by ORing individual queries.
            for permission_code in permission_codes:
                code = str(permission_code['extra_permission_code'])
                query_dict[base_query_string] = code
                if custom_query:
                    custom_query |= Q(**query_dict)
                else:
                    custom_query = Q(**query_dict)
            # return the custom query
            return custom_query
        except Exception as e:
            raise Exception(e, function)











