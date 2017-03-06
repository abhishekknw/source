angular
  .module('catalogueApp').
  constant('errorHandler',{
    name : 'Machadalo',
    success : 'success',
    error : 'error',
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


  });
