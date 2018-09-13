'use strict';


 angular.module('catalogueApp')
 .factory('DashboardService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';
    var url_base_proposal = 'v0/ui/proposal/'
    var DashboardService = {};



    DashboardService.getCampaigns = function(campaignId, category, date){
        var url = url_base + "campaign-list/" + campaignId + "/?category=" + category + "&date=" +date ;
        return machadaloHttp.get(url);
    }

    DashboardService.getCampaignDetails = function(campaignId,query){
      var url = url_base + "dashboard/suppliers_booking_status/?campaign_id=" + campaignId +"&query=" + query;
      return machadaloHttp.get(url);
    }


    DashboardService.getAllCampaignsData = function(organisationId,category){
      var url = url_base + "campaigns-assigned-inventory-counts/" + organisationId + "/?category=" + category;
      return machadaloHttp.get(url);
    }

    DashboardService.getAssignedIdsAndImages = function(organisationId,category,type,date,inventory){
      var url = url_base + "campaigns-assigned-inventory-ids-and-images/" + organisationId + "/?category=" + category
              + "&type=" + type + "&date=" + date + "&inventory=" + inventory;
      return machadaloHttp.get(url);
    }

    DashboardService.getCountOfSupplierTypesByCampaignStatus = function(campaignStatus){
      var url = url_base + "dashboard/get_count_of_supplier_types_by_campaign_status/?status=" + campaignStatus;
      return machadaloHttp.get(url);
    }

    DashboardService.getSuppliersOfCampaignWithStatus = function(campaignId){
      var url = url_base + "dashboard/get_suppliers_current_status/?campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }

    DashboardService.getCampaignFilters = function(campaignId){
      var url = url_base + "dashboard/get_campaign_filters/?campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }

    DashboardService.getPerformanceMetricsData = function(campaignId,type,inv,perf_param){
      var url = url_base + "dashboard/get_performance_metrics_data/?campaign_id=" + campaignId + "&type=" + type + "&inv_code=" + inv + "&perf_param="+perf_param;
      return machadaloHttp.get(url);
    }

    DashboardService.getLocationData = function(campaignId,inv){
      var url = url_base + "dashboard/get_location_difference_of_inventory/?campaign_id=" + campaignId + "&inv=" + inv;
      return machadaloHttp.get(url);
    }

    DashboardService.getCampaignInvTypesData = function(campaignId){
      var url = url_base + "dashboard/get_supplier_data_by_campaign/?campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }

    DashboardService.getCampaignInventoryActivitydetails = function(campaignId){
      var url = url_base + "dashboard/get_campaign_inventory_activity_details/?campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }

    DashboardService.getLeadsByCampaign = function(campaignId){
      var url = url_base + "dashboard/get_leads_by_campaign/?campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }

    DashboardService.getLeadsByCampaignNew = function(campaignId){
      var url = url_base + "dashboard/get_leads_by_campaign_new/?campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }

    DashboardService.getCompareCampaignChartData = function(data){
      var url = url_base + "dashboard/proposal_id/get_leads_by_multiple_campaigns/";
      return machadaloHttp.post(url,data);
    }

     DashboardService.getCompareCampaignChartData = function(data){
      var url = url_base + "dashboard/campaign_id/get_leads_by_multiple_campaigns_new/";
      return machadaloHttp.post(url,data);
    }

    DashboardService.getSupplierImages = function(supplierId,invType,activityType){
      var url = url_base + "dashboard/get_activity_images_by_suppliers/?supplier_id=" + supplierId + "&inv_code=" + invType + "&act_type=" + activityType;
      return machadaloHttp.get(url);
    }

    DashboardService.getHashtagImages = function(campaignId){
      var url = url_base + "hashtag_images/?campaign_id=" + campaignId;
      return machadaloHttp.get(url);
    }
    return DashboardService;

 }]);
