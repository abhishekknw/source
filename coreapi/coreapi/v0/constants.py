model_names = ['InventorySummary', 'ContactDetails', 'Events', 'FlyerInventory', 'ImageMapping', 'PosterInventory',
               'SocietyTower', 'PriceMappingDefault', 'SocietyInventoryBooking', 'StallInventory', 'WallInventory','FlatType' ]


# we have group_name and there respective codes. These codes are designed to respect the heirarchy of various kinds of
# users we have in our system
group_codes = {
    'master_users': '0',
    'ops_heads': '01',
    'bd_heads': '02',
    'external_bds': '03',
    'general_bd_user': '020'
}

# model_name_to_user_mapping
model_name_user_mapping = {
    'AccountInfo': 'business__user__user_code',
    'ProposalInfo': 'account__business__user__user_code',
}

# the following is dict of valid amenities for supppliers
valid_amenities_code_name = {
    'GY': 'GYM',
    'GA': 'GARDEN',
    'PA': 'PLAY AREA',
    'SP': 'SWIMMING POOL'
}

# quadrant code
first_quadrant_code = '1'
second_quadrant_code = '2'
third_quadrant_code = '3'
fourth_quadrant_code = '4'

# custom database name
database_name = 'custom_api_database'

# max flat count per society
flat_type_default_params = {
    '1R': {"count": 20, "size": 1000},
    '1B': {"count": 50, "size": 1500},
    '1-5B': {"count": 60, "size": 2000},
    '2B': {"count": 70, "size": 2500},
    '2-5B': {"count": 75, "size": 3000},
    '3B': {"count": 30, "size": 3200},
    '3-5B': {"count": 35, "size": 4500},
    '4B': {"count": 40, "size": 5000},
    '5B': {"count": 45, "size": 5500},
    'PH': {"count": 50, "size": 6000},
    'RH': {"count": 55, "size": 6500},
    'DP': {"count": 60, "size": 7000}
}

# default tower range
default_tower_range = [1, 4]
default_tower_base_name = "Tower"

# default possession year range
default_possession_year_range = [2000, 2017]
default_percentage_range_of_tenants_to_flat = [0, 100]
default_flat_avg_rental_persqft_range = [0, 2000]
default_flat_sale_cost_persqft_range = [0, 3000]


# inventory constants
default_poster_per_tower = 6
default_standee_per_tower = 3
default_stall_per_society = 1
default_flier_frequency_per_society = 4

# Guest User code
guest_user_code = '99'

# website constants

from coreapi.settings import BASE_DIR

# all inventory codes
poster_inventory_code = 'PO'
standee_inventory_code = 'ST'
stall_inventory_code = 'SL'
flier_inventory_code = 'FL'
car_display_inventory_code = 'CD'

glass_facade_inventory_code = 'GF'
hoarding_inventory_code = 'HO'
dropdown_inventory_code = 'DD'
promotion_desk_inventory = 'PD'
pillar_inventory_code = 'PI'
trolley_inventory_code = 'TR'
wall_inventory_code = 'WA'
floor_inventory_code = 'FO'

# to identify unique supplier types
society = 'RS'
corporate = 'CP'
gym = 'GY'
salon = 'SA'
bus_shelter = 'BS'
retail_shop_code = 'RE'
bus_depot_code = 'BD'
educational_institute = 'EI'
hording = 'HO'
bus = 'BU'
gantry = 'GN'
radio_channel = 'RC'
tv_channel = 'TV'

# all supplier codes
society_code = 'RS'
corporate_code = 'CP'

educational_institute_code = 'EI'
hording_code = 'HO'



# yes or no
positive = ['Yes', 'Y', '1']
negative = ['No', 'N', '0']

valid_supplier_codes = [society, corporate, gym, salon, bus_shelter, bus_depot_code, retail_shop_code, educational_institute_code, hording_code, bus, gantry, radio_channel, tv_channel]

supplier_keys = [

    'city', 'city_code', 'society_locality', 'area_code', 'society_subarea', 'subarea_code', 'supplier_type', 'supplier_code', 'society_name'

    , 'society_address1', 'society_address2', 'society_zip', \
 \
    'society_latitude', 'society_longitude', 'possession_year', 'tower_count', 'flat_count', \
 \
    'vacant_flat_count', 'service_household_count', 'working_women_count', 'avg_household_occupants', \
    'bachelor_tenants_allowed', 'flat_avg_rental_persqft', 'cars_count', 'luxury_cars_count', \
    'society_location_type', 'society_type_quality', 'society_type_quantity', 'count_0_5', 'count_5_15', \
    'count_15_25', 'count_25_60', 'count_60above', 'society_weekly_off',
]

basic_supplier_export_headers = ['City', 'City Code', 'Area', 'Area Code', 'Sub Area', 'Sub Area Code', 'SupplierType', 'SupplierCode', 'SupplierName', 'supplier_id', 'Error']
basic_supplier_data_keys = ['city_name', 'city_code', 'area_name', 'area_code', 'subarea_name', 'subarea_code', 'supplier_type_code', 'supplier_code', 'supplier_name', 'supplier_id', 'error']

corporate_keys = [

    'city', 'city_code', 'area', 'area_code', 'subarea', 'subarea_code', 'supplier_type', 'supplier_code', 'name', 'address1', \
    'address2', 'zipcode', 'latitude', 'longitude', 'corporate_type', 'industry_segment', 'building_count', 'floorperbuilding_count', \
    'totallift_count', 'locality_rating', 'quality_rating', 'quantity_rating', 'totalemployees_count', 'isrealestateallowed', \
    'averagerent', 'commoncafeteria', 'bank_account_name', 'bank_name', 'ifsc_code', 'account_number'

]

proposal_header_keys = [
    'Center Name', 'Center Proposal Id', 'Center Id', 'Space Mapping Id', 'Inventory Type Id', 'Supplier Id', 'Supplier Name', 'Supplier Sub Area', 'Supplier Type', 'Supplier Tower Count', \
    'Supplier Flat Count',
]

