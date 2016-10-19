import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from rest_framework.test import APITestCase
from rest_framework import status

import v0.models as models
import v0.Tests.utils as test_utils

'''
This file contains test cases for website app.
'''


# class GetBusinessTypesTestCase(APITestCase):
#     """
#     Test cases for view GetBusinessTypesAPIView
#     author: Nikhil
#     """
#     def setUp(self):
#         # make some BusinessTypes
#         models.BusinessTypes.objects.create(business_type='EDUCATION', business_type_code='EDU')
#         models.BusinessTypes.objects.create(business_type='SPORTS', business_type_code='SPO')
#
#     def test_pass_get_all_business_types(self):
#         """
#         passes when api is hit to get all business types
#         """
#
#         # make the url
#         url = reverse('get-business-types')
#
#         # make the call
#         response = self.client.get(url)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class BusinessAPIListViewTestCase(APITestCase):
#     """
#     Test cases for view BusinessAPIListView
#     author: Nikhil
#     """
#     def setUp(self):
#         # make some business_types
#         self.business_type = models.BusinessTypes.objects.create(business_type='EDUCATION', business_type_code='EDU')
#
#         # make business sub types
#         self.business_sub_type = models.BusinessSubTypes.objects.create(business_type=self.business_type, business_sub_type='SCHOOL',  business_sub_type_code='SCH')
#
#         # make some businesses
#         self.business = models.BusinessInfo.objects.create(business_id='B1', name='AXCDG', type_name=self.business_type, sub_type=self.business_sub_type,)
#         business_content_type = ContentType.objects.get_for_model(model=models.BusinessInfo)
#
#         # make a contact for the business
#         self.contact = models.BusinessAccountContact.objects.create(content_type=business_content_type, object_id=self.business.business_id, name='C1', designation='d1', department='D1', phone='123456789', email='whatever@gmail.com')
#
#     def test_pass_get_business_info(self):
#         """
#         passes when api is hit to get business info
#         """
#         # make the url
#         url = reverse('get-all-business-info')
#
#         # make the call
#         response = self.client.get(url)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class BusinessAPIViewTestCase(APITestCase):
#     """
#     Test cases for BusinessAPIView. The view is used to fetch one business data on supplying
#     right business id
#     author: Nikhil
#     """
#
#     def setUp(self):
#         # make business_type
#         self.business_type = models.BusinessTypes.objects.create(business_type='EDUCATION', business_type_code='EDU')
#
#         # make business sub types
#         self.business_sub_type = models.BusinessSubTypes.objects.create(business_type=self.business_type,
#                                                                         business_sub_type='SCHOOL',
#                                                                         business_sub_type_code='SCH')
#
#         # make some businesses
#         self.business = models.BusinessInfo.objects.create(business_id='B1', name='AXCDG', type_name=self.business_type,
#                                                            sub_type=self.business_sub_type, )
#
#         # make accounts
#         models.AccountInfo.objects.create(account_id='a1', business=self.business, name='A1', phone='960790857', email='whatever@gmail.com')
#
#         models.AccountInfo.objects.create(account_id='a2', business=self.business, name='A2', phone='960790857',
#                                   email='whatever@gmail.com')
#
#     def test_pass_get_data_one_business(self):
#         """
#         API passed on providing right business id
#         """
#
#         # make the url
#         url = reverse('get-one-business-data', kwargs={'id': 'B1'})
#
#         # make the call
#         response = self.client.get(url)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_fail_get_data_one_business(self):
#         """
#         on supplying wrong business id, the api fails
#         """
#         # make the url
#         url = reverse('get-one-business-data', kwargs={'id': 'GUDDU'})
#
#         # make the call
#         response = self.client.get(url)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class GetBusinessSubTypesAPIViewTestCase(APITestCase):
#     """
#     Test cases for GetBusinessSubTypesAPIView. The view is used to fetch various subtypes of business on the basis
#     of business type id.
#     author: Nikhil
#     """
#
#     def setUp(self):
#         # make business_type
#         self.business_type = models.BusinessTypes.objects.create(business_type='EDUCATION', business_type_code='EDU')
#
#         # make business sub types
#         self.business_sub_type = models.BusinessSubTypes.objects.create(business_type=self.business_type,
#                                                                         business_sub_type='SCHOOL',
#                                                                         business_sub_type_code='SCH')
#
#     def test_pass_get_business_sub_types(self):
#         """
#         API passes on providing right business_type id
#         """
#         # make the url
#         url = reverse('get-business-subtypes', kwargs={'id': self.business_type.id})
#
#         # make the call
#         response = self.client.get(url)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_pass_get_business_sub_types_wrong_business_id(self):
#         """
#         API passes on providing wrong business_type id because .filter is used to fetch objects on the view
#         if it doesn't find them, it returns en empty set
#         """
#         # make the url
#         url = reverse('get-business-subtypes', kwargs={'id': self.business_type.id + 1000})
#
#         # make the call
#         response = self.client.get(url)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class GetAccountProposalsAPIViewTestCases(APITestCase):
#     """
#     Test cases for GetAccountProposalsAPIView. The views fetches all proposals for a given account.
#     author: Nikhil
#     """
#
#     def setUp(self):
#         # make business_type
#         self.business_type = models.BusinessTypes.objects.create(business_type='EDUCATION', business_type_code='EDU')
#
#         # make business sub types
#         self.business_sub_type = models.BusinessSubTypes.objects.create(business_type=self.business_type,
#                                                                         business_sub_type='SCHOOL',
#                                                                         business_sub_type_code='SCH')
#
#         # make businesses
#         self.business = models.BusinessInfo.objects.create(business_id='B1', name='AXCDG', type_name=self.business_type,
#                                                            sub_type=self.business_sub_type, )
#
#         # make account
#         self.account = models.AccountInfo.objects.create(account_id='a1', business=self.business, name='A1', phone='960790857',
#                                           email='whatever@gmail.com')
#
#         # make some proposals for this account
#
#         models.ProposalInfo.objects.create(proposal_id='abc', account=self.account, name='P1', tentative_cost=500)
#         models.ProposalInfo.objects.create(proposal_id='def', account=self.account, name='P2', tentative_cost=100)
#
#     def test_pass_get_all_proposals(self):
#         """
#         Test passes fetching successfully all proposals for the given account
#         """
#         # make the url
#         url = reverse('get-account-proposals', kwargs={'account_id': 'a1'})
#
#         # make the call
#         response = self.client.get(url)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_fail_get_all_proposals(self):
#         """
#         Test fails for wrong account_id
#         """
#         # make the url
#         url = reverse('get-account-proposals', kwargs={'account_id': 'xxx'})
#
#         # make the call
#         response = self.client.get(url)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#

