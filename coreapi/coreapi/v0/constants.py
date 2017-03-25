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
valid_amenities = {
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