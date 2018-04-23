'use strict';


 angular.module('catalogueApp')
 .factory('campaignLeadsService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';

    var campaignLeadsService = {};

        campaignLeadsService.create = function(data){
          var url = url_base + "lead-alias/";
          return machadaloHttp.post(url, data);
        }

        campaignLeadsService.getLeads = function(campaignId){
          var url = url_base + "leads/?campaign_id=" + campaignId;
          return machadaloHttp.get(url);
        }

        campaignLeadsService.getCampaignDetails = function(assigned_by,userId,fetch_all){
          var url = url_base + "campaign-assignment/?include_assigned_by="+ assigned_by +  "&to="+userId + "&fetch_all=" + fetch_all;
          return machadaloHttp.get(url);
        }

        campaignLeadsService.getCampaignLeadAliasData = function(campaignId){
          var url = url_base + "lead-alias/?campaign_id=" + campaignId;
          return machadaloHttp.get(url);
        }

        campaignLeadsService.getShortlistedSuppliers = function(campaignId){
            var url = url_base + "proposal/"+ campaignId + "/shortlisted_suppliers/";
        	return machadaloHttp.get(url);
        }

        campaignLeadsService.getAliasData = function(campaignId){
          var url = url_base + "lead-alias/?campaign_id=" + campaignId;
          return machadaloHttp.get(url);
        }

        campaignLeadsService.importLeadsThroughSheet = function(campaignId,data){
          var url = url_base + "leads/" + campaignId + "/import_leads/";
          return machadaloHttp.post(url,data);
        }
        return campaignLeadsService;

 }]);