#
# class SpacesOnCenterAPIViewTestCases(APITestCase):
#     """
#     Test cases for the view SpacesOnCenterAPIView
#     """
#
#     def setUp(self):
#         # create some societies
#         self.society_1 = models.SupplierTypeSociety.objects.create(supplier_id='S1', society_name='NAME1', society_longitude=10, society_latitude=20)
#         self.society_2 = models.SupplierTypeSociety.objects.create(supplier_id='S2', society_name='NAME2', society_longitude=11,
#                                                            society_latitude=21),
#         self.society_3 = models.SupplierTypeSociety.objects.create(supplier_id='S3', society_name='NAME3', society_longitude=9, society_latitude=19)
#
#         # set a proposal id
#         self.proposal_id = 'abc'
#
#         self.proposal = create_basic_proposal(self.proposal_id)
#
#         # create a center when you have a proposal
#         self.center = models.ProposalCenterMapping.objects.create(proposal=self.proposal, center_name='C1', latitude=5, longitude=25, radius=2, pincode=400072, city='Mumbai', area='Powai', subarea='Powai')
#
#         # create space mapping object
#         self.space_mapping = models.SpaceMapping.objects.create(center=self.center, proposal=self.proposal, society_allowed=True, society_count=5)
#
#         # create InventoryType
#         models.InventoryType.objects.create(supplier_code='S1', space_mapping=self.space_mapping, poster_allowed=True)
#
#
#     def test_pass_get_suppliers(self):
#         """
#         Test passes for a simple call to getSpaces
#         """
#         # make the url
#         url = reverse('get-spaces', kwargs={'proposal_id': self.proposal_id})
#
#         # make the call
#         response = self.client.get(url)
#
#         print response.data
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetLocationsAPIViewTestCase(APITestCase):
    """
    GetLocationsAPIView test cases.
    """
    def setUp(self):

        # use a function to make necessary database. it's cleaner
        self.context = test_utils.create_city_area_subarea()

    def test_pass_get_area(self):
        """
        Test passes on fetching area as type parameter
        """

        # make the url
        url = reverse('locations', kwargs={'id' : self.context['city'].id})

        # query params
        data = {
            'type': 'areas'
        }

        # make the call
        response = self.client.get(url, data=data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pass_get_sub_area(self):
        """
        Test passes on fetching sub area as type parameter
        """

        # make the url
        url = reverse('locations', kwargs={'id': self.context['area'].id})

        # query params
        data = {
            'type': 'sub_areas'
        }

        # make the call
        response = self.client.get(url, data=data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_get_sub_area(self):
        """
        Test fails on providing wrong type
        """

        # make the url
        url = reverse('locations', kwargs={'id': self.context['area'].id})

        # query params
        data = {
            'type': 'xxxx'
        }

        # make the call
        response = self.client.get(url, data=data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)






def create_basic_proposal(proposal_id):
        """
        Returns: a proposal object

        """
        # make business_type
        business_type = models.BusinessTypes.objects.create(business_type='EDUCATION', business_type_code='EDU')

        # make business sub types
        business_sub_type = models.BusinessSubTypes.objects.create(business_type=business_type,
                                                                        business_sub_type='SCHOOL',
                                                                        business_sub_type_code='SCH')

        # make businesses
        business = models.BusinessInfo.objects.create(business_id='B1', name='AXCDG', type_name=business_type,
                                                           sub_type=business_sub_type, )

        # make account
        account = models.AccountInfo.objects.create(account_id='a1', business=business, name='A1', phone='960790857',
                                          email='whatever@gmail.com')

        # make some proposals for this account

        proposal = models.ProposalInfo.objects.create(proposal_id=proposal_id, account=account, name='P1', tentative_cost=500)

        return proposal






















