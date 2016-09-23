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
 'Center Name', 'Supplier Id', 'Supplier Name', 'Sub Area', 'Society Type', 'Tower Count',\
 'Flat Count'
 ]

inventorylist = {
	'PO' :  { 'HEADER' : [ 'Poster Count', 'Poster Price', 'Poster Duration','Poster Price Factor','Poster price per flat'],
	          'DATA': ['total_poster_count', 'poster_price' , 'poster_duration' , 'poster_price_factor', 'poster_price_per_flat'] 
	}, 
	'ST' :  { 'HEADER': ['Standee Count', 'Standee Price', 'Standee Duration', 'Standee Price factor', 'Standee price per flat'],  
	          'DATA': ['total_standee_count', 'standee_price', 'standee_duration', 'standee_price_factor', 'standee_price_per_flat'] 
	}
}

sample_data = [
'vvhbhb', 'bhbhbh'
]

society_keys = [ 'supplier_id', 'society_name',  'society_subarea', 'society_type_quality',\
'tower_count', 'flat_count' 
]

center_keys = ['center_name']

export_keys = ['center', 'societies', 'societies_inventory', 'societies_inventory_count']

contact_keys = [
    'city', 'area', 'sub_area', 'supplier_type', 'society_name', 'supplier_code', 'contact_type', 'salutation', \
    'name', 'landline', 'mobile', 'email'
]

STD_CODE = '022'
COUNTRY_CODE = '+91'