inventorylist = {
    'PO': {
        'HEADER': ['Poster Allowed', 'Poster price type', 'Poster price available', 'Poster Price', 'Poster Price Factor', 'Poster price per flat', 'Poster Business Price'],
        'DATA': ['poster_allowed', 'poster_price_type', 'poster_price_available',  'poster_price', 'poster_price_factor', 'poster_price_per_flat', 'poster_business_price']
    },
    'ST': {
        'HEADER': ['Standee Allowed', 'Standee price type', 'Standee price available',   'Standee Price', 'Standee Price factor','Standee price per flat', 'Standee Business Price'],
        'DATA': ['standee_allowed',  'standee_price_type', 'standee_price_available',   'standee_price',  'standee_price_factor',
                 'standee_price_per_flat', 'standee_business_price']
    },
    'FL': {
        'HEADER': ['Flier Allowed', 'Flier price type', 'Flier price available',  'Flier Price',  'Flier Price Factor', 'Flier Business Price'],
        'DATA': ['flier_allowed',  'flier_price_type', 'flier_price_available',   'flier_price',  'flier_price_factor', 'flier_business_price']
    },
    'SL': {
        'HEADER': ['Stall Allowed', 'Stall price type', 'Stall price available',   'Stall Price',  'Stall Price Factor', 'Stall Business Price'],
        'DATA': ['stall_allowed', 'stall_price_type', 'stall_price_available',  'stall_price', 'stall_price_factor', 'stall_business_price']
    },
    'CD': {
        'HEADER': ['Car Display Allowed', 'Car Display price type', 'Car Display price available',  'Car Display Price', 'Car Display Price Factor', 'Car Display Business Price'],
        'DATA': ['car_display_allowed', 'car_display_price_type', 'car_display_price_available',  'car_display_price', 'car_display_price_factor', 'car_display_business_price']
    },
    society_code: {
        'HEADER': ['SUPPLIER ID', 'SOCIETY NAME', 'SOCIETY SUBAREA', 'SOCIETY TYPE QUALITY', 'TOWER COUNT', 'FLAT COUNT', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'quality_rating', 'tower_count', 'flat_count', 'status']
    },
    corporate_code: {
        'HEADER': ['SUPPLIER_ID', 'CORPORATE NAME', 'CORPORATE SUBAREA', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'status']
    },
    educational_institute_code:{
        'HEADER': ['SUPPLIER_ID', 'CORPORATE NAME', 'CORPORATE SUBAREA', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'status']
    },
    hording_code:{
        'HEADER': ['SUPPLIER_ID', 'CORPORATE NAME', 'CORPORATE SUBAREA', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'status']
    },
    bus_shelter: {
        'HEADER': ['SUPPLIER_ID', 'BUS SHELTER NAME', 'BUS SHELTER SUBAREA', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'status']
    },
    gym: {
        'HEADER': ['SUPPLIER_ID', 'GYM NAME', 'GYM SUBAREA', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'status']
    },
    salon: {
        'HEADER': ['SUPPLIER_ID', 'SALON NAME', 'SALON SUBAREA', 'STATUS'],
        'DATA': ['supplier_id', 'name', 'subarea', 'status']
    },
    retail_shop_code: {

        'HEADER': ['SUPPLIER_ID', 'RETAIL SHOP NAME', 'RETAIL SUBAREA', 'STATUS'],
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
    'city', 'city_code', 'area', 'area_code', 'sub_area', 'subarea_code', 'supplier_type', 'society_name', 'supplier_code', 'contact_type', 'salutation', \
    'name', 'landline', 'mobile', 'email'
]

STD_CODE = '022'
COUNTRY_CODE = '+91'

price_per_flat = {
    'PO': ['poster_price_per_flat', 'poster_price'],
    'ST': ['standee_price_per_flat', 'standee_price'],
    'CD': ['car_display_price_per_flat', 'car_display_price'],
    'SL': ['stall_price_per_flat', 'stall_price'],
    'FL': ['flier_price_per_flat', 'filer_price'],  # todo: change the spelling from filer to flier once fixed
}


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

                    'STANDEE': 'standee_allowed', 'STALL': 'stall_allowed'}

index_of_center_id = 0

header_to_field_mapping = {
    'center name': 'center_name',
    'center proposal id': 'prop'

}

# inventory related fields in the sheet
inventory_fields = ['poster_count', 'stall_count', 'flier_count', 'standee_count', 'poster_price', 'stall_price', 'flier_price', 'standee_price']

# this list is used to know if a particular inventory was really present in the sheet
is_inventory_available = ['poster_count', 'stall_count', 'standee_count', 'flier_count']

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

        {'match_term': 'Societies Covered ', 'col_name': 'metric_name', 'specific': {'code': 'RS',}, 'value': 0},
        {'match_term': 'Corporate Parks Covered', 'col_name': 'metric_name', 'specific': {'code': 'CP'}, 'value': 0},

        {'match_term': 'Total Society Impressions', 'col_name': 'metric_name', 'specific': {'code': 'RS'}, 'value': 0},
        {'match_term': 'Total Corporates Impressions', 'col_name': 'metric_name', 'specific': {'code': 'CP',}, 'value': 0},

        {'match_term': 'Average Cost per Corporate', 'col_name': 'metric_name', 'specific': {'code': 'CP'}, 'value': 0},
        {'match_term': 'Average Cost per Society', 'col_name': 'metric_name', 'specific': {'code': 'RS'}, 'value': 0},
        {'match_term': 'Average Cost per Gym', 'col_name': 'metric_name', 'specific': {'code': 'GY'}, 'value': 0},
        {'match_term': 'Average Cost per Salon', 'col_name': 'metric_name', 'specific': {'code': 'SA'}, 'value': 0},

        {'match_term': 'Estimated Flat Covered', 'col_name': 'metric_name', 'specific': {'code': 'RS',}, 'value': 0},
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
get_spaces_api_center_keys = ['id', 'name', 'proposal', 'latitude', 'longitude']

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

# define sheet names
salon_sheet_name = 'Salon Details'
gym_sheet_name = 'Gym Details'
bus_shelter_sheet_name = 'Bus shelter Details'
retail_shop_sheet_name = 'Retail Shop Details'
society_sheet_name = 'Society Details'
corporate_sheet_name = 'Corporate Park Details'
educational_institute_sheet_name = 'Educational Institute Details'
hording_sheet_name = 'Hording Details'



# export master data. each key represents a list of list. each list in that list forms a row in the sheet
master_data = {
    society_code: {
        'sheet_name': 'Shortlisted Spaces Details',
        'headers': [],
        'data': []
    },
    corporate_code: {
        'sheet_name': 'Corporate Park Details',
        'headers': [],
        'data': []
    },
    bus_shelter: {
        'sheet_name': bus_shelter_sheet_name,
        'headers': [],
        'data': []
    },
    gym: {
        'sheet_name': gym_sheet_name,
        'headers': [],
        'data': []

    },
    salon: {
        'sheet_name': salon_sheet_name,
        'headers': [],
        'data': []
    },
    retail_shop_code: {
        'sheet_name': retail_shop_sheet_name,
        'headers': [],
        'data': []
    },
    educational_institute_code:{
        'sheet_name': educational_institute_sheet_name,
        'headers': [],
        'data': []
    },
    hording_code:{
        'sheet_name': educational_institute_sheet_name,
        'headers': [],
        'data': []
    },
}

# chose sheet names from just supplier_type_code
sheet_names = {
    society_code: society_sheet_name ,
    corporate_code: corporate_sheet_name,
    gym: gym_sheet_name,
    salon: salon_sheet_name,
    bus_shelter: bus_shelter_sheet_name,
    retail_shop_code: retail_shop_sheet_name,
    educational_institute_code:educational_institute_sheet_name,
    hording_code:hording_sheet_name
}

# chose codes from supplier sheet names
# sheet_names_to_codes
sheet_names_to_codes = {
    society_sheet_name: society_code,
    corporate_sheet_name: corporate_code,
    gym_sheet_name: gym,
    salon_sheet_name: salon,
    bus_shelter_sheet_name: bus_shelter,
    retail_shop_sheet_name: retail_shop_code,
    educational_institute_sheet_name:educational_institute_code,
    hording_sheet_name:hording_code
}

# code to sheet names
code_to_sheet_names = {
    'RS': 'Society Details',
    'CP': 'Corporate Park Details',
    'GY': 'Gym details',
    'EI': 'Educational Institute Details',
    'HO': 'Hording Details'
}

# supplier keys which you want to be included in the sheet in specific order. do not change this order.
# header keys must be in sync with these keys. The following keys will be queried  in db of respective
# supplier models so keys names must match with db column names.

export_supplier_database_keys = {
    'RS': ['id', 'proposal', 'center_name', 'supplier_id', 'society_name', 'society_subarea', 'society_type_quality', 'tower_count', 'flat_count', ],
    'CP': ['id', 'proposal', 'center_name', 'supplier_id', 'name', 'subarea'],
    'EI': ['id', 'proposal', 'center_name', 'supplier_id', 'name', 'subarea'],
    'HO': ['id', 'proposal', 'center_name', 'supplier_id', 'name', 'subarea'],
    bus_shelter: [],
    gym: [],
    salon: []

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
    corporate_code: {
        'real_estate_allowed': 'isrealestateallowed',
        'building_count': 'building_count',
    },
    society_code: {
    },
    bus_shelter: {},
    gym: {},
    salon: {},
    educational_institute: {},
    hording: {}
}

