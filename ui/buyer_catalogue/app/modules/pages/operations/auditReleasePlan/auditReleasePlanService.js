'use strict';
angular.module('catalogueApp')
.factory('auditReleasePlanService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

   var url_base = 'v0/ui/website/';
   var auditReleasePlanService = {};


   auditReleasePlanService.getCampaignReleaseDetails = function(proposal_id){
        var url = url_base + proposal_id + "/campaign-inventories/";
     return machadaloHttp.get(url);
   }


    auditReleasePlanService.updateAuditReleasePlanDetails = function(proposal_id,data){
         var url = url_base + proposal_id + "/campaign-inventories/";
      return machadaloHttp.put(url,data);
    }

    auditReleasePlanService.saveUser = function(data){
      var url = url_base + 'inventory-activity-assignment/';
      return machadaloHttp.post(url,data);
    }
   return auditReleasePlanService;
  return 0;
}]);
