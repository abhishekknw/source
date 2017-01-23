# this file lists down all types of messages to be used in the code.

# this error occur while importing a file and length of header row does not match the predefined header we have
LENGTH_MISMATCH_ERROR = 'Length of row read {0}, does not match with length of keys {1} defined in constants'
CAMPAIGN_INVALID_STATE_ERROR = 'This proposal is not a campaign yet because it\'s state {0} is not set to {1})'
CAMPAIGN_ON_HOLD_ERROR = 'This proposal is not a campaign yet because it is on hold'
CAMPAIGN_NOT_APPROVED_ERROR = 'This proposal is not a campaign yet because it has not been approved by ops HEAD'
CAMPAIGN_NO_INVOICE_ERROR = 'This proposal is not a campaign because it does not have any invoice number'

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

