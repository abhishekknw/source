'use strict';


 angular.module('catalogueApp')
 .factory('LeadFormService',['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';
    var url_base_ui = 'v0/ui/';

    var LeadFormService = {};

    LeadFormService.getCampaignLeadAliasData = function(campaignId){
      var url = url_base + "lead-alias/?campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }

    LeadFormService.getCampaignInfo = function(campaignId){
      var url = url_base + "proposal/" + campaignId + "/";
      return machadaloHttp.get(url);
    }

    LeadFormService.getSupplierDetails = function(supplierId){
      var url = url_base_ui + "society/" + supplierId;
      return machadaloHttp.get(url);
    }

    LeadFormService.saveLeads = function(data){
      var url = url_base + "leads/";
      return machadaloHttp.post(url,data);
    }

    LeadFormService.updateLeads = function(id,data){
      var url = url_base + "leads/" + id + "/";
      return machadaloHttp.put(url,data);
    }

    LeadFormService.getLeads = function(campaignId , supplierId){
      var url = url_base + "leads/?campaign_id=" + campaignId + "&supplierId=" + supplierId;
      return machadaloHttp.get(url);
    }


    return LeadFormService;
    return campaignLeadsService;

}]);