# pi filters which come in range fashion. These filters are used in PI calculation
pi_range_filters = {
    society_code: {
        'flat_avg_rental_persqft': 'flat_avg_rental_persqft',
        'flat_sale_cost_persqft': 'flat_sale_cost_persqft',
        'possession_year': 'age_of_society'
    },
    corporate_code: {},
    bus_shelter: {},
    gym: {},
    salon: {},
    educational_institute: {},
    hording: {}
}

# Filter names which do not map directly to db field
tenants_to_flat_count = 'percentage_of_tenants_to_flat_count'

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

flat_type_name_to_code = {

    '1 RK': '1R',
    '1 BHK': '1B',
    '1.5 BHK': '1-5B',
    '2 BHK': '2B',
    '2.5 BHK': '2-5B',
    '3 BHK': '3B',
    '3.5 BHK': '3-5B',
    '4 BHK': '4B',
    '5 BHK': '5B',
    'PENT HOUSE': 'PH',
    'ROW HOUSE': 'RH',
    'DUPLEX': 'DP'

}
# currently some db columns which mean the same are named differently in society and other suppliers. hence in order to
# to reduce code, this is a mapping for each type of supplier, from the term we get from front end to the term
# that is there in db as a column
query_dict = {
    society_code: {
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
    corporate_code: {
        'quantity': {'query': 'quantity_rating__in',
                     'dict': quantity_dict,
                     },
        'quality': {'query': 'quality_rating__in',
                    'dict': quality_dict
                    },
        'locality': {'query': 'locality_rating__in',
                     'dict': locality_dict
                     }
    },

    gym: {
        'quantity': { },
        'quality': {},
        'locality': {}
    },
    salon: {
        'quantity': {},
        'quality': {},
        'locality': {}
    },
    bus_shelter: {
        'quantity': {},
        'quality': {},
        'locality': {}
    },
    retail_shop_code: {
        'quantity': {},
        'quality': {},
        'locality': {}
    },
    educational_institute_code: {
        'quantity': {},
        'quality': {},
        'locality': {}
    },
    hording_code: {
        'quantity': {},
        'quality': {},
        'locality': {}
    },
}

# searching fields per supplier
search_fields = {
    society_code: ['supplier_id__icontains', 'society_name__icontains', 'society_address1__icontains',
           'society_city__icontains', 'society_locality__icontains',
           'society_state__icontains'
           ],
    corporate_code: ['supplier_id__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains', 'area__icontains',
           'subarea__icontains',
           'city__icontains', 'state__icontains', 'zipcode__icontains'
           ],
    bus_shelter: ['supplier_id__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains', 'area__icontains',
           'subarea__icontains',
           'city__icontains', 'state__icontains', 'zipcode__icontains'
           ],
    gym: ['supplier_id__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains', 'area__icontains',
           'subarea__icontains',
           'city__icontains', 'state__icontains', 'zipcode__icontains'
           ],
    salon: ['supplier_id__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains', 'area__icontains',
           'subarea__icontains',
           'city__icontains', 'state__icontains', 'zipcode__icontains'
           ],
    retail_shop_code:['supplier_id__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains', 'area__icontains',
           'subarea__icontains',
           'city__icontains', 'state__icontains', 'zipcode__icontains'
           ],
    educational_institute_code:['supplier_id__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains', 'area__icontains',
           'subarea__icontains',
           'city__icontains', 'state__icontains', 'zipcode__icontains'
           ],
    hording_code:['supplier_id__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains', 'area__icontains',
            'subarea__icontains',
            'city__icontains', 'state__icontains', 'zipcode__icontains'
            ],
}

# to calculate what cost of each inventory. currently we are using only these. type and duration are used to fetch
# inventory type objects adn duration type objects.
inventory_duration_dict = {
    'PO': {'name': 'POSTER', 'type_duration': [{'type': 'poster_a4', 'duration': 'campaign_weekly'}]},
    'ST': {'name': 'STANDEE', 'type_duration': [{'type': 'standee_small', 'duration': 'campaign_weekly'}]},
    'SL': {'name': 'STALL', 'type_duration': [{'type': 'stall_small', 'duration': 'unit_daily'}]},
    'FL': {'name': 'FLIER', 'type_duration': [{'type': 'flier_door_to_door', 'duration': 'unit_daily'}, ]},
    'CD': {'name': 'CAR DISPLAY', 'tye_duration': [{'type': 'car_display_price', 'duration': 'unit_daily'}]}
}

inventory_type_duration_dict = {
    'PO': {'name': 'POSTER', 'type_duration': [{'type': 'a4', 'duration': 'campaign_weekly'}]},
    'ST': {'name': 'STANDEE', 'type_duration': [{'type': 'small', 'duration': 'campaign_weekly'}]},
    'SL': {'name': 'STALL', 'type_duration': [{'type': 'small', 'duration': 'unit_daily'}]},
    'FL': {'name': 'FLIER', 'type_duration': [{'type': 'door_to_door', 'duration': 'unit_daily'}, ]},
}

# this is used in setting pricing when FilteredSuppliers API is hit
inventory_type_duration_dict_list = {
    'PO': ['POSTER', 'A4', 'Campaign Weekly'],
    'ST': ['STANDEE', 'Small', 'Campaign Weekly'],
    'SL': ['STALL', 'Small', 'Unit Daily'],
    'FL': ['FLIER', 'Door-to-Door', 'Unit Daily'],
    'CD': ['CAR DISPLAY', 'Standard', 'Unit Daily'],
    'GA': ['Gateway Arch', 'Non Lit', 'Unit Quaterly'],
    'SB': ['SUNBOARD', 'Normal', 'Unit Quaterly'],
    'BA': ['BANNER', 'Small', 'Campaign Weekly']
}

# this dict maps keys directly to db values. do not change
duration_dict = {
    'campaign_weekly': 'Campaign Weekly',
    'campaign_monthly': 'Campaign Monthly',
    'unit_weekly': 'Unit Weekly',
    'unit_monthly': 'Unit Monthly',
    'unit_daily': 'Unit Daily',
    'two_days': '2 Days'
}
# this dict maps keys directly to db values. do not change
type_dict = {
    'a4': 'A4',
    'a3': 'A3',
    'small': 'Small',
    'medium': 'Medium',
    'large': 'Large',
    'canopy': 'Canopy',
    'customize': 'Customize',
    'standard': 'Standard',
    'premium': 'Premium',
    'door_to_door': 'Door-to-Door',
    'mail_box': 'Mailbox',
    'lobby': 'Lobby',
    'normal': 'Normal'
}

# format to be used in datetime
datetime_format = '%d-%m-%Y %H-%M-%S'

# metric file details
metric_file_path = BASE_DIR + '/files/empty_proposal_cost_data.xlsx'
metric_sheet_name = 'Offline Pricing'

# settings to tune in generation of proposal_id
business_letters = 4
account_letters = 4
# send only this much characters in response
proposal_id_limit = 5

# a list ot tuples where each tuple says the inventory_type, duration, and  column indexes where pricing information of
#  inventories is stored. These are used to populate price_mapping_default() table.
current_inventories = [('poster_a4', 'campaign_weekly', 6), ('standee_small', 'campaign_weekly', 18), ('stall_small', 'unit_daily', 23), ('car_display_standard', 'unit_daily', 30), ('flier_door_to_door', 'unit_daily', 41)]

# shortlisted_inventory_pricing_keys
shortlisted_inventory_pricing_keys = ['supplier_id', 'supplier_type_code', 'inventory_price', 'inventory_count', 'factor']

# valid email fields
valid_email_keys = ['subject', 'body', 'to']

# MIME types

mime = {
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}

# email subject, body templates
email = {
    'subject': 'Test subject',
    'body': 'This a system generated mail. Please find the file named $file attached',
    'to': ['kshitij.mittal01@gmail.com']
}

# filter types
filter_type = {
    society_code: ['inventory_type_selected', 'quality_type', 'quantity_type', 'locality_rating', 'flat_type'],
    corporate_code: ['inventory_type_selected', 'quality_type', 'quantity_type', 'locality_rating', 'employee_count'],
    bus_shelter: [],
    gym: [],
    salon: [],
    retail_shop_code: [],
    educational_institute_code:[],
    hording_code:[]

}
# to store employee_count
employee_count_codes = {
    0: 'SM',
    1000: 'MD',
    3000: 'LA',
    6000: 'VL',
}
# status of suppliers which are in get_spaces(), not in
status = 'S'
shortlisted = 'S'
removed = 'R'
buffer = 'B'
finalized = 'F'
valid_statuses = [shortlisted, removed, buffer]

# name of inventories as in db
poster = 'POSTER'
standee = 'STANDEE'
stall = 'STALL'
flier = 'FLIER'
car_display = 'CAR DISPLAY'


# subjects:
subjects = {
    'agency': 'Your proposal request has been received',
    'bd_head': 'A new Proposal request has been received'
}

# body
bodys = {
    'agency': 'Hi, your proposal request has been received and machadalo team will contact you !',
    'bd_head': 'Please find following details of proposal:  \n \n User Name: $user_name '
               '\n Business: $business \n Account: $account \n Proposal: $proposal_id \n '
               ' and the sheet \t  $file_name \t attached'
}

# default emails
emails = {
    'bd_head': 'dev@machadalo.com',
    'bd_user': 'anmol.prabhu@machadalo.com',
    'root_user': 'anupam@machadalo.com'
}

# default status of each inventory is defined here. The reason i didn't chose a boolean value is because may be in
# future there can be more than two status of an inventory. who knows  ?
inventory_status = 'F'  # F stands for free or available.
inventory_booked_status = 'B'

# shortlisted inventory details keys
shortlisted_inventory_detail_keys = ['inventory_price', 'inventory_count', 'factor', 'ad_inventory_type', 'ad_inventory_duration']

# model names as store in ContentType table. update here if you change the model names.
society_model_name = 'suppliertypesociety'

# stall_settings
default_stall_type = 'Small'
default_stall_duration_type = 'Unit Daily'
default_stall_allocation_interval = 1
default_stall_assignment_frequency = 1

# temp list of inventories not implemented yet. delete it after implemantation.
inv_not_implemented = []

# standee configs
standee_name = 'STANDEE'
default_standee_type = 'Medium'
default_standee_duration_type = 'Unit Weekly'
default_standee_assignment_frequency = 1

# poster configs
poster_name = 'POSTER'
default_poster_type = 'A4'
default_poster_duration_type = 'Unit Weekly'
default_poster_assignment_frequency = 1

# Flier configs
default_flier_type = 'Mailbox'
default_flier_duration_type = 'Unit Daily'
default_flier_assignment_frequency = 1

# class names. change them when class name changes.
stall_class_name = 'StallInventory'
standee_class_name = 'StandeeInventory'
flier_class_name = 'FlyerInventory'
poster_class_name = 'PosterInventory'

# different states of a proposal being converted to campaign
proposal_converted_to_campaign = 'PTC'
proposal_not_converted_to_campaign = 'PNC'
proposal_on_hold = 'POH'
proposal_requested = 'PR'
proposal_finalized = 'PF'

campaign_state = {
    'PTC': 'converted',
    'PNC': 'not converted',
    'POH': 'on hold',
    'PR': 'requested',
    'PF': 'finalized'
}


# different mode of payments
payment_method = {
    'cash': 'CASH',
    'neft': 'NEFT',
    'cheque': 'CHEQUE'
}

# different payments statuses
payment_status = {
    'payment_done': 'PD',
    'payment_not_initiated': 'PNI',
    'payment_pending': 'PP',
    'check_released' : 'PCR',
    'payment_rejected' : 'PR'
}

payment_code_to_status = {
    'PD': 'Payment Done',
    'PNI': 'Payment Not Initiated',
    'PP': 'Payment Pending',
    'PCR': 'Cheque Released',
    'PR': 'Payment Rejected',
}

booking_priority_code_to_status = {
    'VH': 'Very High',
    'HH': 'High'
}

# supplier booking status
booking_status = {
    'booked': 'BK',
    'unknown': 'UN',
    'not_booked': 'NB',
    'phone_booked' : 'PB',
    'visit_booked' : 'VB',
    'rejected' : 'SR',
    'send_email' : 'SE',
    'visit_required' : 'VR',
    'call_required' : 'CR',
    'decision_pending' : 'DP',
    'tentative_booking' : 'TB',
    'new_entity': 'NE',
    'not_initiated': 'NI',
    'recce':'RE',
    'meeting_fixed':'MF',
    'meeting_converted':'MC',
    'complete_lockdown': 'LCL',
    'partial_lockdown': 'LPL',
    'open_lockdown': 'LOL',
    'emergency_system': 'LES',
    'essential_required': 'LER',
    'medicine_required': 'LMR',
    'vegetables_fruits_required': 'LVR'
}

booking_code_to_status = {
    'BK': 'Confirmed Booking',
    'NB': 'Not Booked',
    'PB': 'Phone Booked',
    'VB': 'Visit Booked',
    'SR': 'Rejected',
    'SE': 'Send Email',
    'VR': 'Visit Required',
    'CR': 'Call Required',
    'DP': 'Decision Pending',
    'TB': 'Tentative Booking',
    'NE': 'New Entity',
    'NI': 'Not Initiated',
    'RE': 'Recce',
    'MF': 'Meeting Fixed',
    'MC': 'Meeting Converted',
    'CM': 'completed',
    'UN': 'unknown',
    'LCL': 'Complete Lockdown',
    'LPL': 'Partial Lockdown',
    'LOL': 'Open Lockdown',
    'LES': 'Emergency System',
    'LER': 'Essential Required',
    'LMR': 'Medicine Required',
    'LVR': 'Vegetables & Fruits Required',
    'CM': 'Completed',
    'BSR': 'Rejected',
    'BDP': 'Decision Pending',
    'BNI': 'Not Initiated',
    'BNE': 'New Entity',
    'BUN': 'Unknown',
    'OEL': 'Emergency Situation',
    'OCL': 'Complete Lockdown',
    'OPBL': 'Partial Building/Tower Lockdown',
    'OPFL': 'Partial Floor Lockdown',
    'OPHL': 'Partial House/Flat Lockdown',
    'OP': 'OPEN'
}

booking_substatus_code_to_status = {
    'UPNI': 'Phone Number Issue',
    'UCPI': 'Contact Person Issue',
    'MWA': 'Meeting with AGM',
    'MWS': 'Meeting with Secretory',
    'MWC': 'Meeting with Chairman',
    'MWT': 'Meeting with Treasurer',
    'MWO': 'Meeting with Other',
    'DPRR': 'Recce Required',
    'RERA': 'Recce Approved',
    'DPVR': 'Visit Required',
    'DPCR': 'Call Required',
    'DPNR': 'Negotiation Required',
    'DPNA': 'Not Available',
    'DPP': 'Postponed',
    'DPSOO': 'Specific Occasion Only',
    'DPOS': 'DP Others',
    'RLO': 'Less occupancy',
    'RLC': 'Less Children',
    'RUB': 'Under Builder',
    'RVE': 'Very Expensive',
    'RCR': 'Client Rejected',
    'RRS': 'Rejected by Society',
    'ROS': 'Rejected Others',
    'PB': 'Phone Booking',
    'VB': 'Visit Booking',
    'NVW': 'Wikimapia',
    'NVG': 'Google',
    'NVA': '99Acres',
    'NVMB': 'Magic Brick',
    'NVFT': 'First Time Assigned',
    'NVOS' : 'NE Others'
}

# different campaign states
completed = 'COMPLETED'
running = 'RUNNING'
upcoming = 'UPCOMING'
unknown = 'UNKNOWN'

# to fetch default inventory duration type.
default_inventory_durations = {
    'stallinventory': 1,
    'standeeinventory': 7,
    'flyerinventory': 1
}

# define number of days within which we will show the campaigns.
delta_days = 3

# activity type
activity_type = {
    'RELEASE': 'RELEASE',
    'CLOSURE': 'CLOSURE',
    'AUDIT': 'AUDIT'
}


# standalone society configs
standalone_society_config = {
    'tower_count': 2,
    'flat_count': 70,
    'amenity_count': 3
}

# random pattern length
pattern_length = 6

# inventory_code to name
inventory_code_to_name = {
    'PO': poster,
    'SL': stall,
    'FL': flier,
    'ST': standee,
    'CD': car_display
}

# inventories which  have a model and object_id, content_type fields
inventories_with_object_id_fields = [poster_inventory_code, standee_inventory_code, flier_inventory_code, stall_inventory_code]

# valid extensions to be eligible for deletion of files
valid_extensions = ['xlsx']

# amenity count threshold
amenity_count_threshold = 3

# defaults if these doesn't exist in the database
default_inventory_count = -1
default_inventory_price = -1
default_inventory_duration = 'NOT AVAILABLE'

# default string for ASSIGNED TO NONE
default_assigned_to_string = 'ASSIGNED TO NONE'

# default code for city, area, subarea if not in database
not_in_db_special_code = 'XXXX'

# name of file which is generated when all_supplier_data is hit
all_supplier_data_file_name = 'files/all_supplier_data.xlsx'

# new supplier header names
supplier_headers = {

    'base-data': {

        'basic_data': [
            'city', 'city_code', 'area', 'area_code', 'sub area', 'sub area code', 'supplier type', 'supplier code', 'supplier name',
            'address1', 'address2', 'zip code', 'latitude', 'longitude', 'possession year', 'locality rating', 'quality rating', 'quantity rating',
        ],

        'supplier_specific': {
            'RS': [
                   'tower count', 'flat count', 'vacant flat count', 'service class population', 'working women count', 'average household occupants', 'bachelor tenants allowed', 'car count', 'luxury car count',
                   'age group 0 to 6', 'age group 7 to 18', 'above 60', 'society weekly off', 'pets allowed',
                   'number of rented flats', 'number of flats rented to bachelors'
                   ]
        },

        'amenities': ['Amenity Swimming Pool Present', 'Amenity Play Area Present', 'Amenity Garden Present', 'Amenity Gym Present', 'Amenity Open Area Present',
                      'Amenity Parking Area Present', 'Amenity Steam Bath Present', 'Amenity Club House Present', 'Amenity Community Hall Present',
                      'Amenity Steam Bath / Sauna  / Jaccuzzi Present'],


        'events': ['Event Holi', 'event Diwali', 'event Independence day', 'event republic day', 'event christmas',
                   'event Ganeshotsav', 'event Dusshehra', 'event Navratri', 'event Sports', 'event New Year',
                   'event Onam', 'event Lohri', 'event Gudi Padwa','event eid', 'event Satyanarayan Puja', 'event Janmashtmi',
                   'event Guru Nanak Jayanti', 'event Makar Sankranti', 'event any other'
                   ],

        'flats': ['Flat 1 RK present', '1 RK Count', '1 RK size', '1 RK Rent',
                  'Flat 1 BHK present', '1 BHK Count', '1 BHK size', '1 BHK Rent',
                  'Flat 1.5 BHK present', '1.5 BHK count', '1.5 BHK size', '1.5 BHK Rent',
                  'Flat 2 BHK present', '2 BHK count', '2 BHK size', '2 BHK rent',
                  'Flat 2.5 BHK present', '2.5 BHK count', '2.5 BHK size', '2.5 BHK rent',
                  'Flat 3 BHK present', '3 BHK count', '3 BHK size', '3 BHK rent',
                  'Flat 3.5 BHK present', '3.5 BHK count', '3.5 BHK size', '3.5 BHK rent',
                  'Flat 4 BHK present', '4 BHK count', '4 BHK size', '4 BHK rent',
                  'Flat 4.5 BHK present', '4.5 BHK count', '4.5 BHK size', '4.5 BHK rent',
                  'Flat 5 BHK present', '5 BHK count', '5 BHK size', '5 BHK rent',
                  'Flat Pent House present', 'Pent house count', 'pent house size', 'pent house rent',
                  'FLat Row house present', 'row house count', 'row house size', 'row house rent',
                  'Flat duplex present', 'duplex count', 'duplex size', 'duplex rent'
                  ]
    },

    'inventory-pricing-data': {

        'basic-data-headers': ['city', 'city_code', 'area', 'area_code', 'sub area', 'sub area code', 'supplier type', 'supplier code', 'supplier name'],

        'inventory-pricing-data-headers': [

            'Poster Allowed On Notice Board', 	'A4 Allowed', 	'A3 Allowed', 	'Notice Board Count',
            'Campaign Price of Posters on Notice Board per Week', 'Price Confidence for NB', 'Poster Allowed in Lift',
            'Total No of lifts',	'Total Posters on all lifts',
            'Campaign Price of Posters in Lift per Week',	'Price Confidence for lift',
            'Number of Posters/Tower', 	'Standee Allowed in Society',	'Small Standee', 	'Medium Standee',
            'Standee count',	'Campaign Price of Standees/Week',	'Standee Price Confidence',	'Number of Standees/Tower',
            'Stalls Allowed', 	'Canopy/Small Allowed',	'Campaign Price of Stall/day(Canopy/Small)',	'Price confidence of Canopy/Small',
            'Stall	Large Allowed',	'Campaign Price of Large/day',	'Price confidence of Large Stall',	'Car Displayed Allowed',
            'Standard Car Display Allowed',	'Campaign Price of Standard Car display',	'Price confidence of Standard Car display',
            'Preimum Car Display Allowed',	'Campaign Price of Premium Car display',	'Price confidence of Premium Car display',
            'Number of Stalls/Car Display Allowed Per Day',	'Flier Distribution Allowed',	'Mailbox Allowed',
            'Door-to-Door Allowed', 'At Lobby(Through Watchman) Allowed', 	'Frequency of Flier Distribution/Month', 	'Campaign Price of Flier/Day',	'Flier Price Confidence'
        ]

    }
}

valid_amenities = {
    'Gym': 'GY',
    'Swimming pool': 'SP',
    'Garden': 'GA',
    'Open Area': 'OA',
    'Play Area': 'PA',
    'Parking Area': 'PAR'
}

valid_events = ['Holi', 'Diwali', 'Republic Day', 'Independence Day', 'Christmas',
                'Ganeshotsav', 'Dusshehra', 'Navratri', 'Sports', 'New Year', 'Onam', 'Lohri', 'Gudi Padwa', 'eid',
                'Satyanarayan Puja', 'Makar Sankranti', 'any other'
                ]

society_db_field_to_input_field_map = {
    'supplier_code': 'supplier_code',
    'society_address1': 'address1',
    'society_name': 'supplier_name',
    'society_city': 'city',
    'society_subarea': 'sub_area',
    'society_address2': 'address2',
    'society_state': 'state_name',
    'society_latitude': 'latitude',
    'society_longitude': 'longitude',
    'society_type_quantity': 'quantity_rating',
    'society_type_quality': 'quality_rating',
    'society_locality': 'locality_rating',
    'age_of_society': 'possession_year',
    'tower_count': 'tower_count',
    'flat_count': 'flat_count',
    'vacant_flat_count': 'vacant_flat_count',
    'service_household_count': 'service_class_population',
    'working_women_count': 'working_women_count',
    'avg_household_occupants': 'average_household_occupants',
    'bachelor_tenants_allowed': 'bachelor_tenants_allowed',
    'cars_count':'car_count',
    'luxury_cars_count': 'luxury_car_count',
    'society_weekly_off': 'society_weekly_off',
    'age_group_0_6': 'age_group_0_to_6',
    'age_group_7_18': 'age_group_7_to_18',
    'total_tenant_flat_count': 'number_of_rented_flats'

}

# these basic fields are common to all kinds of suppliers
basic_db_fields_to_input_field_map = {
    'supplier_code':  'supplier_code',
    'name': 'supplier_name',
    'address1': 'address1',
    'address2': 'address2',
    'area': 'area',
    'subarea': 'sub_area',
    'city': 'city',
    'latitude': 'latitude',
    'longitude': 'longitude'
}


campaign_weekly = 'Campaign Weekly'
campaign_monthly = 'Campaign Monthly'
unit_weekly = 'Unit Weekly'
unit_monthly = 'Unit Monthly'
unit_daily = 'Unit Daily'
two_days = '2 Days'
unit_quaterly = 'Unit Quaterly'

A4 = 'A4'
A3 = 'A3'
small = 'Small'
large = 'Large'
medium = 'Medium'
canopy = 'Canopy'
customize = 'Customize'
standard = 'Standard'
premium = 'Premium'
door_to_door = 'Door-to-Door'
mailbox = 'Mailbox'
lobby = 'Lobby'

allowed = 'allowed'

price_mapping_default_headers = {
    poster: [(allowed,), (A4, campaign_weekly), (A3, campaign_weekly), (A4, campaign_monthly), (A3, campaign_monthly), (A4, unit_weekly), (A3, unit_monthly)],
    standee: [(allowed,), (small, campaign_weekly), (large, campaign_weekly)],
    stall: [(allowed,), (canopy, unit_daily), (canopy, two_days), (small, unit_daily), (small, two_days), (large, unit_daily), (large, two_days), (customize, unit_daily), (customize, two_days)],
    flier: [(allowed,), (door_to_door, unit_daily), (mailbox, unit_daily), (lobby, unit_daily)],
    car_display: [(allowed,), (standard, unit_daily), (standard, two_days), (premium, unit_daily), (premium, two_days)]
}

keys_old = [
    'city', 'city_code',  'area', 'area_code', 'subarea',  'supplier_type', 'supplier_name', 'supplier_code', \
    'poster_allowed_nb', 'nb_A4_allowed', 'nb_A3_allowed', 'nb_count', 'poster_price_week_nb', \
    'nb_price_confidence', 'poster_allowed_lift', 'lift_count', 'total_posters_lift_count', 'poster_price_week_lift', \
    'lift_price_confidence', 'poster_count_per_tower', 'standee_allowed', 'standee_small', 'standee_medium',
    'total_standee_count', \
    'standee_price_week', 'standee_price_confidence', 'standee_count_per_tower', 'stall_allowed', \
    'stall_small', 'stall_price_day_small', 'smallStall_price_confidence', 'stall_large', 'stall_price_day_large', \
    'largeStall_price_confidence', 'car_display_allowed', 'cd_standard', 'cd_price_day_standard',
    'standard_price_confidence  ', \
    'cd_premium', 'cd_price_day_premium', 'premium_price_confidence', 'total_stall_count', 'flier_allowed',
    'mailbox_allowed', \
    'd2d_allowed', 'flier_lobby_allowed', 'flier_frequency', 'flier_price_day', 'flier_price_confidence'
]
keys = [
    'supplier_id', 'poster_allowed_nb', \
    'nb_A4_allowed', 'nb_A3_allowed', 'nb_count', 'poster_price_week_nb', \
    'nb_price_confidence', 'poster_allowed_lift', 'lift_count', 'total_poster_count', 'poster_price_week_lift', \
    'lift_price_confidence', 'poster_count_per_tower', 'standee_allowed', 'standee_small', 'standee_medium',
    'total_standee_count', \
    'standee_price_week', 'standee_price_confidence', 'standee_count_per_tower', 'stall_allowed', \
    'stall_small', 'stall_price_day_small', 'smallStall_price_confidence', 'stall_large', 'stall_price_day_large', \
    'largeStall_price_confidence', 'car_display_allowed', 'cd_standard', 'cd_price_day_standard',
    'standard_price_confidence', \
    'cd_premium', 'cd_price_day_premium', 'premium_price_confidence', 'total_stall_count', 'flier_allowed',
    'mailbox_allowed', \
    'd2d_allowed', 'flier_lobby_allowed', 'flier_frequency', 'flier_price_day', 'flier_price_confidence'
]

decision = {
    "YES": "yes",
    "NO": "No"
}

poster_inventory_code = 'PO'
standee_inventory_code = 'ST'
flier_inventory_code = 'FL'
stall_inventory_code = 'SL'

# name of inventories as in db
poster = 'POSTER'
standee = 'STANDEE'
stall = 'STALL'
flier = 'FLIER'
car_display = 'CAR DISPLAY'

society = 'RS'
corporate = 'CP'
gym = 'GY'
salon = 'SA'
bus_shelter = 'BS'
retail_shop = 'RE'
hording = "HO"


inventory_name_to_code = {
    poster: poster_inventory_code,
    standee: standee_inventory_code,
    stall: stall_inventory_code,
    flier: flier_inventory_code,
    car_display: car_display_inventory_code
}

# add new supplier type and corresponding class here

# suppliers = {'RS': v0.models.SupplierTypeSociety, 'CP': v0.models.SupplierTypeCorporate,
#              'GY': v0.models.SupplierTypeGym,
#              'SA': v0.models.SupplierTypeSalon}

tower_count_attribute_mapping = {
    'RS': 'tower_count',
    'CP': 'building_count',
    'GY': 'mirrorstrip_count',
    'SA': 'none',
    'RE': 'average_weekday',
    'BS': 'halt_buses_count',
    'HO': 'tower_count'
}

# codes to model names
codes_to_model_names = {
    'RS': 'SupplierTypeSociety',
    'CP': 'SupplierTypeCorporate',
    'GY': 'SupplierTypeGym',
    'SA': 'SupplierTypeSalon',
    'BS': 'SupplierTypeBusShelter',
    'EI': 'SupplierEducationalInstitute',
    'HO': 'SupplierHording',
    'BU': 'SupplierBus',
    'GN': 'SupplierGantry',
    'RC': 'SupplierRadioChannel',
    'TV': 'SupplierTvChannel',
    'WI': 'WhatsAppIndividualInventory',
    'WG': 'WhatsAppGroupInventory',
  
    bus_depot_code: 'SupplierTypeBusDepot',
    retail_shop: 'SupplierTypeRetailShop',
    stall: 'StallInventory',
    standee: 'StandeeInventory',
    flier: 'FlyerInventory',
    poster: 'PosterInventory',
    car_display: 'StallInventory',
    stall_inventory_code: 'StallInventory',
    standee_inventory_code: 'StandeeInventory',
    flier_inventory_code: 'FlyerInventory',
    poster_inventory_code: 'PosterInventory',
    car_display_inventory_code: 'StallInventory',
    'GA': 'GatewayArchInventory',
    'gateway arch' : 'GatewayArchInventory',
    'GATEWAY ARCH' : 'GatewayArchInventory',
    'SUNBOARD': 'SunBoardInventory',
    'SB': 'SunBoardInventory',
    'BA': 'BannerInventory',
    'BANNER': 'BannerInventory',
    'POSTER LIFT': 'PosterLiftInventory',
    'HOARDING' : 'HordingInventory',
    'Hoarding' : 'HordingInventory',
    'GANTRY' : 'GantryInventory',
    'Gantry' : 'GantryInventory',
    'BUS SHELTER' : 'BusShelterInventory',
    'BUS BACK' : 'BusBackInventory',
    'BUS RIGHT' : 'BusRightInventory',
    'BUS LEFT' : 'BusLeftInventory',
    'BUS WRAP' : 'BusWrapInventory',
    'FLOOR' : 'FloorInventory',
    'CEILING' : 'CeilingInventory',
    'BILLING' : 'BillingInventory',
    'COUNTER DISPLAY' : 'CounterDisplayInventory',
    'TENT CARD' : 'TentCardInventory',
    'TABLE' : 'TableInventory',
    'HOARDING LIT' : 'HordingLitInventory',
    'BUS SHELTER LIT' : 'BusShelterLitInventory',
    'GANTRY LIT' : 'GantryLitInventory',
    'WALL' : 'WallInventory',
    'WHATSAPP INDIVIDUAL': 'WhatsAppIndividualInventory',
    'WHATSAPP GROUP': 'WhatsAppGroupInventory'
}

supplier_code_to_names = {
    'RS': 'Residential',
    'RE': 'Retail Shop',
    'CP': 'Corporate Park',
    'BS': 'Bus Shelter',
    'SA': 'Salon',
    'GY': 'Gym',
    'EI': 'Educational Institute',
    'HO': 'Hording',
    'GN': 'Gantry',
    'BU': 'Bus',
    'RC': 'Radio Channel',
    'TV': 'TV Channel',
}

# model to codes
model_to_codes = {
    'SupplierTypeSociety': 'RS',
    'SupplierTypeCorporate': 'CP',
    'SupplierTypeGym': 'GY',
    'SupplierTypeSalon': 'SA',
    'SupplierTypeBusShelter': 'BS',
    'SupplierTypeRetailShop': retail_shop,
    'SupplierEducationalInstitute':'EI',
    'SupplierHording' : 'HO',
    'StallInventory': 'SL',
    'StandeeInventory': 'ST',
    'FlyerInventory': 'FL',
    'PO': 'PosterInventory',
    'ST': 'StandeeInventory',
    'SL': 'StallInventory',
    'FL': 'FlyerInventory',
    'GA': 'GatewayArchInventory',
    'PosterInventory': 'PO',
    'SupplierTypeBusDepot': bus_depot_code,
    'SB': 'SunBoardInventory',
    'BA': 'BannerInventory'
}

# default state and state codes. used to fetch state object in various import api's.

state_name = 'Maharashtra'
state_code = 'MH'

# supplier type names
society_name = 'Society'
corporate_name = 'corporate'


# valid city codes as in the db
mumbai_code = 'MUM'

# basic supplier codes
society_code = 'RS'
corporate_code = 'CP'

# basic permission types
permission_type_create = 'create'
permission_type_read = 'read'
permission_type_update = 'update'
permission_type_delete = 'delete'


api_error_mail_to = 'kshitij.mittal01@gmail.com'
# default prices
default_actual_supplier_price = 0
default_suggested_supplier_price = 0

valid_regions = {
    'CITY': 'City',
    'AREA': 'Area',
    'SUBAREA': 'Subarea'
}

supplier_id_max_length = 20

# the values must match with fields of ObjectLevelPermission model
permission_contants = {
    'CREATE': 'create',
    'UPDATE': 'update',
    'VIEW': 'view',
    'VIEW_ALL': 'view_all',
    'UPDATE_ALL': 'update_all',
    'DELETE': 'delete'
}

#category list
category = {
    'business' : 'BUSINESS',
    'business_agency' : 'BUSINESS_AGENCY',
    'supplier_agency' : 'SUPPLIER_AGENCY',
    'machadalo' : 'MACHADALO',
}
query_status = {
    'supplier_code' : 'supplier_code',
    'booking_status': 'booking_status',
    'phase' : 'phase'
}
exported_file_name_default = 'direct_ptoc_no_file'

campaign_status = {
    'ongoing_campaigns' : 'ongoing',
    'completed_campaigns' : 'completed',
    'upcoming_campaigns' : 'upcoming'
}

society_payment_headers = {
    'Index' : True,
    'Society Id' : True,
    'Name For Payment' : True,
    'IFSC Code' : True,
    'Bank Name' : True,
    'Account Number' : True
}
business_category_campaign_query = {
    'campaign' : 'campaign__account__organisation'
}
bus_agency_campaign_query = {
    'campaign' : 'campaign__user'
}
sup_agency_campaign_query = {
    'campaign' : 'assigned_to'
}
category_query_status = {
    'campaign_query' : 'campaign'
}

perf_metrics_types = {
    'inv_type' : 'inv',
    'lead_type' : 'lead'
}
perf_metrics_param = {
    'on_time' : 'on_time',
    'on_location' : 'on_location',
    'inv' : 'inv'
}

MACHADALO_ORG_ID = 'MAC1421'

tableHeaderData = {
    'RS' :{
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "flat_count" : "Flat Count",
        "resident_count" : "Resident Count",
        "average_household_points" : "Average Household Points",
        "tower_count" : "Tower Count",
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price" : "Inventory Supplier Price",
        "total_supplier_price" : "Total Supplier Price (Per Flat)",
        "negotiated_price" : "Negotiated Price",
        "cost_per_flat" : "Cost Per Flat",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    },
    'CP' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "employee_count":"Employee Count",
        "visitors_count" : "Visitors Count",
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_employee" : "Cost Per Employee",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    },
    'GY' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "weekend_daily_footfall_count" : "Weekend Daily Footfall Count",
        "weekday_daily_footfall_count" : "Weekday Daily Footfall Count",  
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_weekend_daily_footfall" : "Cost Per Weekend Daily Footfall",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    },
    'SA' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "weekend_daily_footfall_count" : "Weekend Daily Footfall Count",
        "weekday_daily_footfall_count" : "Weekday Daily Footfall Count",  
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_weekend_daily_footfall" : "Cost Per Weekend Daily Footfall",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    },
    'BS' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "footfall_count" : "Footfall Count",
        "traffic_count" :  "Traffic Count",
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_footfall" : "Cost Per Footfall",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    },
    'RE' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "weekend_daily_footfall_count" : "Weekend Daily Footfall Count",
        "weekday_daily_footfall_count" : "Weekday Daily Footfall Count", 
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_weekend_daily_footfall" : "Cost Per Weekend Daily Footfall",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    }, 
    'BD' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "average_weekend_daily_footfall" : "Average Weekend(Daily Footfall)",
        "average_weekday_daily_footfall" : "Average Weekday(Daily Footfall)", 
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_average_daily_footfall" : "Cost Per Average Daily Footfall",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    },
    'EI' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "student_count" : "Student Count",
        "teacher_count" : "Teacher Count",
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_student" : "Cost Per Student",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    },
    'HO' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "eyeball_count" :"Eyeball Count",
        "traffic_count" : "Traffic Count", 
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_eyeball" : "Cost Per Eyeball",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    },
    'ALL' : {
        "srNo" : "Sr No",
        "name" : "Supplier Name",
        "supplier_id" : "Supplier Id",
        "supplier_type" : "Supplier Type",
        "area_subArea" : "Area (Sub Area)",
        "address_landmark" : "Address (Landmark)",
        "relation_ship_data" : "RelationShip Data",
        "unit_primary_count" : "Unit Primary Count",
        "unit_secondary_count" : "Unit Secondary Count", 
        "contacts_details" : "Contacts Details",
        "assign_user" : "Assign User",
        "booking_priority" : "Booking Priority",
        "booking_status_and_sub_status" : "Booking Status and Sub Status",
        "requirement_given" : "Requirement Given",
        "phase" : "Phase",
        "internal_comments" : "Internal Comments",
        "comments" : "Comments",
        "next_action_date" : "Next Action Date",
        "inventory_type" : "Inventory Type",
        "inventory_count" : "Inventory Count",
        "inventory_days" : "Inventory Days",
        "inventory_supplier_price": "Inventory Supplier Price",
        "total_supplier_price": "Total Supplier Price",
        "negotiated_price" : "Negotiated Price",
        "cost_per_unit" : "Cost Per Unit",
        "freebies" : "Freebies",
        "mode_of_payment" : "Mode Of Payment",
        "transaction_cheque_number" : "Transaction/Cheque Number",
        "payment_status" : "Payment Status",
        "permission_box" : "Permission Box",
        "receipt" : "Receipt",
        "lead_performance_summary" : "Lead Performance Summary",
        "completion_status" : "Completion Status",
        "delete_action" : "Delete Action",
        "brand":"Brand"
    }
}

supplier_size_category = {
    "RS":{
        "1-150":{
            "min": 0,
            "max": 150
        },
        "151-400":{
            "min": 151,
            "max": 400
        },
        "401+":{
            "min": 401
        }
    },
    "CP":{
        "1-1000":{
            "min": 1,
            "max": 1000
        },
        "1001-10000":{
            "min": 1001,
            "max": 10000
        },
        "10001+":{
            "min": 10001
        }
    },
    "EI":{
        "1-500":{
            "min": 1,
            "max": 500
        },
        "501-2000":{
            "min": 501,
            "max": 2000
        },
        "2001+":{
            "min": 2001
        }
    },
    "RE":{
        "1-100":{
            "min": 1,
            "max": 100
        },
        "101-1000":{
            "min": 101,
            "max": 1000
        },
        "1001+":{
            "min": 1001
        }
    },
    "GY":{
        "1-50":{
            "min": 1,
            "max": 50
        },
        "51-200":{
            "min": 51,
            "max": 200
        },
        "201+":{
            "min": 201
        }
    },
    "SA":{
        "1-20":{
            "min": 1,
            "max": 20
        },
        "21-50":{
            "min": 21,
            "max": 50
        },
        "51+":{
            "min": 51
        }
    },
    "BS":{
        "1-100":{
            "min": 1,
            "max": 100
        },
        "101-300":{
            "min": 101,
            "max": 300
        },
        "301+":{
            "min":301
        }
    },
    "BUS":{
        "1-30":{
            "min": 1,
            "max": 30
        },
        "31-100":{
            "min": 31,
            "max": 100
        },
        "101+":{
            "min":101
        }
    },
    "Hording":{
        "1-10000":{
            "min": 1,
            "max": 10000
        },
        "10001-50000":{
            "min": 10001,
            "max": 50000
        },
        "50001+":{
            "min":50001
        }
    },
    "Gantry":{
        "1-10000":{
            "min": 1,
            "max": 10000
        },
        "10001-50000":{
            "min": 10001,
            "max": 50000
        },
        "50001+":{
            "min":50001
        }
    },
    
}

summary_header = {
    'B to C' :{
        "phase_details" : "Phase Details",
        "confirmed_booked" : "Confirmed Booked",
        "verbally_booked" : "Verbally Booked",
        "followup_required" : "Followup Required",
        "total" : "Total",     
    },
    'B to B' :{
        "phase_details" : "Phase Details",
        'meeting_fixed' : 'Meeting fixed',
        'meeting_converted' : 'Meeting converted',
        'decision_pending' : 'Decision Pending',
        "total" : "Total",
    },
    'Others' :{
        "phase_details" : "Phase Details",
        'emergency_situation' : 'Emergency Situation',
        'complete_lockdown' : 'Complete Lockdown',
        'partial_building_lockdown' : 'Partial Building/Tower Lockdown',
        'partial_floor_lockdown' : 'Partial Floor Lockdown',
        'partial_house_lockdown' : 'Partial House/Flat Lockdown',
        'open' : 'OPEN',
        "total" : "Total",  
    }
}

breakup_header = {
    'B to C' :{
        "confirmed_booked" : "Confirmed Booked",
        "not_initiated" : "Not Initiated",
        "followup_required" : "Followup Required",
        "verbally_booked" : "Verbally Booked",
        "rejected" : "Rejected",
        "total" : "Total",     
    },
    'B to B' :{
        'meeting_fixed' : 'Meeting fixed',
        "not_initiated" : "Not Initiated",
        'meeting_converted' : 'Meeting converted',
        'decision_pending' : 'Decision Pending',
        'rejected' : 'Rejected',
        "total" : "Total",
    },
    'Others' :{
        'emergency_situation' : 'Emergency Situation',
        'complete_lockdown' : 'Complete Lockdown',
        'partial_building_lockdown' : 'Partial Building/Tower Lockdown',
        'partial_floor_lockdown' : 'Partial Floor Lockdown',
        'partial_house_lockdown' : 'Partial House/Flat Lockdown',
        'open' : 'OPEN',
        "total" : "Total",  
    }
}

supplier_master_diff_table = {
    'RS': {
        'supplier_name': 'society_name',
        'supplier_type': 'supplier_code',
        'unit_primary_count': 'flat_count',
        'unit_secondary_count': 'tower_count',
        'area': 'society_locality',
        'subarea': 'society_subarea',
        'city': 'society_city',
        'state': 'society_state',
        'landmark': 'landmark',
        'zipcode': 'society_zip',
        'latitude': 'society_latitude',
        'longitude': 'society_longitude',
        'feedback': 'feedback',
        'quality_rating': 'society_type_quality',
        'quantity_rating': 'society_type_quantity',
        'address1': 'society_address1'
    },
    'CP': {
        'supplier_name': 'name',
        'supplier_type': 'supplier_code',
    },
    'GY': {
        'supplier_name': 'name',
        'supplier_type': 'supplier_code',
        'quality_rating': 'category'
    },
    'SA': {
        'supplier_name': 'name',
        'supplier_type': 'supplier_code',
        'quality_rating': 'category'
    },
    'BS': {
        'supplier_name': 'name',
        'supplier_type': 'supplier_code'
    },
    'RE': {
        'supplier_name': 'name',
        'supplier_type': 'supplier_code',
        'quality_rating': 'rating',
        'quantity_rating': 'store_size'
    },
    'EI': {
        'supplier_name': 'name',
        'supplier_type': 'supplier_code'
    },
    'HO': {
        'supplier_name': 'name',
        'supplier_type': 'supplier_code'
    },
}