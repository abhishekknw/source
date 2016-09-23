

def getList (data, society_keys):
	return [ data.get(key, '') for key in society_keys ]

def inventoryPricePerFlat (data, inventory_array):
	price_per_flat = {
	      'PO' : ['poster_price_per_flat', 'poster_price'],
	      'ST' : ['standee_price_per_flat', 'standee_price']
	}

	for arr in inventory_array:
           header = []
           header = inventorylist[arr]['HEADER']
           data[price_per_flat[arr][0]] =   data[price_per_flat[arr][1]] / data['flat_count']    
   

    return data