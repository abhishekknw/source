 'use strict';
 angular.module('catalogueApp')
 .factory('releaseCampaignService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

    var url_base = 'v0/ui/website/';
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
    return releaseCampaignService;
}]);
