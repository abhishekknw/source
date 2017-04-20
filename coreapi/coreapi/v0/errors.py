# this file lists down all types of messages to be used in the code.

# this error occur while importing a file and length of header row does not match the predefined header we have
LENGTH_MISMATCH_ERROR = 'Length of row read {0}, does not match with length of keys {1} defined in constants'
CAMPAIGN_INVALID_STATE_ERROR = 'This proposal is not a campaign yet because it\'s state {0} is not set to {1})'
CAMPAIGN_ON_HOLD_ERROR = 'This proposal is not a campaign yet because it is on hold'
CAMPAIGN_NOT_APPROVED_ERROR = 'This proposal is not a campaign yet because it has not been approved by ops HEAD'
CAMPAIGN_NO_INVOICE_ERROR = 'This proposal is not a campaign because it does not have any invoice number'
CAMPAIGN_NO_START_OR_END_DATE_ERROR = 'This proposal {0} is not a campaign because it does not have either start or end date defined'
ALREADY_A_CAMPAIGN_ERROR = 'This proposal {0}  has already been converted to campaign'

INVALID_PAYMENT_METHOD_CODE = 'This code {0} is not a valid payment method code'
INVALID_PAYMENT_STATUS_CODE = 'This code {0} is not a valid payment status code'
INVALID_BOOKING_STATUS_CODE =  'This code {0} is not a valid booking status code'

INVALID_START_END_DATE = 'The start {0} and end date {0} are wrong. The end date cannot be less than start date'
NO_DATES_ERROR = 'This proposal {0} does not have any start and end date. Please fill the dates'
DATES_OVERLAP_ERROR = 'The inventory with id {0} current dates {1} and {2} overlap with already booked dates {3} and {4} under campaign id {5}.  Hence this inventory is not booked under the current proposal'

CANNOT_CONVERT_TO_CAMPAIGN_ERROR = 'The proposal {0} cannot be converted into campaign because {1}'

# Message codes on success
PROPOSAL_CONVERTED_TO_CAMPAIGN = 'This proposal {0} is converted to campaign successfully'
REVERT_CAMPAIGN_TO_PROPOSAL = 'The campaign {0} inventories are released and state changed to {1}'
NO_INVENTORIES_ASSIGNED_ERROR = 'The current proposal {0} has not been assigned any inventories'

# object does not exist error
OBJECT_DOES_NOT_EXIST_ERROR = 'The object for table {0} does not exist for id {1}'
INVALID_ACTIVITY_TYPE_ERROR = 'This activity type {0} is not recognised by our system'
ZERO_AUDITS_ERROR = 'The inventory  {0}  with id {1} has zero audits assigned to it. You cannot audit this inventory.'
NUMBER_OF_ACTIVITY_EXCEEDED_ERROR = 'Number of possible {0} s for this inventory was {1}. You have already done that many {0} s'

INVALID_AMENITY_CODE_ERROR = 'The amenity code {0} is invalid'

SUPPLIER_CITY_NO_CREATE_PERMISSION_ERROR = 'Sorry. You do not have sufficient permissions to create supplier of type {0} for city with code {1}'

NO_INVENTORIES_PRESENT_MESSAGE = 'There are really no inventories available'

NO_INVENTORY_ACTIVITY_ASSIGNMENT_ERROR = 'There are no inventory activities assigned, hence you cannot proceed further in our system. You must be assigned inventory activities first in order to proceed further'

INVALID_DATE_FORMAT = "The recieved format of the date string does not matches the current supported format of {0} and {1}"

ALL_IMAGES_SYNCED_UP_MESSAGE = "Seems like all the images synced up already"

NO_TOWER_ASSIGNED_ERROR = "There is no tower assigned to this inventory {0} with id {1}"
NO_IMAGES_FOR_THIS_PROPOSAL_MESSAGE = "There are no images in our system for this proposal {0}"
TASK_NOT_DONE_YET_ERROR = "This task with id {0} is not successfull yet"
PATH_DOES_NOT_EXIST = "This path {0} doesnt not exist"

NO_GEOCODE_INSTANCE_FOUND = 'We did not get a geo code instance for this address {0}'
INCORRECT_DATABASE_NAME_ERROR = 'The database name in settings file \'{0}\' does not matches the custom defined database name \'{1}\' '

UPLOAD_AMAZON_SUCCESS = 'Upload to amazon successfull'

DELETION_NOT_PERMITTED = 'The deletion of file with extension {0} is not permitted'

GROUP_DOES_NOT_EXIST = 'The group with name {0} does not exist in the database'

HEADER_NOT_PRESENT_IN_SHEET = 'The header with name {0} not present in sheet header list. lookup key is {1}'

COUNT_SIZE_RENT_VALUE_NOT_PRESENT = 'One or more of following values {0}, {1}, {2} is not provided for this supplier {3}'
