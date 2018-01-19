'use strict';


 angular.module('catalogueApp')
 .factory('sheetToCampaignService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  	var url_base_website = 'v0/ui/website/';
    var url_base_supplier = 'v0/ui/';

  	var sheetToCampaignService = {};

    sheetToCampaignService.getSocieties = function(){
      var url = url_base_supplier + "society/list/";
      return machadaloHttp.get(url);
    }

    sheetToCampaignService.getProposalCenters = function(proposalId){
      var url = url_base_website + "proposal-center-mapping/?proposal_id=" + proposalId;
      return machadaloHttp.get(url);
    }

    sheetToCampaignService.convertDirectProposalToCampaign = function(data){
      var url = url_base_website + "convert-direct-proposal-to-campaign/";
      return machadaloHttp.post(url,data);
    }

  	return sheetToCampaignService;
  }]);
