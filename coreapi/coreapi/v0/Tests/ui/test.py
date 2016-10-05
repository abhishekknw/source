import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

import v0.models as models


class GenerateSupplieridTestCase(APITestCase):
    """
    Test case for GenerateSupplierIdAPIView
    """

    def setUp(self):
        # make required objects in test db
        self.state = models.State.objects.create(state_name='UttarPradesh', state_code='UP')
        self.city = models.City.objects.create(city_name='Lucknow', city_code='LKO', state_code=self.state)
        self.city_area = models.CityArea.objects.create(label="LKO CANTT", area_code="LC", city_code=self.city)
        self.city_sub_area = models.CitySubArea.objects.create(subarea_name='Vijay Nagar', subarea_code="VN",
                                                               area_code=self.city_area)

    def test_pass_correct_data_cp(self):
        # make the url
        url = reverse('generate-id')

        # make the data
        data = {
            'city_id': self.city.id,
            'area_id': self.city_area.id,
            'subarea_id': self.city_sub_area.id,
            'supplier_type': 'CP',
            'supplier_code': 'UPL',
            'supplier_name': 'TestSuplier'
        }
        # make the call
        response = self.client.post(url, data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pass_correct_data_rs(self):
        # make the url
        url = reverse('generate-id')

        # make the data
        data = {
            'city_id': self.city.id,
            'area_id': self.city_area.id,
            'subarea_id': self.city_sub_area.id,
            'supplier_type': 'RS',
            'supplier_code': 'UPL',
            'supplier_name': 'TestSuplier'
        }
        # make the call
        response = self.client.post(url, data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_incorrect_supplier_type_code(self):
        # make the url
        url = reverse('generate-id')

        # make the data
        data = {
            'city_id': self.city.id,
            'area_id': self.city_area.id,
            'subarea_id': self.city_sub_area.id,
            'supplier_type': 'XX',
            'supplier_code': 'UPL',
            'supplier_name': 'TestSuplier'
        }
        # make the call
        response = self.client.post(url, data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CorporateAPIListViewTestCases(APITestCase):
    """
    Testing the url /v0/ui/corporate/list/ which lists all the corporates.
    """
    def setUp(self):
        # make a superuser
        # login him

        self.super_user = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')

        # make a sample SupplierTypeCorporate
        self.supplier_type_corporate = models.SupplierTypeCorporate.objects.create(supplier_id='SS1', name="whatever")

    def test_pass_list_all_supplier_corporates_valid_login(self):
        # make the url
        url = reverse('corporate-list')

        # login the user
        self.client.login(username='john', password='johnpassword')

        # make the call
        response = self.client.get(url)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_list_supplier_corporates_invalid_login(self):
        # make the url
        url = reverse('corporate-list')

        # make the call without login
        response = self.client.get(url)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SaveBasicCorporateDetailsAPIViewTestCase(APITestCase):
    """
    test cases for SaveBasicCorporateDetails
    """

    def setUp(self):
        # create a SupplierTypeCorporate
        self.supplier_type_corporate = models.SupplierTypeCorporate.objects.create(supplier_id='SS1', name="whatever")

        # create a CorporateParkCompanyList instance
        self.corporate_park_company_list = models.CorporateParkCompanyList.objects.create(name="C1",
                                                                                          supplier_id=self.supplier_type_corporate)

    def test_pass_get_basic_details_corporate(self):
        """
        GET api passes on right data
        """
        # make the url with arguments as the url expects supplier id
        url = reverse('load-initial-corporate-data', kwargs={'id': 'SS1'})

        # make the call
        response = self.client.get(url)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_wrong_supplier_id(self):
        """
        GET api fails on wrong supplier id
        """
        # make the url
        url = reverse('load-initial-corporate-data', kwargs={'id': 'XXX'})

        # make the call
        response = self.client.get(url)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pass_post_basic_details(self):
        """
        Post API passes on right data
        """
        # make the data to be posted
        self.data = {
            'supplier_id': 'SS1',
            'list1': ['c1', 'c2', 'c3'],
            'building_count': 2
        }

        # make the url
        url = reverse('load-initial-corporate-data', kwargs={'id': 'SS1'})

        # make the call
        response = self.client.post(url, self.data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_post_wrong_supplier_id(self):
        """
        POST api fails if wrong supplier_id is provided
        """
        # make the data to be posted
        self.data = {
            'supplier_id': 'XXX',
            'list1': ['c1', 'c2', 'c3'],
            'building_count': 2
        }

        # make the url
        url = reverse('load-initial-corporate-data', kwargs={'id': 'XXX'})

        # make the call
        response = self.client.post(url, self.data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SaveBuildingDetailsAPIViewTestCase(APITestCase):
    """
    Tests for SaveBuildingDetails API View
    """
    def setUp(self):
        # create a SupplierTypeCorporate
        self.supplier_type_corporate = models.SupplierTypeCorporate.objects.create(supplier_id='SS1', name="whatever")

        # create buildings for this corporate
        models.CorporateBuilding.objects.create(building_name='B1', number_of_wings=2, corporatepark_id=self.supplier_type_corporate)
        models.CorporateBuilding.objects.create(building_name='B2', number_of_wings=2, corporatepark_id=self.supplier_type_corporate)

    def test_pass_get_all_buildings(self):
        """
        Get api passes with valid data
        """
        # make the url
        url = reverse('save-building-details', kwargs={'id': 'SS1'})

        # make the call
        response = self.client.get(url)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_wrong_supplier_id(self):
        """
        Get API fails on supplying wrong supplier_id
        """
        # make the url
        url = reverse('save-building-details', kwargs={'id': 'XXX'})

        # make the call
        response = self.client.get(url)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pass_submit_building_details(self):
        """
        POST api passes on right data
        """
        # make the data
        self.data = [

            {
                'number_of_wings': 1,
                'wingInfo': [
                    {
                        'number_of_floors': 2,
                        'wing_name_temp': 'w1',
                        'wing_name': 'w1'
                    }

                ],
                'building_name': 'B1'
            },
            {
                'number_of_wings': 2,
                'wingInfo': [
                    {
                        'number_of_floors': 2,
                        'wing_name_temp': 'w21',
                        'wing_name': 'w21'
                    },
                    {
                        'number_of_floors': 1,
                        'wing_name_temp': 'w22',
                        'wing_name': 'w22'

                    }
                ],
                'building_name': 'B2'

            }
        ]

        # make the url
        url = reverse('save-building-details', kwargs={'id': 'SS1'})

        # make the call
        response = self.client.post(url, data=json.dumps(self.data), content_type='application/json')

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
