
keys = [
    'city', 'city_code',  'area', 'area_code', 'subarea', 'subarea_code',  'supplier_type', 'supplier_name', 'supplier_code', \
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

decision = {

    "YES": "yes",
    "NO": "No"
}

# add new supplier type and corresponding class here

# suppliers = {'RS': v0.models.SupplierTypeSociety, 'CP': v0.models.SupplierTypeCorporate,
#              'GY': v0.models.SupplierTypeGym,
#              'SA': v0.models.SupplierTypeSalon}

tower_count_attribute_mapping = {

    'RS': 'tower_count',
    'CP': 'building_count',
    'GY': 'none',
    'SA': 'none'
}

# codes to model names
codes_to_model_names = {

                'RS': 'SupplierTypeSociety', 'CP': 'SupplierTypeCorporate','GY': 'SupplierTypeGym',
                'SA': 'SupplierTypeSalon', 'BS': 'SupplierTypeBusShelter', 'STALL': 'StallInventory',
                'STANDEE': 'StandeeInventory'
         }
# model to codes
model_to_codes = {
    'SupplierTypeSociety': 'RS', 'SupplierTypeCorporate': 'CP', 'SupplierTypeGym': 'GY', 'SupplierTypeSalon': 'SA', 'SupplierTypeBusShelter': 'BS',
    'StallInventory': 'SL', 'StandeeInventory': 'ST'
}

# default state and state codes. used to fetch state object in various import api's.
state_name = 'Uttar Pradesh'
state_code = 'UP'

# supplier type names
society_name = 'Society'
