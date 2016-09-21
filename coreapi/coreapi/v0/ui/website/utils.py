from constants import data_keys

def getList (data):
	return [ data[key] for key in data_keys ]

