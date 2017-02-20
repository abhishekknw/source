'use strict';
angular.module('catalogueApp')
.factory('opsExecutionPlanService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

   var url_base = 'v0/ui/website/';
   var opsExecutionPlanService = {};

   opsExecutionPlanService.getOpsExecutionImageDetails = function(proposal_id){
        var url = url_base + "inventory-activity-image/" + "?proposal_id=" + proposal_id;
     return machadaloHttp.get(url);
   }

   opsExecutionPlanService.getSuppierDetails = function(supplier_id,supplier_type_code){
     var url = url_base + "supplier-details/" + "?supplier_id=" + supplier_id  + "&supplier_type_code=" + supplier_type_code;
     return machadaloHttp.get(url);
   }

   opsExecutionPlanService.getSummaryDetails = function(proposal_id){
        var url = url_base + "generate-inventory-activity-summary/" + "?proposal_id=" + proposal_id;
     return machadaloHttp.get(url);
   }


   return opsExecutionPlanService;
}]);
