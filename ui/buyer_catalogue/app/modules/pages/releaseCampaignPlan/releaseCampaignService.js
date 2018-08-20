 'use strict';
 angular.module('catalogueApp')
 .factory('releaseCampaignService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

    var url_base = 'v0/ui/website/';
    var url_base_ui = 'v0/ui/';
    var releaseCampaignService = {};


    releaseCampaignService.getCampaignReleaseDetails = function(proposal_id){
         var url = url_base + proposal_id + "/campaign-inventories/";
    	return machadaloHttp.get(url);
    }

    releaseCampaignService.updateAuditReleasePlanDetails = function(proposal_id,data){
         var url = url_base + proposal_id + "/campaign-inventories/";
      return machadaloHttp.put(url,data);
    }

    releaseCampaignService.addSuppliersToCampaign = function(data){
      var url = url_base + 'add-suppliers-direct-to-campaign/';
      return machadaloHttp.post(url,data);
    }

    releaseCampaignService.getRelationShipData = function(supplierId,supplierCode,campaignId){
      var url = url_base + "get-relationship-and-past-campaigns-data/?supplier_id=" + supplierId + "&supplier_code=" + supplierCode
                + "&campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }

    releaseCampaignService.savePaymentDetails = function(data,supplierId){
      var url = url_base_ui + 'society/';
      return machadaloHttp.post(url,data);
    }

    return releaseCampaignService;
}]);
