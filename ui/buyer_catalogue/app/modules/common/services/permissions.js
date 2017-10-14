angular
  .module('catalogueApp').
  constant('permissions',{
    //homepage
    homePage : {
      organisationsListView   : 'can_view_organisation_list',
      organisationDetailsView : 'can_view_organisation_details',
      accountListView         : 'can_view_account_list',
      addNewAccount           : 'can_add_new_account',
      createNewProposal       : 'can_create_new_propsoal',
      proposalListView        : 'can_view_proposal_list',
    },

    pagePermissions : {
      homepage        : 'homepage',
      proposalSummary : 'proposal_summary_page',
      mapView         : 'mapview',
    },

    urlList : {
      '/manageCampaign/create' : 'homepage',
    }
  });
