from constants import price_per_flat


def getList(data, society_keys):
    return [data.get(key, '') for key in society_keys]


def inventoryPricePerFlat(data, inventory_array):
    for arr in inventory_array:
        data[price_per_flat[arr][0]] = (data[price_per_flat[arr][1]]) / (data['flat_count'])
    return data
