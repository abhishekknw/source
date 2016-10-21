import v0.models as models


def create_city_area_subarea():
        """

        Returns: a dict containing necessary objects for creating a subarea

        """
        state =  models.State.objects.create(state_name='UP', state_code='UP')
        city =  models.City.objects.create(city_name='LKO', city_code='LKO', state_code=state)
        city_area = models.CityArea.objects.create(label='Aminabad', area_code='A', city_code=city)
        city_subarea = models.CitySubArea.objects.create(subarea_name='Vihar', subarea_code='V',  area_code=city_area)

        context = {
            'state': state,
            'city': city,
            'area': city_area,
            'subarea': city_subarea
        }
        return context


def create_centers():
    """

    Returns: a list of centers

    """
    centers = [
        {
            'city': '1',
            'center': {
                'city': 'Mumbai',
                'area': 'Kharghar',
                'center_name': 'powai',
                'subarea': 'Sector 10',
                'pincode': '401200',
                'longitude': '',
                'radius': 1,
                'address': 'powai',
                'latitude': ''
            },
            'area': u'17'
        },
        {
            'city': '1',
            'center': {
                'city': 'Mumbai',
                'area': 'Jogeshwari(E)',
                'center_name': 'juhu',
                'subarea': 'Parsi Colony',
                'pincode': '401345',
                'longitude': '',
                'radius': 1,
                'address': 'juhu',
                'latitude': ''
            },
            'area': '14'
        }
    ]
    return centers


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


def create_final_proposal_data():
    """
    creates data for CreateFinalProposal API view
    """
    proposal_id = 'abrakadabra'

    supplier_type_code = 'RS'

    supplier_id_1 = 's1'
    supplier_id_2 = 's2'

    # create a proposal
    proposal = create_basic_proposal(proposal_id)

    # create a center
    center = create_centers()[0]['center']

    # create some suppliers
    models.SupplierTypeSociety.objects.create(supplier_id='s1', society_name='Gajar')
    models.SupplierTypeSociety.objects.create(supplier_id='s2', society_name='Bhindi')

    data = [
        {
            'center': center,
            'societies': [
                {
                    'supplier_type_code': supplier_type_code,
                    'status': 'R',
                    'supplier_id': supplier_id_1,
                },
                {
                    'supplier_type_code': supplier_type_code,
                    'status': 'B',
                    'supplier_id': supplier_id_2,
                },
            ],
            'filters_data': create_filter_data()
        }
    ]
    return data, proposal.proposal_id


def create_filter_data():
    supplier_type_code = 'RS'
    return [
        {
            'supplier_type_code': supplier_type_code,
            'filters': [{'name': 'inventory_type', 'value': 'RO'}, {'name': 'inventory_type', 'value': 'PO'}]

        }
    ]
