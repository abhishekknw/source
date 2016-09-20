'''

# helper file for ui views. all functions in this file should take a common format of  (request, data)
order of imports
 -native python imports
 -django specific imports
 -third party imports
 -file imports

'''

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status

from v0.models import City, CityArea, CitySubArea


def get_supplier_id(request, data):
    """
    :param request: request parameter
    :param data: dict containing valid keys . Note the keys should be 'city', 'area', sub_area', 'supplier_type' ,
    'supplier_code' for this to work
    :return:  Response in which data has a key 'supplier_id' containing supplier_id
    """
    try:

        city_object = City.objects.get(city_name=data['city'])
        area_object = CityArea.objects.get(label=data['area'])
        subarea_object = CitySubArea.objects.get(subarea_name=data['sub_area'],
                                                 area_code=area_object)
        supplier_id = city_object.city_code + area_object.area_code + subarea_object.subarea_code + data[
            'supplier_type'] + data[
                          'supplier_code']
    except KeyError as e:
        return Response(data={'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist as e:
        return Response(data={'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={'supplier_id': supplier_id}, status=status.HTTP_200_OK)
