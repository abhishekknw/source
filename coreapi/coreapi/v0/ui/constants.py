
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

poster_inventory_code = 'PO'
standee_inventory_code = 'ST'
flier_inventory_code = 'FL'
stall_inventory_code = 'SL'
car_display_inventory_code = 'CD'

# name of inventories as in db
poster = 'POSTER'
standee = 'STANDEE'
stall = 'STALL'
flier = 'FLIER'
car_display = 'CAR DISPLAY'


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
    'GY': 'none',
    'SA': 'none'
}

# codes to model names
codes_to_model_names = {
                'RS': 'SupplierTypeSociety',
                'CP': 'SupplierTypeCorporate',
                'GY': 'SupplierTypeGym',
                'SA': 'SupplierTypeSalon',
                'BS': 'SupplierTypeBusShelter',
                stall: 'StallInventory',
                standee: 'StandeeInventory',
                flier: 'FlyerInventory',
                poster: 'PosterInventory',
                car_display:'StallInventory',
                stall_inventory_code: 'StallInventory',
                standee_inventory_code: 'StandeeInventory',
                flier_inventory_code: 'FlyerInventory',
                poster_inventory_code: 'PosterInventory',
                car_display_inventory_code:  'StallInventory'
         }
# model to codes
model_to_codes = {
    'SupplierTypeSociety': 'RS',
    'SupplierTypeCorporate': 'CP',
    'SupplierTypeGym': 'GY',
    'SupplierTypeSalon': 'SA',
    'SupplierTypeBusShelter': 'BS',
    'StallInventory': 'SL',
    'StandeeInventory': 'ST',
    'FlyerInventory': 'FL',
    'PO': 'PosterInventory',
    'PosterInventory': 'PO'
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


api_error_mail_to = 'nikhil.singh@machadalo.com'
# default prices
default_actual_supplier_price = 0
default_suggested_supplier_price = 0

