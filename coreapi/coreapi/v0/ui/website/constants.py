from coreapi.settings import BASE_DIR

supplier_keys = [
    'city', 'area', 'sub_area', 'supplier_type', 'supplier_code', 'society_name'

    , 'society_address1', 'society_address2', 'society_zip', \
 \
    'society_latitude', 'society_longitude', 'possession_year', 'tower_count', 'flat_count', \
 \
    'vacant_flat_count', 'service_household_count', 'working_women_count', 'avg_household_occupants', \
    'bachelor_tenants_allowed', 'flat_avg_rental_persqft', 'cars_count', 'luxury_cars_count', \
    'society_location_type', 'society_type_quality', 'society_type_quantity', 'count_0_5', 'count_5_15', \
    'count_15_25', 'count_25_60', 'count_60above', 'society_weekly_off',
]

proposal_header_keys = [
    'Center Name','Center Proposal Id', 'Center Id', 'Space Mapping Id', 'Inventory Type Id', 'Supplier Id', 'Supplier Name', 'Supplier Sub Area', 'Supplier Type', 'Supplier Tower Count', \
    'Supplier Flat Count',
]

inventorylist = {
    'PO': {
        'HEADER': ['Poster Count', 'Poster Price', 'Poster Duration', 'Poster Price Factor', 'Poster price per flat', 'Poster Business Price'],
        'DATA': ['total_poster_count', 'poster_price', 'poster_duration', 'poster_price_factor',
                 'poster_price_per_flat', 'poster_business_price']
    },
    'ST': {
        'HEADER': ['Standee Count', 'Standee Price', 'Standee Duration', 'Standee Price factor',
                   'Standee price per flat', 'Standee Business Price'],
        'DATA': ['total_standee_count', 'standee_price', 'standee_duration', 'standee_price_factor',
                 'standee_price_per_flat', 'standee_business_price']
    },
    'FL': {
        'HEADER': ['Flier count', 'Flier Price', 'Flier Duration', 'Flier Price Factor', 'Flier Business Price'],
        'DATA': ['flier_count', 'flier_price', 'flier_duration', 'flier_price_factor', 'flier_business_price']
    },
    'SL': {
        'HEADER': ['Stall Count', 'Stall Price', 'Stall Duration', 'Stall Price Factor', 'Stall Business Price'],
        'DATA': ['stall_count', 'stall_price', 'stall_duration', 'stall_price_factor', 'stall_business_price']
    },
    'CD': {
        'HEADER': ['Car Display Count', 'Car Display Price', 'Car Display Duration', 'Car Display Price Factor', 'Car Business Price' ],
        'DATA': ['car_display', 'car_display_price', 'car_display_duration', 'car_display_price_factor', 'car_business_price']
    },
    'RS': {
        'HEADER': ['SUPPLIER ID', 'SOCIETY NAME', 'SOCIETY SUBAREA','SOCIETY TYPE QUALITY', 'TOWER COUNT', 'FLAT COUNT', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'quality_rating', 'tower_count', 'flat_count', 'status' ]
    },
    'CP': {
        'HEADER': ['SUPPLIER_ID', 'CORPORATE NAME', 'CORPORATE SUBAREA', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'status']
    },
    'CENTER': {
        'HEADER': ['CENTER ID', 'CENTER NAME', 'PROPOSAL'],
        'DATA': ['id', 'center_name', 'proposal']
    }
}

sample_data = [
    'vvhbhb', 'bhbhbh'
]

# society keys
society_keys = ['supplier_id', 'society_name', 'society_subarea', 'society_type_quality', \
                'tower_count', 'flat_count',
                ]

# keys for the center
center_keys = ['center_name', 'proposal', 'id']

export_keys = ['center', 'societies', 'societies_inventory', 'societies_inventory_count']

contact_keys = [
    'city', 'area', 'sub_area', 'supplier_type', 'society_name', 'supplier_code', 'contact_type', 'salutation', \
    'name', 'landline', 'mobile', 'email'
]

STD_CODE = '022'
COUNTRY_CODE = '+91'

price_per_flat = {
    'PO': ['poster_price_per_flat', 'poster_price'],
    'ST': ['standee_price_per_flat', 'standee_price'],
    'CD': ['car_display_price_per_flat', 'car_display_price'],
    'SL': ['stall_price_per_flat', 'stall_price'],
    'FL': ['flier_price_per_flat', 'filer_price'], #todo: change the spelling from filer to flier once fixed
}

