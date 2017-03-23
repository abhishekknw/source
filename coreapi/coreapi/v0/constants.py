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
