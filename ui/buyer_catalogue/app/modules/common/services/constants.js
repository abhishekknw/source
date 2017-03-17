angular
  .module('catalogueApp').
  constant('errorHandler',{
    name : '',
    success : 'success',
    error : 'error',
    warning : 'warning',
    server_connection_error : 'Server is down, Please Try again',
    //createproposal
    geo_location_error : 'Address or Pincode Incorrect, Please Provide Correct Information',
    //mapview
    save_success : 'Saved successfully',
    save_error : 'Some error occured, Data not saved',
    importfile_error : 'Please select correct file',
    uploadfile_success : 'File Uploaded successfully',
    uploadfile_error  : 'Error occured, Please check your internet connection and Try again',
    request_proposal_success : 'Request for proposal is sent, Machadalo team will contact you soon',
    request_proposal_error : 'Error occured, Please check your internet connection and Try again',
    save_proposal_success : 'Your proposal is saved successfully',
    supplier_status_error : 'Sorry, There is some error in saving supplier status',
    //auditReleasePlan
    positive_number_error : 'Enter Positive Number Only',
    //opsDashboard
    onhold_success : 'BD team has been notified',
    onhold_error : 'Error occured, Please check your internet connection',
    assign_user_success : 'The Proposal is converted to campaign and assigned to user',
    assign_user_error : 'Some error occured in asigning proposal to user',
    accept_proposal_error : 'Error occured while converting proposal to campaign',
    decline_proposal_error : 'Error occured while declining campaign, Please ensure that you are declining campaign which is not on hold',
    //releaseplan
    updateData_success : 'Data updated successfully',
    updateData_error : 'Error occured while saving data',
    //auditReleasePlan
    inventory_date_success : 'Inventory Dates are saved successfully',
    inventory_date_error : 'Error occured while saving dates',
    //currentProposal or proposal summary
    invoice_confirm : 'Do You really want to confirm Invoice Details?',
    invoice_success : 'Your Invoice details are saved successfully',
    invoice_error : 'Error occured, Invoice details are not saved',
    //opsExecution
    reAssign_success : 'Reassign is Successful',
    reAssign_error : 'Error occured while reassigning, Please Try again',
    //createAccount
    account_success : 'Account Details saved successfully',
    account_error : 'Error occured in saving account details',
    //CreateCampaign
    business_success : 'Business Details saved successfully',
    business_error : 'Error occured in saving business details',


  });