# supplier_code_filter_params = {
#     'RS': {
#         'MODEL': SupplierTypeSociety,
#         'SERIALIZER' : SupplierTypeSocietySerializer,
#     },
#     'CP': {
#         'MODEL': SupplierTypeCorporate
#         # 'SERIALIZER' : SupplierTypeCorporateSerializer,
#     },
#     'GY': {
#         'MODEL': SupplierTypeGym
#         # 'SERIALIZER' : SupplierTypeGymSerializer,
#     },
#     'SL': {
#         'MODEL': SupplierTypeSalon
#         # 'SERIALIZER' : SupplierTypeSalonSerializer,
#     }
#
# }

import_master_keys = ['societies_inventory', 'societies_inventory_count', 'societies', 'center', 'societies_count']

society_inventory_keys = [
     'space_mapping', 'id',
]

societies_header_to_field_mapping = {
    'SUPPLIER ID': 'supplier_id',
    'SUPPLIER NAME': 'society_name',
    'SUB AREA': 'society_subarea',
    'SOCIETY TYPE': 'society_type_quality',
    'TOWER COUNT': 'tower_count',
    'FLAT COUNT': 'flat_count'
}

import_center_keys = [
    'center_name', 'proposal', 'id'
]

inventories_keys = {'BANNER': 'banner_allowed', 'POSTER': 'poster_allowed', 'FLIER': 'flier_allowed',

               'STANDEE':'standee_allowed', 'STALL': 'stall_allowed'}

index_of_center_id = 0

header_to_field_mapping = {
    'center name': 'center_name',
    'center proposal id': 'prop'

}

# inventory related fields in the sheet
inventory_fields = ['poster_count', 'stall_count', 'flier_count', 'standee_count', 'poster_price', 'stall_price', 'flier_price', 'standee_price']

# this list is used to know if a particular inventory was really present in the sheet
is_inventory_available = ['poster_count', 'stall_count', 'standee_count','flier_count']

# this dict uses items of is_inventory_available list to get corresponding model names
# BASE_NAME is available so that once we know what inventories are  in the sheet we can construct other inventory
# headers based on the base name.
inventory_models = {
    'poster_count': {'MODEL': 'PosterInventory', 'BASE_NAME': 'poster'},
    'stall_count': {'MODEL': 'StallInventory', 'BASE_NAME': 'stall'},
    'flier_count': {'MODEL': 'FlierThroughLobbyInfo', 'BASE_NAME': 'flier'},
    'standee_count': {'MODEL': 'StandeeInventory', 'BASE_NAME': 'standee'}
}

# a mapping from table names to serializers
table_to_serializer = {
    'ideation_design_cost': 'IdeationDesignCostSerializer',
    'logistic_operations_cost': 'LogisticOperationsCostSerializer',
    'space_booking_cost': 'SpaceBookingCostSerializer',
    'event_staffing_cost': 'EventStaffingCostSerializer',
    'data_sciences_cost': 'DataSciencesCostSerializer',
    'printing_cost': 'PrintingCostSerializer',
    'proposal_metrics': 'ProposalMetricsSerializer',
    'proposal_master_cost': 'ProposalMasterCostSerializer'
}


# predefined keys in data dict for Offline pricing. we need to make spaces for diff kinds of data
# the following data structure is a dict with keys as model names. values are a list of columns and some other details
# which are required to populate the db. each row of the sheet is mapped to a specific column of a specific model and
# has a particular value.

