angular
  .module('catalogueApp').
  constant('permissions',{
    //homepage
    homePage : {
      organisationsListView   : 'can_view_organisation_list',
      organisationDetailsView : 'can_view_organisation_details',
      accountListView         : 'can_view_account_list',
      addNewAccount           : 'can_add_new_account',
      createNewProposal       : 'can_create_new_proposal',
      proposalListView        : 'can_view_proposal_list',
    },

    proposalSummaryPage : {
      addInvoiceDetails   :  'can_add_invoice_details',
    },

    mapviewPage : {
      changeRadius        :   'can_change_radius_on_mapview',
      changeCenter        :   'can_change_center_location_on_mapview',
      viewFilters         :   'can_view_filters_on_mapview_and_gridview',
      applyFilters        :   'can_apply_filters_on_mapview_and_gridview',
      saveData            :   'can_save_data_on_mapview_and_gridview',
      addSuppliers        :   'can_add_extra_suppliers_on_gridview',
      requestProposal     :   'can_request_proposal_on_gridview',
      uploadProposal      :   'can_upload_proposal_on_gridview',
      finalizeStatus      :   'can_change_supplier_status_to_finalize_on_gridview',
      bufferStatus        :   'can_change_supplier_status_to_buffer_on_gridview',
      removeStatus        :   'can_change_supplier_status_to_remove_on_gridview',
    },

    opsDashBoard : {
      acceptProposal      :   'can_change_proposal_state_to_accept_on_opsdashboard',
      declineProposal     :   'can_change_proposal_state_to_decline_on_opsdashboard',
      onHoldPrposal       :   'can_change_proposal_state_to_onhold_on_opsdashboard',
    },

    supplierBookingPage : {
      addNegotiatedPrice  :   'can_add_negotiated_price_on_supplierBookingPage',
      viewNegotiatedPrice :   'can_view_negotiated_price_on_supplierBookingPage',
      viewBookingStatus   :   'can_view_booking_status_of_supplier_on_supplierBookingPage',
      changeBookingStatus :   'can_change_booking_status_of_supplier_on_supplierBookingPage',
      viewPhase           :   'can_view_phase_of_supplier_on_supplierBookingPage',
      addPhase            :   'can_add_phase_of_supplier_on_supplierBookingPage',
      viewPaymentMode     :   'can_view_mode_of_payment_of_supplier_on_supplierBookingPage',
      addPaymentMode      :   'can_add_mode_of_payment_of_supplier_on_supplierBookingPage',
      viewPaymentDetails  :   'can_view_payment_details_of_supplier_on_supplierBookingPage',
      viewInventoryIds    :   'can_view_inventory_ids_of_supplier_on_supplierBookingPage',
      updateData          :   'can_update_data_on_supplierBookingPage',
    },

    auditReleasePage : {
      assignDates         :   'can_assign_dates_of_campaign_of_all_activities_on_ManageAuditDetailsPage',
      viewDates           :   'can_view_dates_of_activities_on_ManageAuditDetailsPage',
      addComments         :   'can_add_comments_for_activities_on_ManageAuditDetailsPage',
      updateData          :   'can_update_data_on_ManageAuditDetailsPage',
    },

    opsExecutionPage : {
      reAssignDates       :   'can_ReAssign_activity_dates_on_OpsExecutionPage',
      viewSupplierDetails :   'can_view_supplier_details_on_OpsExecutionPage',
      viewImages          :   'can_view_images_on_OpsExecutionPage',
      uploadImages        :   'can_upload_images_on_OpsExecutionPage',
      viewSummary         :   'can_view_summary_details_on_OpsExecutionPage',
      downloadImages      :   'can_download_images_on_OpsExecutionPage',
    },

    navBar : {
      viewManagement      :   'can_view_Management_on_NavBar',
      menuHome            :   'can_view_HomePage_Button_on_Menu',
      menuOpsDashBoard    :   'can_view_OpsDashBoard_Button_on_Menu',
      menuCampaignList    :   'can_view_CampaignList_Button_on_Menu',
    },

    pagePermissions : {
      homepage                : 'homePage',
      proposalSummaryPage     : 'proposalSummaryPage',
      mapViewPage             : 'mapViewPage',
      createProposalPage      : 'createProposalPage',
      showCurrentProposalPage : 'showCurrentProposalPage',
      managementPage          : 'managementPage',
      opsDashBoardPage        : 'opsDashBoardPage',
      CampaignListPage        : 'CampaignListPage',
      supplierBookingPage     : 'supplierBookingPage',
      auditReleasePage        : 'auditReleasePage',
      opsExecutionPage        : 'opsExecutionPage',
      showProposalHistoryPage : 'showProposalHistoryPage',
      publicPage              :  'publicPage',
    },
  });
