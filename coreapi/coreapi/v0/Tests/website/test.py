from __future__ import print_function
import json

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from rest_framework.test import APITestCase
from rest_framework import status
from v0.ui.account.models import BusinessTypes, BusinessSubTypes
from v0.ui.organisation.models import Organisation
from v0.ui.account.models import AccountInfo
from v0.ui.proposal.models import ProposalInfo

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
#         self.business = models.Organisation.objects.create(business_id='B1', name='AXCDG', type_name=self.business_type, sub_type=self.business_sub_type,)
#         business_content_type = ContentType.objects.get_for_model(model=models.Organisation)
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
#     Test cases for BusinessAccounts. The view is used to fetch one business data on supplying
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
#         self.business = models.Organisation.objects.create(business_id='B1', name='AXCDG', type_name=self.business_type,
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
#         self.business = models.Organisation.objects.create(business_id='B1', name='AXCDG', type_name=self.business_type,
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


#
# class GetLocationsAPIViewTestCase(APITestCase):
#     """
#     GetLocationsAPIView test cases.
#     """
#     def setUp(self):
#
#         # use a function to make necessary database. it's cleaner
#         self.context = test_utils.create_city_area_subarea()
#
#     def test_pass_get_area(self):
#         """
#         Test passes on fetching area as type parameter
#         """
#
#         # make the url
#         url = reverse('locations', kwargs={'id' : self.context['city'].id})
#
#         # query params
#         data = {
#             'type': 'areas'
#         }
#
#         # make the call
#         response = self.client.get(url, data=data)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_pass_get_sub_area(self):
#         """
#         Test passes on fetching sub area as type parameter
#         """
#
#         # make the url
#         url = reverse('locations', kwargs={'id': self.context['area'].id})
#
#         # query params
#         data = {
#             'type': 'sub_areas'
#         }
#
#         # make the call
#         response = self.client.get(url, data=data)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_fail_get_sub_area(self):
#         """
#         Test fails on providing wrong type
#         """
#
#         # make the url
#         url = reverse('locations', kwargs={'id': self.context['area'].id})
#
#         # query params
#         data = {
#             'type': 'xxxx'
#         }
#
#         # make the call
#         response = self.client.get(url, data=data)
#
#         # check the response
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
#
#
#


class CreateInitialProposalTestCases(APITestCase):
    """
    Test cases for CreateInitialProposal. This view is first step in creating proposal.
    """
    def setUp(self):

        # create account
        # setup proposal data

        # make business_type
        business_type = BusinessTypes.objects.create(business_type='EDUCATION', business_type_code='EDU')

        # make business sub types
        business_sub_type = BusinessSubTypes.objects.create(business_type=business_type,
                                                                        business_sub_type='SCHOOL',
                                                                        business_sub_type_code='SCH')

        # make businesses
        business = Organisation.objects.create(business_id='B1', name='AXCDG', type_name=business_type,
                                                      sub_type=business_sub_type, )

        # make account
        self.account = AccountInfo.objects.create(account_id='a1', business=business, name='A1', phone='960790857',
                                          email='whatever@gmail.com')

        self.proposal_data = {

            'tentative_cost': 1000,
            'name': 'garam_masala',
            'centers': test_utils.create_centers(),
        }

    def test_pass_create_fresh_proposal(self):
        """
        Test should pass with fresh proposal data
        """
        # make the url
        url = reverse('create-initial-proposal', kwargs={'account_id': self.account.account_id})

        # make the call
        response = self.client.post(url, data=json.dumps(self.proposal_data), content_type='application/json')

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pass_create_child_proposal(self):
        """
        Test should pass. use  case is, first we create a proposal. Then we hit the API. Then we again hit the
        api with parent set to id of the previous proposal.
        """
        url = reverse('create-initial-proposal', kwargs={'account_id': self.account.account_id})

        # make the call
        response = self.client.post(url, data=json.dumps(self.proposal_data), content_type='application/json')

        proposal_id_created = response.data['data']

        # copy the old proposal data to new data
        self.new_proposal = self.proposal_data

        # set the parent this time.
        self.new_proposal['parent'] = proposal_id_created

        # again hit the url. because a parent is set, now when  a new proposal_id is created, it's parent attribute
        # is set to this parent value which we are sending.
        url = reverse('create-initial-proposal', kwargs={'account_id': self.account.account_id})

        # make the call
        response = self.client.post(url, data=json.dumps(self.new_proposal), content_type='application/json')

        # fetch the new proposal_id created second time.
        child_proposal_id = response.data['data']

        # fetch the parent for this proposal_id.
        parent_id = ProposalInfo.objects.get(proposal_id=child_proposal_id).parent.proposal_id

        # this should be the same parent which was supplied
        self.assertEqual(parent_id, proposal_id_created)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateFinalProposalTestCase(APITestCase):
    """
    Test cases for CreateFinalProposal API view. This view is the second step in creating proposal.
    """
    def setUp(self):
        """
         [
             {
                  center : { id : 1 , center_name: c1, ...   } ,
                  suppliers:  { 'RS' : [ { 'supplier_type_code': 'RS', 'status': 'R', 'supplier_id' : '1'}, {...}, {...}  }
                  suppliers_meta: {
                                     'RS': { 'inventory_type_selected' : [ 'PO', 'POST', 'ST' ]  },
                                     'CP': { 'inventory_type_selected':  ['ST']
                  }
             }
        ]
        """
        self.data, self.proposal_id = test_utils.create_final_proposal_data()

    def test_pass_create_final_proposal(self):
        # make the url
        url = reverse('create-final-proposal', kwargs={'proposal_id': self.proposal_id})

        # make the call
        response = self.client.post(url, data=json.dumps(self.data), content_type='application/json')

        print(response.data)

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)






