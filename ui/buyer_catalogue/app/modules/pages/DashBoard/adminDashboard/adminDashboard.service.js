'use strict';


 angular.module('catalogueApp')
 .factory('adminDashboardService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';

    var adminDashboardService = {};



    adminDashboardService.getCampaigns = function(campaignId, category, date){
        var url = url_base + "campaign-list/" + campaignId + "/?category=" + category + "&date=" +date ;
        return machadaloHttp.get(url);
    }

    adminDashboardService.getCampaignDetails = function(campaignId,query){
      var url = url_base + "dashboard/suppliers_booking_status/?campaign_id=" + campaignId +"&query=" + query;
      return machadaloHttp.get(url);
    }


    adminDashboardService.getAllCampaignsData = function(organisationId,category){
      var url = url_base + "campaigns-assigned-inventory-counts/" + organisationId + "/?category=" + category;
      return machadaloHttp.get(url);
    }

    adminDashboardService.getAssignedIdsAndImages = function(organisationId,category,type,date,inventory){
      var url = url_base + "campaigns-assigned-inventory-ids-and-images/" + organisationId + "/?category=" + category
              + "&type=" + type + "&date=" + date + "&inventory=" + inventory;
      return machadaloHttp.get(url);
    }

    return adminDashboardService;

 }]);