offline_pricing_data = {
    'ideation_design_cost': [{'match_term': 'ideation', 'col_name': 'total_cost', 'specific': None, 'value': 0}, ],

    'logistic_operations_cost': [
        {'match_term': 'logistics and operations', 'col_name': 'total_cost', 'specific': None, 'value': 0}],

    'space_booking_cost': [
        {'match_term': 'space booking charges society', 'col_name': 'total_cost', 'specific': {'code': 'RS'}, 'value': 0},
        {'match_term': 'space booking charges corporates', 'col_name': 'total_cost', 'specific': {'code': 'CP'},
         'value': 0},

    ],

    'event_staffing_cost': [

        {'match_term': 'event staffing cost', 'col_name': 'total_cost', 'specific': None, 'value': 0},

    ],

    'data_sciences_cost': [
        {'match_term': 'data sciences', 'col_name': 'total_cost', 'specific': None, 'value': 0},

    ],

    'printing_cost': [
        {'match_term': 'printing cost', 'col_name': 'total_cost', 'specific': None, 'value': 0},
    ],

    'proposal_master_cost': [

        {'match_term': 'Agency Charges', 'col_name': 'agency_cost', 'specific': None, 'value': 0},
        {'match_term': 'Basic Cost(Without Tax)', 'col_name': 'basic_cost', 'specific': None, 'value': 0},
        {'match_term': 'discount', 'col_name': 'discount', 'specific': None, 'value': 0},
        {'match_term': 'Total Cost with Tax', 'col_name': 'total_cost', 'specific': None, 'value': 0},
        {'match_term': 'Total Cost with Tax', 'col_name': 'total_cost', 'specific': None, 'value': 0},
        {'match_term': 'Tax', 'col_name': 'tax', 'specific': None, 'value': 0},
        {'match_term': 'Total Impressions', 'col_name': 'total_impressions', 'specific': None, 'value': 0},
        {'match_term': 'Average Cost per Impression', 'col_name': 'average_cost_per_impression', 'specific': None,
         'value': 0},

    ],
    'proposal_metrics': [

        {'match_term': 'Societies Covered ', 'col_name': 'metric_name', 'specific': {'code': 'RS',  }, 'value': 0},
        {'match_term': 'Corporate Parks Covered', 'col_name': 'metric_name', 'specific': {'code': 'CP'}, 'value': 0},

        {'match_term': 'Total Society Impressions', 'col_name': 'metric_name', 'specific': {'code': 'RS'}, 'value': 0},
        {'match_term': 'Total Corporates Impressions', 'col_name': 'metric_name', 'specific': {'code': 'CP',},'value': 0},

        {'match_term': 'Average Cost per Corporate', 'col_name': 'metric_name', 'specific': {'code': 'CP'}, 'value': 0},
        {'match_term': 'Average Cost per Society', 'col_name': 'metric_name', 'specific': {'code': 'RS'}, 'value': 0},
        {'match_term': 'Average Cost per Gym', 'col_name': 'metric_name', 'specific': {'code': 'GY'}, 'value': 0},
        {'match_term': 'Average Cost per Salon', 'col_name': 'metric_name', 'specific': {'code': 'SA'}, 'value': 0},

        {'match_term': 'Estimated Flat Covered', 'col_name': 'metric_name', 'specific': {'code': 'RS', }, 'value': 0},
        {'match_term': 'Estimated Tower Covered', 'col_name': 'metric_name', 'specific': {'code': 'CP'}, 'value': 0},
        {'match_term': 'Estimated Residents', 'col_name': 'metric_name', 'specific': {'code': 'RS'}, 'value': 0},
        {'match_term': 'Estimated Employess', 'col_name': 'metric_name', 'specific': {'code': 'CP'}, 'value': 0},

    ]

}

# models whose only one object exists in the sheet and data is made up of  content of  many rows
one_obect_models = ['ideation_design_cost', 'logistic_operations_cost', 'event_staffing_cost', 'data_sciences_cost', 'printing_cost', ]


# set the column index in the sheet that determines the values for Offline prricing
value_index = 1
comment_index = 2
metric_model = 'proposal_metrics'

# information of center to be sent back in get-spaces api
get_spaces_api_center_keys = [ 'id', 'name', 'proposal', 'latitude', 'longitude' ]

# in order to display data we need common keys. This mapping is for society uncommon keys map to common ketys.
society_common_keys = {
    'supplier_id': 'supplier_id',
    'supplier_code': 'supplier_code',
    'society_name': 'name',
    'society_address1': 'address1',
    'society_address2': 'address2',
    'society_locality': 'area',
    'society_subarea': 'subarea',
    'society_city': 'city',
    'society_state': 'state',
    'society_zip': 'zipcode',
    'society_latitude': 'latitude',
    'society_longitude': 'longitude',
    'society_type_quantity': 'locality_rating',
    'society_type_quality': 'quality_rating',
}


# export master data. each key represents a list of list. each list in that list forms a row in the sheet
master_data = {
    'RS': {
           'sheet_name': 'Shortlisted Spaces Details',
           'headers': [],
           'data': []
           },
    'CP': {
           'sheet_name': 'Corporate Park Details',
           'headers': [],
           'data': []
    },
}

# chose sheet names from just supplier_type_code
sheet_names = {
    'RS': 'Society Details',
    'CP': 'Corporate Park Details',
    'GY': 'Gym details'
}

# chose codes from supplier sheet names
# sheet_names_to_codes

sheet_names_to_codes = {
    'Society Details': 'RS',
    'Corporate Park Details': 'CP',
    'Gym details': 'GY'
}


# supplier keys which you want to be included in the sheet in specific order. do not change this order.
# header keys must be in sync with these keys. The following keys will be queried  in db of respective
# supplier models so keys names must match with db column names.

export_supplier_database_keys = {
    'RS': [ 'id', 'proposal', 'center_name', 'supplier_id', 'society_name', 'society_subarea', 'society_type_quality', 'tower_count', 'flat_count', ],
    'CP': [ 'id', 'proposal', 'center_name',  'supplier_id', 'name', 'subarea']
}

