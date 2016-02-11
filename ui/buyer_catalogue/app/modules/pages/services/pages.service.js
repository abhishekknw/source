'use strict';

/**
 * @ngdoc service
 * @name mdopsApp.societyDetailsService
 * @description
 * # societyDetailsService
 * Service in the mdopsApp.
 */

angular.module('machadaloPages').factory('pagesService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    
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

    pagesService.getRequestedCampaigns = function () {
       var url = url_base + "finalizeCampaign/";
       return machadaloHttp.get(url);
      };

    pagesService.getRequestedInventory = function (id) {
       var url = url_base + "campaign/" + id + "/inventories/";
       return machadaloHttp.get(url);
      };

      

    pagesService.processParam = function(){
     if($stateParams.campaignId)
     {
       $rootScope.campaignId = $stateParams.campaignId;
     }
     else {
       $rootScope.campaignId = null;
     }
   };

   return pagesService;
}]);