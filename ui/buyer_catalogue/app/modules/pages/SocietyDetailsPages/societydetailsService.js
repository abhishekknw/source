'use strict';
angular.module('catalogueApp')
.factory('societyDetailsViewService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

   var url_base = 'v0/ui/website/';
   var societyDetailsViewService = {};
   var url_base_societyDetails ='v0/ui/';
   var url_base_user = 'v0/';


   //Start: code added for societydetails
   societyDetailsViewService.getSociety = function (id,supplierTypeCode) {
     console.log(id);
      var url = url_base_societyDetails + "supplier/" + id + "/image_details/?supplierTypeCode=" + supplierTypeCode;;
      return machadaloHttp.get(url);
   };
   societyDetailsViewService.get_inventory_summary = function(id, supplierTypeCode){
     var url = url_base_societyDetails + "society/" + id + "/inventory_summary/?supplierTypeCode=" + supplierTypeCode;
     return machadaloHttp.get(url);
   };
   societyDetailsViewService.processParam = function(){
    if($stateParams.campaignId){
      $rootScope.campaignId = $stateParams.campaignId;
    }else {
      $rootScope.campaignId = null;
     }

     if($stateParams.societyId){
      $rootScope.societyId = $stateParams.societyId;
    }else {
      $rootScope.societyId = null;
    }
   };
   return societyDetailsViewService;
}]);
