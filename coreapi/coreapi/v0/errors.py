# this file lists down all types of error messages to be used in the code.

# this error occur while importing a file and length of header row does not match the predefined header we have
LENGTH_MISMATCH_ERROR = 'Length of row read {0}, does not match with length of keys {1} defined in constants'
CAMPAIGN_INVALID_STATE_ERROR = 'This proposal is not a campaign yet because it\'s state {0} is not set to {1})'
CAMPAIGN_ON_HOLD_ERROR = 'This proposal is not a campaign yet because it is on hold'
CAMPAIGN_NOT_APPROVED_ERROR = 'This proposal is not a campaign yet because it has not been approved by ops HEAD'
CAMPAIGN_NO_INVOICE_ERROR = 'This proposal is not a campaign because it does not have any invoice number'

INVALID_PAYMENT_METHOD_CODE = 'This code {0} is not a valid payment method code'
INVALID_PAYMENT_STATUS_CODE = 'This code {0} is not a valid payment status code'