# these HEADER keys are specific to the supplier. the sequence and count of HEADER keys must match with sequence
# and count of database keys.
export_supplier_header_keys = {

    'RS': ['CENTER_ID', 'CENTER_NAME', 'PROPOSAL', 'SUPPLIER_ID', 'SOCIETY NAME', 'SOCIETY_SUBAREA',
           'SOCIETY_TYPE_QUALITY', 'TOWER_COUNT', 'FLAT_COUNT'],
    'CP': ['CENTER_ID', 'CENTER_NAME', 'PROPOSAL', 'SUPPLIER_ID', 'CORPORATE NAME', 'CORPORATE SUBAREA']
}

# lead keys
lead_keys = ['name', 'email', 'phone', 'address', 'gender', 'age', 'lead_type', 'lead_status']

# filters. the following dict maps supplier specific filters to database fields directly
supplier_filters = {
    'CP': {
        'real_estate_allowed': 'isrealestateallowed',
        'building_count': 'building_count',
    },
    'RS': {
    }
}

# from the front end we recieve only the codes, hence there is a mapping to actual values. Do not change it's name
quality_dict = {
    'UH': 'Ultra High',
    'HH': 'High',
    'MH': 'Medium High',
    'ST': 'Standard'
}
# from the front end we recieve only the codes, hence there is a mapping to actual values. Do not change it's name.
locality_dict = {
    'UH': 'Ultra High',
    'HH': 'High',
    'MH': 'Medium High',
    'ST': 'Standard'
}
# from the front end we recieve only the codes, hence there is a mapping to actual values
inventory_dict = {
    'PO': 'poster_allowed_nb',
    'ST': 'standee_allowed',
    'SL': 'stall_allowed',
    'FL': 'flier_allowed',
    'BA': 'banner_allowed',
    'CD': 'car_display_allowed',
}
# from the front end we recieve only the codes, hence there is a mapping to actual values. Do not change it's name.
quantity_dict = {
    'LA': 'Large',
    'MD': 'Medium',
    'VL': 'Very Large',
    'SM': 'Small',
}
# from the front end we recieve only the codes, hence there is a mapping to actual values
flat_type_dict = {
    '1R': '1 RK',
    '1B': '1 BHK',
    '1-5B': '1.5 BHK',
    '2B': '2 BHK',
    '2-5B': '2.5 BHK',
    '3B': '3 BHK',
    '3-5B': '3.5 BHK',
    '4B': '4 BHK',
    '5B': '5 BHK',
    'PH': 'PENT HOUSE',
    'RH': 'ROW HOUSE',
    'DP': 'DUPLEX'
}
# currently some db columns which mean the same are named differently in society and other suppliers. hence in order to
# to reduce code, this is a mapping for each type of supplier, from the term we get from front end to the term
# that is there in db as a column
query_dict = {
    'RS': {
        'quantity': {'query': 'society_type_quantity__in',
                     'dict': quantity_dict
                     },
        'quality': {'query': 'society_type_quality__in',
                    'dict': quality_dict
                   },
        'locality': {'query': 'society_location_type__in',
                     'dict': locality_dict
                    }
    },
    'CP': {
        'quantity': {'query': 'quantity_rating__in',
                     'dict': quantity_dict,
                    },
        'quality': {'query': 'quality_rating__in',
                    'dict': quality_dict
                   },
        'locality': {'query': 'locality_rating__in',
                     'dict': locality_dict
                    }
    }
}
# searching fields per supplier
search_fields = {
    'RS': ['supplier_id__icontains', 'society_name__icontains', 'society_address1__icontains',
           'society_city__icontains',
           'society_state__icontains'
           ],
    'CP': ['supplier_id__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains', 'area__icontains',
           'subarea__icontains',
           'city__icontains', 'state__icontains', 'zipcode__icontains'
           ]
}

# to calculate what cost of each inventory. currently we are using only these. type and duration are used to fetch
# inventory type objects adn duration type objects.
inventory_duration_dict = {
    'PO': {'name': 'POSTER', 'type_duration': [{'type': 'poster_a4', 'duration': 'campaign_weekly'}]},
    'ST': {'name': 'STANDEE', 'type_duration': [{'type': 'standee_small', 'duration': 'campaign_weekly'}]},
    'SL': {'name': 'STALL',   'type_duration':  [{'type': 'stall_small', 'duration': 'unit_daily'}]},
    'FL': {'name': 'FLIER', 'type_duration': [{'type': 'flier_door_to_door', 'duration': 'unit_daily'}, ]},
    'CD': {'name': 'CAR DISPLAY', 'tye_duration':  [{'type': 'car_display_price', 'duration': 'unit_daily'}]}
}

# format to be used in datetime
datetime_format = '%d-%m-%Y %H-%M-%S'

# metric file details
metric_file_path = BASE_DIR + '/files/empty_proposal_cost_data.xlsx'
metric_sheet_name = 'Offline Pricing'
