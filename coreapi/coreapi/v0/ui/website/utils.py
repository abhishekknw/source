from constants import society_keys

def getList (data):
	return [ data[key] for key in society_keys ]
