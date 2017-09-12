angular
  .module('catalogueApp').
  constant('constants',{
    //amazon keys
    // base_url : 'http://coreapi-test.3j6wudg4pu.ap-southeast-1.elasticbeanstalk.com/',
    base_url : 'http://localhost:8000/',
    url_base : 'v0/ui/website/',
    AWSAccessKeyId : 'AKIAI6PVCXJEAXV6UHUQ',
    policy : "eyJleHBpcmF0aW9uIjogIjIwMjAtMDEtMDFUMDA6MDA6MDBaIiwKICAiY29uZGl0aW9ucyI6IFsgCiAgICB7ImJ1Y2tldCI6ICJtZGltYWdlcyJ9LCAKICAgIFsic3RhcnRzLXdpdGgiLCAiJGtleSIsICIiXSwKICAgIHsiYWNsIjogInB1YmxpYy1yZWFkIn0sCiAgICBbInN0YXJ0cy13aXRoIiwgIiRDb250ZW50LVR5cGUiLCAiIl0sCiAgICBbImNvbnRlbnQtbGVuZ3RoLXJhbmdlIiwgMCwgNTI0Mjg4MDAwXQogIF0KfQoK",
    acl : 'public-read',
    signature : "GsF32EZ1IFvr2ZDH3ww+tGzFvmw=",
    content_type : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    //amazon server
    aws_bucket_url : 'http://mdimages.s3.amazonaws.com/',
    //general
    name : '',
    success : 'success',
    error : 'error',
    warning : 'warning',
    errorMsg : 'Error Occured',
    server_connection_error : 'Server is down, Please Try again',
    emptyResponse : 'No results Found',
    btn_success : 'btn-success',
    warn_user_msg : 'Are You Sure?',
    save_success : 'Saved successfully',
    save_error : 'Some error occured, Data not saved',
    shortlisted : 'Shortlisted',
    removed : 'Removed',
    buffered : 'Buffered',
    finalized: 'Finalized',
    statusCode_shortlisted : 'S',
    statusCode_buffered : 'B',
    statusCode_removed : 'R',
    statusCodeFinalized: 'F',
    showSystemError: true,

    //createproposal
    geo_location_error : 'Address or Pincode Incorrect, Please Provide Correct Information',
    center_warning : 'Do you want to create only one center ?',
    //mapview
    importfile_error : 'Please select correct file',
    save_success : 'Saved successfully',
    save_error : 'Some error occured, Data not saved',
    importfile_error : 'Some error occurred while importing file.',
    uploadfile_success : 'File Uploaded successfully',
    uploadfile_error  : 'Error occured, Please check your internet connection and Try again',
    request_proposal_success : 'Request for proposal is sent, Machadalo team will contact you soon',
    request_proposal_error : 'Error occured, Please check your internet connection or Valid Email Id is not provided',
    save_proposal_success : 'Your proposal is saved successfully',
    supplier_status_error : 'Sorry, There is some error in saving supplier status',
    amenity_error : 'Error in getting Amenities',
    client_email_error : 'Error occured while sending Email to Client',
    bdhead_email_error : 'Error occured while sending Email to BDHead',
    upload_error : 'error occured while uploading file',
    deletefile_error : 'Error occured, File not deleted',
    finalize : 'F',
    buffer : 'B',
    remove : 'R',
    supplierCode_all : 'All',
    RS:'Society',
    CP:'Corporate',
    BS:'Bus Shelter',
    GY:'Gym',
    SA:'Saloon',
    RE:'Retail Store',
    All:'All',

    //auditReleasePlan
    positive_number_error : 'Enter Positive Number Only',
    //opsDashboard
    onhold_success : 'BD team has been notified',
    onhold_error : 'Error occured, Please check your internet connection',
    assign_user_success : 'The Proposal is converted to campaign and assigned to user',
    assign_user_error : 'Some error occured in asigning proposal to user',
    accept_proposal_error : 'Error occured while converting proposal to campaign',
    decline_proposal_error : 'Error occured while declining campaign, Please ensure that you are declining campaign which is not on hold',
    emptyProposalMsg : 'No Proposals Found',
    email_error : 'Error while sending Email, Try Again',
    sleepTime : '3000',
    //campaignList
    emptyCampaignList : 'No Campaigns Found',
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
    images_download_error : 'Download Failed, Retry later',
    no_image_error : 'There are no images available to download',
    upload_image_activity_url : 'upload-inventory-activity-image-amazon/',
    //createAccount
    account_success : 'Account Details saved successfully',
    account_error : 'Error occured in saving account details',
    //CreateCampaign
    business_success : 'Business Details saved successfully',
    business_error : 'Error occured in saving business details',
    campaign_manager : 'campaign_manager',
    proposalMaking : 'PM',
    proposalRequested : 'PR',
    proposalFinalized : 'PF',
    proposalConverted : 'PTC',
    proposalOnHold : 'POH',
    proposalDeclined : 'PNC',
    PTC : 'Converted',
    PR : 'Requested',
    PF : 'Finalized',
    POH : 'On-Hold',
    PNC : 'Declined',
    //manage user
    createUser_success : 'Successfully Created',
    create_group_success : 'Group Created Successfully',
    create_group_error : 'Error Occured in creating group',
    password_error : 'Must match to password',
    delete_confirm_user : 'Do you really want to delete this user?',
    delete_confirm : 'Yes! Delete it!',
    delete_confirm_group : 'Do you really want to delete this Group?',
    changePassword_success : 'Password changed Successfully',

    //guestPage
    location_error : 'Please enter accurate location',

    //permissions
    bd_manager : 'BD Manager',
    campaign_manager : 'Campaign Manager',

    //errorMsg
    show_system : true,
    show_general : true,

  });
