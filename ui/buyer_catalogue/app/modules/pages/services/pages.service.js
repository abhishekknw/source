'use strict';

/**
 * @ngdoc service
 * @name mdopsApp.societyDetailsService
 * @description
 * # societyDetailsService
 * Service in the mdopsApp.
 */

angular.module('machadaloPages').factory('pagesService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {


   var url_base = "v0/ui/website/";
   var pagesService = {};

   // To return the archived estimates
   pagesService.listSocieties = function (sObj) {
     var url = url_base + "society/list/";
     if(sObj && sObj != "")
      url += "?search="+sObj
     return machadaloHttp.get(url);
   };

    pagesService.getAllBusinesses = function () {
      var url = url_base + "businesses/";
      return machadaloHttp.get(url);
   };


   pagesService.getBusiness = function (id) {
       var url = url_base + "business/" + id;
       return machadaloHttp.get(url);
      };

    pagesService.createBusinessCampaign = function (data) {
      console.log(data);
       var url = url_base + "newCampaign/";
       return machadaloHttp.post(url, data);
      };

    pagesService.getCampaigns = function (status) {
       var url = url_base + "getCampaigns/?status=" + status;
       return machadaloHttp.get(url);
      };


    pagesService.saveFinalizedInventory = function (data) {
      var url = url_base + "campaign/" + data.inventory[0].inventories[0].campaign + "/inventories/";
      return machadaloHttp.post(url, data);
    };

    pagesService.getSocietyInventory = function (id) {
       var url = url_base + "campaign/" + id + "/inventories/";//The id here referes to campaign id
       return machadaloHttp.get(url);
      };

    pagesService.removeThisSociety = function(society_id, type) {
      var url = url_base + "campaign/" + society_id + "/inventories/?type=" + type; //The id here referes to societybooking id to be deleted, not campaign id
      return machadaloHttp.delete(url);
     }

     pagesService.book = function (campaign_id, new_status) {
      var url = url_base + "campaign/" + campaign_id+ "/book/?status=" + new_status;
      return machadaloHttp.get(url);
    };


    pagesService.processParam = function(){
     if($stateParams.campaignId){
       $rootScope.campaignId = $stateParams.campaignId;
     }else {
       $rootScope.campaignId = null;
     }
   };

   return pagesService;
}]);
